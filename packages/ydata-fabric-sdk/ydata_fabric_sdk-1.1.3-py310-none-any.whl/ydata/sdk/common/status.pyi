from .model import BaseModel
from typing import Generic, TypeVar

T = TypeVar('T')

class GenericStateErrorStatus(BaseModel, Generic[T]):
    state: T | None
    class Config:
        use_enum_values: bool
