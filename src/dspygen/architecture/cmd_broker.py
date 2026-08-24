"""BRCE boundary enforcing grant, consent, idempotency, budgets, and postconditions."""
from __future__ import annotations

from dataclasses import asdict
from datetime import datetime, timezone
from typing import Any, Callable, MutableMapping

from dspygen.architecture.cmd_kernel import validate_external_intent
from dspygen.architecture.cmd_types import (
    ArchitectureRefusal,
    BrokerPolicy,
    Consent,
    Grant,
    Intent,
    Receipt,
    Standing,
    canonical_json,
    utc_now,
)
from dspygen.architecture.digest import blake3_hex


def _parse(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _not_expired(value: str) -> bool:
    return _parse(value) > datetime.now(timezone.utc)


def execute(
    intent: Intent,
    grant: Grant,
    consent: Consent,
    *,
    adapter: Callable[[Intent], Any],
    observe_postcondition: Callable[[Intent, Any], bool],
    idempotency_ledger: MutableMapping[str, str],
    previous_receipt: str | None = None,
    policy: BrokerPolicy = BrokerPolicy(),
) -> Receipt:
    validate_external_intent(intent)
    if policy.circuit_open:
        raise ArchitectureRefusal("BROKER-CIRCUIT-OPEN")
    if policy.error_budget_remaining <= 0:
        raise ArchitectureRefusal("BROKER-ERROR-BUDGET-EXHAUSTED")
    if policy.max_retries < 0:
        raise ArchitectureRefusal("CMD-RESOURCE-BOUND", "negative retry budget")
    if grant.intent_id != intent.intent_id:
        raise ArchitectureRefusal("AUTH-SCOPE-MISMATCH", "intent")
    if not _not_expired(intent.expiry) or not _not_expired(grant.expiry):
        raise ArchitectureRefusal("AUTH-GRANT-EXPIRED")
    if intent.operation not in grant.scope_operations:
        raise ArchitectureRefusal("AUTH-SCOPE-MISMATCH", intent.operation)
    if consent.revocation_state != "active":
        raise ArchitectureRefusal("EXT-REVOCATION-UNKNOWN")
    if consent.action != intent.operation:
        raise ArchitectureRefusal("EXT-CONSENT-SCOPE", consent.action)
    if not _not_expired(consent.expiry):
        raise ArchitectureRefusal("EXT-CONSENT-MISSING", "expired")
    for key, requested in intent.resource_budget.items():
        if requested > grant.resource_ceiling.get(key, -1):
            raise ArchitectureRefusal("CMD-RESOURCE-BOUND", key)
    if intent.idempotency_key in idempotency_ledger:
        raise ArchitectureRefusal("AUTH-SCOPE-MISMATCH", "duplicate idempotency key")

    consequence = None
    last_error: Exception | None = None
    for _attempt in range(policy.max_retries + 1):
        try:
            consequence = adapter(intent)
            last_error = None
            break
        except Exception as exc:
            last_error = exc
    if last_error is not None:
        raise ArchitectureRefusal("BROKER-RETRY-EXHAUSTED", type(last_error).__name__)
    if not observe_postcondition(intent, consequence):
        raise ArchitectureRefusal("EXT-POSTCONDITION")
    consequence_digest = blake3_hex(canonical_json(consequence).encode())
    grant_digest = blake3_hex(canonical_json(asdict(grant)).encode())
    receipt = Receipt(
        schema="cmd.external-receipt.v1",
        operation=intent.operation,
        intent_digest=blake3_hex(canonical_json(intent.to_dict()).encode()),
        grant_digest=grant_digest,
        subject_revision=intent.subject_digest,
        pre_state_digest=grant.precondition_digest,
        plan_digest=intent.candidate_id,
        artifacts=(("external-consequence", consequence_digest),),
        post_state_digest=consequence_digest,
        postcondition="observed",
        verifier_report_digest=consequence_digest,
        previous_receipt=previous_receipt,
        standing_result=Standing.PARTIAL_ALIVE,
        typed_refusals=(),
        issued_at=utc_now(),
    )
    idempotency_ledger[intent.idempotency_key] = receipt.receipt_id
    return receipt


def run_autonomic_controller(
    trigger: Any,
    *,
    monitor: Callable[[Any], Any],
    analyze: Callable[[Any], Any],
    plan: Callable[[Any], Intent | None],
    execute_via_brce: Callable[[Intent], Receipt],
    converged: Callable[[Any], bool],
    max_cycles: int = 5,
) -> tuple[Receipt, ...]:
    """Bounded MAPE-K controller. Execution can only occur through the supplied BRCE rail."""
    if max_cycles <= 0:
        raise ArchitectureRefusal("AUTONOMIC-NON-CONVERGENCE", "invalid cycle bound")
    state = trigger
    receipts: list[Receipt] = []
    seen: set[str] = set()
    for _ in range(max_cycles):
        observation = monitor(state)
        signature = blake3_hex(canonical_json(observation).encode())
        if signature in seen:
            raise ArchitectureRefusal("AUTONOMIC-OSCILLATION")
        seen.add(signature)
        if converged(observation):
            return tuple(receipts)
        diagnosis = analyze(observation)
        intent = plan(diagnosis)
        if intent is None:
            raise ArchitectureRefusal("AUTONOMIC-PLAN-MISSING")
        receipts.append(execute_via_brce(intent))
        state = observation
    raise ArchitectureRefusal("AUTONOMIC-NON-CONVERGENCE", f"cycles={max_cycles}")
