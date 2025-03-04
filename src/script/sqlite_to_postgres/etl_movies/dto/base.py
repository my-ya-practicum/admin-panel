from typing import Protocol, Any, TypeVar, ClassVar
from dataclasses import Field, dataclass

import dacite


class DataClassProtocol(Protocol):
    __dataclass_fields__: ClassVar[dict[str, Field[Any]]]


DataClass = TypeVar("DataClass", bound=DataClassProtocol)


@dataclass
class DTO:
    @classmethod
    def from_dict(cls, params: dict) -> Any:
        return dacite.from_dict(data_class=cls, data=params)
