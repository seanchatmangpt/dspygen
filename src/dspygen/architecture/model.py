"""Pure deterministic DSPyGen architecture law."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Mapping

REQUIRED_BROKER = "BRCE"
REQUIRED_EVIDENCE = (
    "witness",
    "falsifier",
    "independent_verifier",
    "receipt_verifier",
    "replay",
)


class LifecycleState(str, Enum):
    DISCOVERED = "discovered"
    ACQUIRED = "acquired"
    IDENTIFIED = "identified"
    QUALIFIED = "qualified"
    ADMITTED = "admitted"
    COMPOSED = "composed"
    MATERIALIZED = "materialized"
    PROJECTED = "projected"
    AUTHORIZED = "authorized"
    ACTIVE = "active"
    DEPRECATED = "deprecated"
    RETIRED = "retired"
    ARCHIVED = "archived"

    def allows(self, target: "LifecycleState") -> bool:
        if self is target:
            return True
        transitions = {
            self.DISCOVERED: {self.ACQUIRED, self.RETIRED},
            self.ACQUIRED: {self.IDENTIFIED, self.RETIRED},
            self.IDENTIFIED: {self.QUALIFIED, self.RETIRED},
            self.QUALIFIED: {self.ADMITTED, self.RETIRED},
            self.ADMITTED: {self.COMPOSED, self.RETIRED},
            self.COMPOSED: {self.MATERIALIZED, self.RETIRED},
            self.MATERIALIZED: {self.PROJECTED, self.RETIRED},
            self.PROJECTED: {self.AUTHORIZED, self.RETIRED},
            self.AUTHORIZED: {self.ACTIVE, self.DEPRECATED, self.RETIRED},
            self.ACTIVE: {self.DEPRECATED},
            self.DEPRECATED: {self.ACTIVE, self.RETIRED},
            self.RETIRED: {self.ARCHIVED},
            self.ARCHIVED: set(),
        }
        return target in transitions[self]


class Standing(str, Enum):
    PARTIAL_ALIVE = "PARTIAL_ALIVE"
    ALIVE = "ALIVE"
    BLOCKED = "BLOCKED"
    BUILD_BROKEN = "BUILD_BROKEN"
    UNKNOWN = "UNKNOWN"
    UNSUPPORTED = "UNSUPPORTED"


class ArchitectureRefusal(ValueError):
    """Typed refusal raised when an architecture law would be violated."""


@dataclass(frozen=True)
class EvidenceSet:
    witness: bool = False
    falsifier: bool = False
    independent_verifier: bool = False
    receipt_verifier: bool = False
    replay: bool = False

    def missing(self) -> tuple[str, ...]:
        return tuple(name for name in REQUIRED_EVIDENCE if not getattr(self, name))

    def standing(self) -> Standing:
        return Standing.ALIVE if not self.missing() else Standing.PARTIAL_ALIVE

    def require_alive(self) -> None:
        missing = self.missing()
        if missing:
            raise ArchitectureRefusal(f"ALIVE_REFUSED missing_evidence={','.join(missing)}")


@dataclass(frozen=True)
class BrokerIntent:
    intent_id: str
    action: str
    payload_digest: str
    authority: tuple[str, ...]
    resource_ceiling: Mapping[str, int]
    broker: str = REQUIRED_BROKER

    def validate(self) -> None:
        if not self.intent_id.strip():
            raise ArchitectureRefusal("EMPTY_INTENT_ID_REFUSED")
        if not self.action.strip():
            raise ArchitectureRefusal("EMPTY_ACTION_REFUSED")
        if self.broker != REQUIRED_BROKER:
            raise ArchitectureRefusal(
                f"DIRECT_ACTUATION_REFUSED required_broker={REQUIRED_BROKER} actual={self.broker}"
            )
        if len(self.payload_digest) != 64:
            raise ArchitectureRefusal("INVALID_BLAKE3_DIGEST_REFUSED")
        if any(value < 0 for value in self.resource_ceiling.values()):
            raise ArchitectureRefusal("NEGATIVE_RESOURCE_CEILING_REFUSED")

    def to_dict(self) -> dict[str, object]:
        self.validate()
        return {
            "schema": "dspygen.brce.intent.v1",
            "intent_id": self.intent_id,
            "action": self.action,
            "payload_digest": self.payload_digest,
            "authority": list(self.authority),
            "resource_ceiling": dict(sorted(self.resource_ceiling.items())),
            "broker": self.broker,
        }
