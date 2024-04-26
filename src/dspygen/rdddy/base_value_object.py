from pydantic import BaseModel, ConfigDict
from typing import Any


class BaseValueObject(BaseModel):
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    # Example of a method that might be common across all value objects
    def __eq__(self, other: Any) -> bool:
        if isinstance(other, self.__class__):
            return self.model_dump() == other.model_dump()
        return False
