"""Base model utilities for the Naver Commerce SDK."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Generic, Type, TypeVar, cast

from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict

if TYPE_CHECKING:
    from typing_extensions import Self

ModelT = TypeVar("ModelT", bound="BaseModel")


class BaseModel(PydanticBaseModel):
    """
    Base model for all Pydantic models in the SDK.

    Provides enhanced functionality over standard Pydantic models:
    - Proper __repr__ for debugging
    - Type construction and validation utilities
    - Pydantic v2 compatibility
    """

    model_config = ConfigDict(
        # Allow extra fields in responses (for forward compatibility)
        extra="allow",
        # Use enum values instead of enum objects
        use_enum_values=True,
        # Validate default values
        validate_default=True,
        # Validate assignments
        validate_assignment=True,
        # Populate by name (allows both snake_case and camelCase)
        populate_by_name=True,
    )

    def __repr__(self) -> str:
        """Return a string representation of the model."""
        fields = []
        for name, value in self.model_dump(exclude_unset=True).items():
            if isinstance(value, str):
                fields.append(f"{name}={value!r}")
            else:
                fields.append(f"{name}={value}")
        return f"{self.__class__.__name__}({', '.join(fields)})"

    @classmethod
    def construct_type(
        cls: Type[ModelT],
        value: Any,
    ) -> ModelT:
        """
        Construct a model instance from a value.

        This is useful for creating models from API responses without
        full validation. Use with caution.

        Args:
            value: The value to construct from (dict, model, etc.)

        Returns:
            A model instance.
        """
        if isinstance(value, cls):
            return value

        if isinstance(value, dict):
            return cls.model_construct(**value)

        raise TypeError(
            f"Cannot construct {cls.__name__} from {type(value).__name__}"
        )

    @classmethod
    def validate_type(
        cls: Type[ModelT],
        value: Any,
    ) -> ModelT:
        """
        Validate and construct a model instance from a value.

        This performs full validation, unlike construct_type.

        Args:
            value: The value to validate (dict, model, etc.)

        Returns:
            A validated model instance.
        """
        if isinstance(value, cls):
            return value

        return cls.model_validate(value)

    def to_dict(
        self,
        *,
        exclude_unset: bool = False,
        exclude_none: bool = False,
    ) -> dict[str, Any]:
        """
        Convert the model to a dictionary.

        Args:
            exclude_unset: Whether to exclude fields that were not explicitly set
            exclude_none: Whether to exclude fields with None values

        Returns:
            A dictionary representation of the model.
        """
        return self.model_dump(
            exclude_unset=exclude_unset,
            exclude_none=exclude_none,
            by_alias=True,
        )


class GenericModel(BaseModel, Generic[ModelT]):
    """
    Generic base model for parameterized types.

    This is useful for creating generic response wrappers.
    """

    pass


def construct_type(*, value: object, type_: Type[ModelT]) -> ModelT:
    """
    Construct a model instance of the given type from a value.

    Args:
        value: The value to construct from
        type_: The target type

    Returns:
        A model instance of the specified type.
    """
    if isinstance(value, type_):
        return value

    if isinstance(value, BaseModel):
        if isinstance(value, type_):
            return value
        raise TypeError(
            f"Cannot construct {type_.__name__} from {type(value).__name__}"
        )

    if isinstance(value, dict):
        if issubclass(type_, BaseModel):
            return cast(ModelT, type_.model_construct(**value))

    raise TypeError(f"Cannot construct {type_.__name__} from {type(value).__name__}")


def validate_type(*, value: object, type_: Type[ModelT]) -> ModelT:
    """
    Validate and construct a model instance of the given type from a value.

    Args:
        value: The value to validate
        type_: The target type

    Returns:
        A validated model instance of the specified type.
    """
    if isinstance(value, type_):
        return value

    if issubclass(type_, BaseModel):
        return cast(ModelT, type_.model_validate(value))

    raise TypeError(f"Cannot validate {type_.__name__} from {type(value).__name__}")
