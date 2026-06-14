"""PEP 561 type stubs for dspygen.rdddy.base_aggregate."""

from collections.abc import Callable
from typing import Any, Optional, Type, TYPE_CHECKING

from dspygen.rdddy.base_inhabitant import BaseInhabitant
from dspygen.rdddy.base_message import BaseMessage

if TYPE_CHECKING:
    from dspygen.rdddy.service_colony import ServiceColony

__all__ = ["BaseAggregate"]


class BaseAggregate(BaseInhabitant):
    """Cornerstone of the domain model within the RDDDY framework.

    Encapsulates a cluster of domain objects treated as a single unit for data
    changes, enforcing invariants across the entire group.
    """

    service_colony: "ServiceColony"
    inhabitant_id: int

    def __init__(
        self,
        service_colony: "ServiceColony",
        inhabitant_id: Optional[int] = ...,
    ) -> None: ...

    async def start(self, scheduler: Any) -> None: ...
    def on_next(self, message: BaseMessage) -> None: ...
    def on_error(self, error: Any) -> None: ...
    def on_completed(self) -> None: ...
    async def receive(self, message: BaseMessage) -> None: ...
    async def publish(self, message: BaseMessage) -> None: ...
    def map_handlers(self) -> dict[Type[BaseMessage], Callable[..., Any]]: ...
