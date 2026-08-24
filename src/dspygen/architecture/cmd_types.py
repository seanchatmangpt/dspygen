"""Canonical object model for repository combinatorial maximalism."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Mapping

from dspygen.architecture.digest import blake3_hex


def canonical_json(value: Any) -> str:
    import json
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def content_id(prefix: str, value: Any) -> str:
    return f"{prefix}:{blake3_hex(canonical_json(value).encode())}"


class Standing(str, Enum):
    PARTIAL_ALIVE = "PARTIAL_ALIVE"
    ALIVE = "ALIVE"
    BLOCKED = "BLOCKED"
    BUILD_BROKEN = "BUILD_BROKEN"
    UNKNOWN = "UNKNOWN"
    UNSUPPORTED = "UNSUPPORTED"


class Lifecycle(str, Enum):
    EXPERIMENTAL = "EXPERIMENTAL"
    ACTIVE = "ACTIVE"
    DEPRECATED = "DEPRECATED"
    RETIRED = "RETIRED"
    ARCHIVED = "ARCHIVED"


class CandidateState(str, Enum):
    OBSERVED = "Observed"
    ADMITTED = "Admitted"
    CONSTRUCTED = "Constructed"
    VERIFIED = "Verified"
    AUTHORIZED = "Authorized"
    PLANNED = "Planned"
    ACTUATED = "Actuated"
    CONSEQUENCE_VERIFIED = "ConsequenceVerified"
    RECEIPTED = "Receipted"
    REPLAYED = "Replayed"


class Reversal(str, Enum):
    REVERSIBLE = "REVERSIBLE"
    REVERSIBLE_WITH_SNAPSHOT = "REVERSIBLE_WITH_SNAPSHOT"
    COMPENSATABLE = "COMPENSATABLE"
    IRREVERSIBLE = "IRREVERSIBLE"
    UNSUPPORTED = "UNSUPPORTED"
    UNKNOWN = "UNKNOWN"


class Ownership(str, Enum):
    EXCLUSIVE = "exclusive"
    SHARED_MERGE = "shared-merge"
    GENERATED_REGION = "generated-region"
    OBSERVE_ONLY = "observe-only"
    EXTERNAL = "external"


class ArchitectureRefusal(ValueError):
    def __init__(self, code: str, detail: str = "") -> None:
        self.code = code
        self.detail = detail
        super().__init__(f"{code}{': ' + detail if detail else ''}")


@dataclass(frozen=True)
class EvidenceSet:
    witness: bool = False
    falsifier: bool = False
    independent_verifier: bool = False
    receipt_verifier: bool = False
    replay: bool = False

    def missing(self) -> tuple[str, ...]:
        return tuple(k for k, v in asdict(self).items() if not v)

    def standing(self) -> Standing:
        return Standing.ALIVE if not self.missing() else Standing.PARTIAL_ALIVE


@dataclass(frozen=True)
class TreeEntry:
    path: str
    mode: str
    object_type: str
    object_sha: str
    surface: str
    semantic_owner: str
    operational_owner: str
    mutation_authority: str
    evidence_authority: str
    retirement_dependency: str


@dataclass(frozen=True)
class Observation:
    observation_id: str
    subject: str
    revision: str
    tree_digest: str
    observer_identity: str
    sequence: str
    scope: tuple[str, ...]
    excluded_surfaces: tuple[str, ...]
    freshness_limit_seconds: int
    provenance: str
    normalization_policy: str
    entries: tuple[TreeEntry, ...]
    workflows: tuple[str, ...]
    packages: tuple[str, ...]
    entry_points: tuple[str, ...]
    external_integrations: tuple[str, ...]
    unresolved: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class Dimension:
    dimension_id: str
    title: str
    owner: str
    options: tuple[str, ...]
    selection_cardinality: str = "exactly-one"
    dependencies: tuple[str, ...] = ()
    risk_class: str = "normal"
    coverage_mode: str = "exhaustive"


@dataclass(frozen=True)
class Constraint:
    constraint_id: str
    when: Mapping[str, str]
    require: Mapping[str, tuple[str, ...]] = field(default_factory=dict)
    exclude: Mapping[str, tuple[str, ...]] = field(default_factory=dict)
    refusal_code: str = "CMD-CONSTRAINT-VIOLATION"


@dataclass(frozen=True)
class Candidate:
    candidate_id: str
    options: tuple[tuple[str, str], ...]
    source_observation_digest: str
    constraint_policy_digest: str
    signature: str
    state: CandidateState = CandidateState.CONSTRUCTED
    standing: Standing = Standing.UNKNOWN

    def option_map(self) -> dict[str, str]:
        return dict(self.options)


@dataclass(frozen=True)
class AtomicPack:
    identity: str
    version: str
    pack_class: str
    provides: tuple[str, ...]
    requires: tuple[str, ...]
    owner: str
    ownership_claims: tuple[str, ...]
    verifier: str
    trust_floor: str
    content_digest: str


@dataclass(frozen=True)
class BuildingBlock:
    identity: str
    version: str
    purpose: str
    owner: str
    member_packs: tuple[str, ...]
    dependent_bblocks: tuple[str, ...]
    required_capabilities: tuple[str, ...]
    exclusive_capabilities: tuple[str, ...]
    policy_profile: str
    verifier_profile: str
    migration_law: str
    removal_law: str
    downstream_intents: tuple[str, ...]
    exclusions: tuple[str, ...]


@dataclass(frozen=True)
class PartPassport:
    identity: str
    conditioned_inputs: tuple[str, ...]
    guaranteed_outputs: tuple[str, ...]
    causal_polarity: str
    authority_ceiling: tuple[str, ...]
    resource_ceiling: Mapping[str, int]
    isolation_model: str
    host_profile: str
    jurisdiction_profile: str
    conformity_evidence: tuple[str, ...]
    independent_verifier: str
    receipt_format: str
    replacement_law: str
    retirement_law: str


@dataclass(frozen=True)
class Intent:
    intent_id: str
    candidate_id: str
    operation: str
    arguments: Mapping[str, Any]
    subject_digest: str
    desired_postcondition: Mapping[str, Any]
    required_authority: tuple[str, ...]
    resource_budget: Mapping[str, int]
    expiry: str
    idempotency_key: str
    required_broker: str = "BRCE"
    expected_evidence_classes: tuple[str, ...] = (
        "witness", "falsifier", "independent_verifier", "receipt_verifier", "replay"
    )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class Consent:
    subject: str
    action: str
    resource_scope: tuple[str, ...]
    purpose: str
    issuer: str
    issued_at: str
    expiry: str
    revocation_state: str
    evidence_digest: str


@dataclass(frozen=True)
class BrokerPolicy:
    max_retries: int = 3
    circuit_open: bool = False
    error_budget_remaining: float = 1.0
    max_autonomic_cycles: int = 5


@dataclass(frozen=True)
class Grant:
    grant_id: str
    intent_id: str
    approver_identity: str
    policy_digest: str
    scope_operations: tuple[str, ...]
    scope_resources: tuple[str, ...]
    resource_ceiling: Mapping[str, int]
    expiry: str
    precondition_digest: str


@dataclass(frozen=True)
class Artifact:
    path: str
    body: str
    ownership: Ownership
    owner: str
    reversal: Reversal

    @property
    def digest(self) -> str:
        return blake3_hex(self.body.encode())


@dataclass(frozen=True)
class Plan:
    plan_id: str
    observation_digest: str
    policy_digest: str
    candidate_id: str
    artifacts: tuple[Artifact, ...]
    external_intents: tuple[Intent, ...]
    standing: Standing = Standing.UNKNOWN
    actuation_performed: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class Receipt:
    schema: str
    operation: str
    intent_digest: str
    grant_digest: str | None
    subject_revision: str
    pre_state_digest: str
    plan_digest: str
    artifacts: tuple[tuple[str, str], ...]
    post_state_digest: str
    postcondition: str
    verifier_report_digest: str
    previous_receipt: str | None
    standing_result: Standing
    typed_refusals: tuple[str, ...]
    issued_at: str

    @property
    def receipt_id(self) -> str:
        return content_id("receipt", asdict(self))


@dataclass(frozen=True)
class CheckpointReport:
    checkpoint: str
    standing: Standing
    checks: Mapping[str, bool]
    evidence: EvidenceSet
    refusals: tuple[str, ...] = ()
    metrics: Mapping[str, float | int | str] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["standing"] = self.standing.value
        return value


@dataclass(frozen=True)
class CrownReport:
    revision: str
    tree_digest: str
    checkpoints: tuple[CheckpointReport, ...]
    external_standing: Standing
    aggregate_standing: Standing
    exact_head: bool
    detached_replay: bool
    clean_tree: bool
    report_id: str = ""

    def to_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["external_standing"] = self.external_standing.value
        value["aggregate_standing"] = self.aggregate_standing.value
        value["checkpoints"] = [c.to_dict() for c in self.checkpoints]
        value["report_id"] = self.report_id or content_id("verifier", value)
        return value


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
