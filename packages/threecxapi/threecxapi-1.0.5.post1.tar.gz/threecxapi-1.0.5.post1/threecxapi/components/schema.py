from typing import Any
from enum import auto
from functools import lru_cache

from pydantic import BaseModel, ConfigDict

from threecxapi.util import TcxStrEnum


class Schema(BaseModel):
    model_config = ConfigDict(populate_by_name=True, use_enum_values=True)

    def model_dump(self, **kwargs) -> dict[str, Any]:
        # Set default options for model_dump
        default_options = {
            "exclude_unset": True,
            "exclude_none": True,
            "serialize_as_any": True,
            "by_alias": True,
        }

        # Update with any user-provided options
        default_options.update(kwargs)
        # Call the original model_dump with the updated options
        return super().model_dump(**default_options)

    @classmethod
    @lru_cache
    def to_enum(cls) -> TcxStrEnum:
        """Creates an Enum based on the fields of the Schema class."""
        # Create a new TcxStrEnum
        return TcxStrEnum(
            cls.__name__ + "Properties", {field_name: auto() for field_name in cls.__annotations__.keys()}
        )
