from typing import Protocol, Any, TypeVar, ClassVar
from dataclasses import Field


class DataClassProtocol(Protocol):
    __dataclass_fields__: ClassVar[dict[str, Field[Any]]]


DataClass = TypeVar("DataClass", bound=DataClassProtocol)
