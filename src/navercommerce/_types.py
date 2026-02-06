"""Custom types for the Naver Commerce SDK."""

from __future__ import annotations

from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    Literal,
    TypeVar,
    Union,
)

import httpx
from typing_extensions import TypeAlias, TypedDict

if TYPE_CHECKING:
    from pydantic import BaseModel as PydanticBaseModel

# Type variables
ResponseT = TypeVar("ResponseT")
ModelT = TypeVar("ModelT", bound="PydanticBaseModel")

# HTTP types
Headers: TypeAlias = Mapping[str, str]
Query: TypeAlias = Mapping[str, object]
Body: TypeAlias = Mapping[str, object]

# Timeout types
Timeout: TypeAlias = Union[float, httpx.Timeout, None]

# File types for uploads
FileTypes: TypeAlias = Union[
    # file (or bytes)
    bytes,
    # (filename, file (or bytes))
    tuple[str | None, bytes],
    # (filename, file (or bytes), content_type)
    tuple[str | None, bytes, str | None],
    # (filename, file (or bytes), content_type, headers)
    tuple[str | None, bytes, str | None, Mapping[str, str]],
]


class NotGiven:
    """
    A sentinel object used to distinguish omitted fields from fields that are explicitly set to None.

    Usage:
        def create_product(name: str, description: str | NotGiven = not_given):
            if not isinstance(description, NotGiven):
                # description was explicitly provided
                ...
    """

    def __bool__(self) -> Literal[False]:
        return False

    def __repr__(self) -> str:
        return "NOT_GIVEN"


# Singleton instance
not_given = NotGiven()

# NotGiven type for use in annotations
NotGivenOr = Union[NotGiven, TypeVar("T")]


class RequestOptions(TypedDict, total=False):
    """
    Options that can be passed to API methods to customize the request.

    Attributes:
        headers: Additional headers to include in the request
        max_retries: Maximum number of retries for this specific request
        timeout: Timeout for this specific request (seconds or httpx.Timeout)
        extra_json: Additional JSON fields to include in the request body
        extra_query: Additional query parameters to include in the request
    """

    headers: Headers
    max_retries: int
    timeout: Timeout
    extra_json: dict[str, Any]
    extra_query: dict[str, Any]


# HTTP method types
HttpMethod: TypeAlias = Literal["GET", "POST", "PUT", "PATCH", "DELETE"]

# OAuth grant type
OAuthGrantType: TypeAlias = Literal["client_credentials"]
