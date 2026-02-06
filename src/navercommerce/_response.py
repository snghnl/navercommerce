"""Response wrapper classes for the Naver Commerce SDK."""

from __future__ import annotations

from typing import Any, Generic, TypeVar, cast

import httpx

from ._models import BaseModel

ResponseT = TypeVar("ResponseT")


class APIResponse(Generic[ResponseT]):
    """
    Wrapper for API responses that provides access to both parsed data and raw HTTP response.

    This allows users to access the parsed response object while also being able to
    inspect the raw HTTP response, headers, status code, etc.

    Example:
        response = client.products.retrieve("123")
        product = response.parse()  # Get the parsed Product object
        status_code = response.status_code  # Access HTTP status code
        headers = response.headers  # Access response headers
        raw_response = response.http_response  # Access raw httpx.Response
    """

    def __init__(
        self,
        *,
        response: httpx.Response,
        cast_to: type[ResponseT],
        parsed: ResponseT | None = None,
    ) -> None:
        self._response = response
        self._cast_to = cast_to
        self._parsed = parsed

    @property
    def http_response(self) -> httpx.Response:
        """Get the raw httpx.Response object."""
        return self._response

    @property
    def status_code(self) -> int:
        """Get the HTTP status code."""
        return self._response.status_code

    @property
    def headers(self) -> httpx.Headers:
        """Get the response headers."""
        return self._response.headers

    @property
    def content(self) -> bytes:
        """Get the raw response content."""
        return self._response.content

    @property
    def text(self) -> str:
        """Get the response content as text."""
        return self._response.text

    @property
    def url(self) -> httpx.URL:
        """Get the request URL."""
        return self._response.url

    @property
    def request(self) -> httpx.Request:
        """Get the request that produced this response."""
        return self._response.request

    def parse(self) -> ResponseT:
        """
        Parse and return the response data.

        Returns:
            The parsed response object of type ResponseT.
        """
        if self._parsed is not None:
            return self._parsed

        # Parse the response
        data = self._response.json()

        # Handle Naver Commerce API response format
        # Most responses are wrapped in {"code": "SUCCESS", "data": {...}}
        if isinstance(data, dict) and "data" in data:
            data = data["data"]

        # Parse based on the target type
        if issubclass(self._cast_to, BaseModel):
            self._parsed = cast(ResponseT, self._cast_to.model_validate(data))
        else:
            self._parsed = cast(ResponseT, data)

        return self._parsed

    def json(self) -> Any:
        """Get the raw JSON response data."""
        return self._response.json()

    def __repr__(self) -> str:
        return f"APIResponse(status_code={self.status_code}, url={self.url!r}, cast_to={self._cast_to.__name__})"


class AsyncAPIResponse(Generic[ResponseT]):
    """
    Async version of APIResponse.

    Wrapper for API responses in async contexts that provides access to both
    parsed data and raw HTTP response.
    """

    def __init__(
        self,
        *,
        response: httpx.Response,
        cast_to: type[ResponseT],
        parsed: ResponseT | None = None,
    ) -> None:
        self._response = response
        self._cast_to = cast_to
        self._parsed = parsed

    @property
    def http_response(self) -> httpx.Response:
        """Get the raw httpx.Response object."""
        return self._response

    @property
    def status_code(self) -> int:
        """Get the HTTP status code."""
        return self._response.status_code

    @property
    def headers(self) -> httpx.Headers:
        """Get the response headers."""
        return self._response.headers

    @property
    def content(self) -> bytes:
        """Get the raw response content."""
        return self._response.content

    @property
    def text(self) -> str:
        """Get the response content as text."""
        return self._response.text

    @property
    def url(self) -> httpx.URL:
        """Get the request URL."""
        return self._response.url

    @property
    def request(self) -> httpx.Request:
        """Get the request that produced this response."""
        return self._response.request

    async def parse(self) -> ResponseT:
        """
        Parse and return the response data.

        Returns:
            The parsed response object of type ResponseT.
        """
        if self._parsed is not None:
            return self._parsed

        # Parse the response
        data = self._response.json()

        # Handle Naver Commerce API response format
        # Most responses are wrapped in {"code": "SUCCESS", "data": {...}}
        if isinstance(data, dict) and "data" in data:
            data = data["data"]

        # Parse based on the target type
        if issubclass(self._cast_to, BaseModel):
            self._parsed = cast(ResponseT, self._cast_to.model_validate(data))
        else:
            self._parsed = cast(ResponseT, data)

        return self._parsed

    def json(self) -> Any:
        """Get the raw JSON response data."""
        return self._response.json()

    def __repr__(self) -> str:
        return f"AsyncAPIResponse(status_code={self.status_code}, url={self.url!r}, cast_to={self._cast_to.__name__})"
