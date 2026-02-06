"""Base HTTP client implementation for the Naver Commerce SDK."""

from __future__ import annotations

import time
from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    cast,
    get_args,
    get_origin,
)

import httpx

from ._auth import AsyncOAuth2TokenManager, OAuth2TokenManager
from ._constants import (
    DEFAULT_MAX_RETRIES,
    DEFAULT_TIMEOUT,
    INITIAL_RETRY_DELAY,
    MAX_RETRY_DELAY,
    RETRY_MULTIPLIER,
    USER_AGENT,
)
from ._exceptions import (
    ERROR_CODE_TO_EXCEPTION,
    STATUS_CODE_TO_EXCEPTION,
    APIConnectionError,
    APIError,
    APIStatusError,
    APITimeoutError,
)
from ._models import BaseModel
from ._types import Headers, RequestOptions, Timeout

if TYPE_CHECKING:
    from ._types import Body, FileTypes, HttpMethod

ResponseT = TypeVar("ResponseT")


def _merge_mappings(
    map1: Mapping[str, Any] | None,
    map2: Mapping[str, Any] | None,
) -> dict[str, Any]:
    """Merge two mappings, with map2 taking precedence."""
    result: dict[str, Any] = {}
    if map1:
        result.update(map1)
    if map2:
        result.update(map2)
    return result


class SyncAPIClient:
    """
    Synchronous API client with OAuth authentication, retry logic, and error handling.

    This client wraps httpx.Client and provides:
    - Automatic OAuth 2.0 token management
    - Exponential backoff retry logic
    - Comprehensive error handling with Naver-specific error codes
    - Request/response logging and debugging support
    """

    def __init__(
        self,
        *,
        client_id: str,
        client_secret: str,
        base_url: str,
        timeout: Timeout = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        http_client: httpx.Client | None = None,
        **kwargs: Any,
    ) -> None:
        # Initialize the token manager
        self._token_manager = OAuth2TokenManager(
            client_id=client_id,
            client_secret=client_secret,
            base_url=base_url,
            http_client=http_client,
        )

        self._max_retries = max_retries
        self._base_url = base_url

        # Initialize the httpx.Client (composition pattern)
        self._client = httpx.Client(
            base_url=base_url,
            timeout=timeout if timeout is not None else DEFAULT_TIMEOUT,
            **kwargs,
        )

    def _prepare_request(
        self,
        *,
        headers: Headers | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Prepare request parameters by adding authentication and default headers.

        Args:
            headers: Optional headers to include in the request
            **kwargs: Additional request parameters

        Returns:
            Updated request parameters with auth headers
        """
        # Get OAuth token
        access_token = self._token_manager.get_token()

        # Merge headers
        request_headers: dict[str, str] = {
            "Authorization": f"Bearer {access_token}",
            "User-Agent": USER_AGENT,
        }
        if headers:
            request_headers.update(headers)

        kwargs["headers"] = request_headers
        return kwargs

    def _should_retry(self, response: httpx.Response) -> bool:
        """
        Determine if a request should be retried based on the response.

        Args:
            response: The HTTP response

        Returns:
            True if the request should be retried, False otherwise
        """
        # Retry on 429 (Too Many Requests) and 5xx errors
        if response.status_code == 429:
            return True
        if response.status_code >= 500:
            return True

        # Retry on 401 (token might need refresh)
        if response.status_code == 401:
            return True

        return False

    def _calculate_retry_delay(self, attempt: int) -> float:
        """
        Calculate the delay before the next retry using exponential backoff.

        Args:
            attempt: The retry attempt number (0-indexed)

        Returns:
            The delay in seconds
        """
        delay = INITIAL_RETRY_DELAY * (RETRY_MULTIPLIER**attempt)
        return min(delay, MAX_RETRY_DELAY)

    def _handle_error_response(self, response: httpx.Response) -> None:
        """
        Handle error responses by raising appropriate exceptions.

        Args:
            response: The HTTP response

        Raises:
            APIStatusError: For HTTP error responses
        """
        try:
            body = response.json()
        except Exception:
            body = None

        # Extract error information from the response
        error_code: str | None = None
        error_message = f"HTTP {response.status_code}"
        timestamp: str | None = None
        trace_id: str | None = None
        invalid_inputs: list[dict[str, Any]] | None = None

        if body and isinstance(body, dict):
            error_code = body.get("code")
            error_message = body.get("message", error_message)
            timestamp = body.get("timestamp")
            trace_id = body.get("traceId")
            invalid_inputs = body.get("invalidInputs")

        # Determine the exception class to raise
        exception_class: type[APIStatusError] = APIStatusError

        # First try to match by error code
        if error_code and error_code in ERROR_CODE_TO_EXCEPTION:
            exception_class = ERROR_CODE_TO_EXCEPTION[error_code]
        # Fall back to status code matching
        elif response.status_code in STATUS_CODE_TO_EXCEPTION:
            exception_class = STATUS_CODE_TO_EXCEPTION[response.status_code]

        raise exception_class(
            message=error_message,
            response=response,
            body=body,
            code=error_code,
            timestamp=timestamp,
            trace_id=trace_id,
            invalid_inputs=invalid_inputs,
        )

    def _request(
        self,
        method: HttpMethod,
        path: str,
        *,
        cast_to: type[ResponseT],
        options: RequestOptions | None = None,
        **kwargs: Any,
    ) -> ResponseT:
        """
        Make an HTTP request with retry logic and error handling.

        Args:
            method: The HTTP method
            path: The API path (will be appended to base_url)
            cast_to: The type to cast the response to
            options: Optional request options
            **kwargs: Additional request parameters

        Returns:
            The parsed response of type ResponseT

        Raises:
            APIConnectionError: For connection errors
            APITimeoutError: For timeout errors
            APIStatusError: For HTTP error responses
        """
        options = options or {}

        # Extract options
        max_retries = options.get("max_retries", self._max_retries)
        timeout = options.get("timeout")
        extra_headers = options.get("headers")
        extra_json = options.get("extra_json")
        extra_query = options.get("extra_query")

        # Merge extra options
        if extra_headers:
            kwargs["headers"] = _merge_mappings(kwargs.get("headers"), extra_headers)
        if extra_json and "json" in kwargs:
            kwargs["json"] = _merge_mappings(kwargs["json"], extra_json)
        if extra_query and "params" in kwargs:
            kwargs["params"] = _merge_mappings(kwargs["params"], extra_query)
        if timeout is not None:
            kwargs["timeout"] = timeout

        # Prepare request with auth
        # Extract headers from kwargs to avoid duplicate keyword argument
        headers = kwargs.pop("headers", None)
        kwargs = self._prepare_request(headers=headers, **kwargs)

        for attempt in range(max_retries + 1):
            try:
                response = self._client.request(method, path, **kwargs)

                # Check if we should retry
                if response.status_code >= 400:
                    if attempt < max_retries and self._should_retry(response):
                        # Special handling for 401 - clear token cache
                        if response.status_code == 401:
                            self._token_manager.clear_token()
                            # Re-prepare request with new token
                            headers = kwargs.pop("headers", None)
                            kwargs = self._prepare_request(headers=headers, **kwargs)

                        # Wait before retry
                        time.sleep(self._calculate_retry_delay(attempt))
                        continue

                    # No more retries, raise error
                    self._handle_error_response(response)

                # Success! Parse and return the response
                return self._parse_response(response, cast_to=cast_to)

            except httpx.TimeoutException as e:
                if attempt < max_retries:
                    time.sleep(self._calculate_retry_delay(attempt))
                    continue
                raise APITimeoutError(request=e.request) from e

            except httpx.RequestError as e:
                if attempt < max_retries:
                    time.sleep(self._calculate_retry_delay(attempt))
                    continue
                raise APIConnectionError(
                    f"Connection error: {e}",
                    request=getattr(e, "request", None),
                ) from e

        # Should not reach here, but just in case
        raise APIConnectionError(
            "Max retries exceeded",
            request=None,
        )

    def _parse_response(
        self,
        response: httpx.Response,
        *,
        cast_to: type[ResponseT],
    ) -> ResponseT:
        """
        Parse an HTTP response into the target type.

        Args:
            response: The HTTP response
            cast_to: The type to cast the response to

        Returns:
            The parsed response of type ResponseT
        """
        # Handle empty responses
        if not response.content:
            if cast_to is type(None):
                return cast(ResponseT, None)
            raise APIError("Expected response body but got empty response")

        # Handle string responses before JSON parsing
        if cast_to is str:
            return cast(ResponseT, response.text)

        # Handle None type
        if cast_to is type(None):
            return cast(ResponseT, None)

        # Parse JSON response
        data = response.json()

        # Handle Naver Commerce API response format
        # Most responses are wrapped in {"code": "SUCCESS", "data": {...}}
        if isinstance(data, dict) and "data" in data:
            data = data["data"]

        # Cast to the target type
        if cast_to is dict:
            return cast(ResponseT, data)
        elif cast_to is list:
            return cast(ResponseT, data)
        else:
            # Check if it's a generic type like list[Model]
            origin = get_origin(cast_to)
            if origin is list:
                # Handle list[Model] types
                args = get_args(cast_to)
                if args and len(args) > 0:
                    item_type = args[0]
                    # Check if the item type is a BaseModel
                    try:
                        if issubclass(item_type, BaseModel):
                            # Parse each item in the list as a model
                            if isinstance(data, list):
                                return cast(ResponseT, [item_type.model_validate(item) for item in data])
                    except TypeError:
                        pass
                # If not a model list or parsing failed, just return the data
                return cast(ResponseT, data)

            # Check if it's a BaseModel subclass (must be a class first)
            try:
                if issubclass(cast_to, BaseModel):
                    return cast(ResponseT, cast_to.model_validate(data))
            except TypeError:
                # cast_to is not a class, just return the data
                pass

            # For other generic types, just return the data
            return cast(ResponseT, data)

    def get(
        self,
        path: str,
        *,
        cast_to: type[ResponseT],
        options: RequestOptions | None = None,
        **kwargs: Any,
    ) -> ResponseT:
        """Make a GET request."""
        return self._request("GET", path, cast_to=cast_to, options=options, **kwargs)

    def post(
        self,
        path: str,
        *,
        cast_to: type[ResponseT],
        body: Body | None = None,
        files: Mapping[str, FileTypes] | None = None,
        options: RequestOptions | None = None,
        **kwargs: Any,
    ) -> ResponseT:
        """Make a POST request."""
        if body is not None:
            kwargs["json"] = body
        if files is not None:
            kwargs["files"] = files
        return self._request("POST", path, cast_to=cast_to, options=options, **kwargs)

    def put(
        self,
        path: str,
        *,
        cast_to: type[ResponseT],
        body: Body | None = None,
        options: RequestOptions | None = None,
        **kwargs: Any,
    ) -> ResponseT:
        """Make a PUT request."""
        if body is not None:
            kwargs["json"] = body
        return self._request("PUT", path, cast_to=cast_to, options=options, **kwargs)

    def patch(
        self,
        path: str,
        *,
        cast_to: type[ResponseT],
        body: Body | None = None,
        options: RequestOptions | None = None,
        **kwargs: Any,
    ) -> ResponseT:
        """Make a PATCH request."""
        if body is not None:
            kwargs["json"] = body
        return self._request("PATCH", path, cast_to=cast_to, options=options, **kwargs)

    def delete(
        self,
        path: str,
        *,
        cast_to: type[ResponseT],
        options: RequestOptions | None = None,
        **kwargs: Any,
    ) -> ResponseT:
        """Make a DELETE request."""
        return self._request("DELETE", path, cast_to=cast_to, options=options, **kwargs)

    def close(self) -> None:
        """Close the client and clean up resources."""
        self._token_manager.close()
        self._client.close()

    def __enter__(self) -> SyncAPIClient:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()


class AsyncAPIClient:
    """
    Asynchronous API client with OAuth authentication, retry logic, and error handling.

    This client wraps httpx.AsyncClient and provides:
    - Automatic OAuth 2.0 token management
    - Exponential backoff retry logic
    - Comprehensive error handling with Naver-specific error codes
    - Request/response logging and debugging support
    """

    def __init__(
        self,
        *,
        client_id: str,
        client_secret: str,
        base_url: str,
        timeout: Timeout = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        http_client: httpx.AsyncClient | None = None,
        **kwargs: Any,
    ) -> None:
        # Initialize the token manager
        self._token_manager = AsyncOAuth2TokenManager(
            client_id=client_id,
            client_secret=client_secret,
            base_url=base_url,
            http_client=http_client,
        )

        self._max_retries = max_retries
        self._base_url = base_url

        # Initialize the httpx.AsyncClient (composition pattern)
        self._client = httpx.AsyncClient(
            base_url=base_url,
            timeout=timeout if timeout is not None else DEFAULT_TIMEOUT,
            **kwargs,
        )

    async def _prepare_request(
        self,
        *,
        headers: Headers | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Prepare request parameters by adding authentication and default headers.

        Args:
            headers: Optional headers to include in the request
            **kwargs: Additional request parameters

        Returns:
            Updated request parameters with auth headers
        """
        # Get OAuth token
        access_token = await self._token_manager.get_token()

        # Merge headers
        request_headers: dict[str, str] = {
            "Authorization": f"Bearer {access_token}",
            "User-Agent": USER_AGENT,
        }
        if headers:
            request_headers.update(headers)

        kwargs["headers"] = request_headers
        return kwargs

    def _should_retry(self, response: httpx.Response) -> bool:
        """
        Determine if a request should be retried based on the response.

        Args:
            response: The HTTP response

        Returns:
            True if the request should be retried, False otherwise
        """
        # Retry on 429 (Too Many Requests) and 5xx errors
        if response.status_code == 429:
            return True
        if response.status_code >= 500:
            return True

        # Retry on 401 (token might need refresh)
        if response.status_code == 401:
            return True

        return False

    def _calculate_retry_delay(self, attempt: int) -> float:
        """
        Calculate the delay before the next retry using exponential backoff.

        Args:
            attempt: The retry attempt number (0-indexed)

        Returns:
            The delay in seconds
        """
        delay = INITIAL_RETRY_DELAY * (RETRY_MULTIPLIER**attempt)
        return min(delay, MAX_RETRY_DELAY)

    def _handle_error_response(self, response: httpx.Response) -> None:
        """
        Handle error responses by raising appropriate exceptions.

        Args:
            response: The HTTP response

        Raises:
            APIStatusError: For HTTP error responses
        """
        try:
            body = response.json()
        except Exception:
            body = None

        # Extract error information from the response
        error_code: str | None = None
        error_message = f"HTTP {response.status_code}"
        timestamp: str | None = None
        trace_id: str | None = None
        invalid_inputs: list[dict[str, Any]] | None = None

        if body and isinstance(body, dict):
            error_code = body.get("code")
            error_message = body.get("message", error_message)
            timestamp = body.get("timestamp")
            trace_id = body.get("traceId")
            invalid_inputs = body.get("invalidInputs")

        # Determine the exception class to raise
        exception_class: type[APIStatusError] = APIStatusError

        # First try to match by error code
        if error_code and error_code in ERROR_CODE_TO_EXCEPTION:
            exception_class = ERROR_CODE_TO_EXCEPTION[error_code]
        # Fall back to status code matching
        elif response.status_code in STATUS_CODE_TO_EXCEPTION:
            exception_class = STATUS_CODE_TO_EXCEPTION[response.status_code]

        raise exception_class(
            message=error_message,
            response=response,
            body=body,
            code=error_code,
            timestamp=timestamp,
            trace_id=trace_id,
            invalid_inputs=invalid_inputs,
        )

    async def _request(
        self,
        method: HttpMethod,
        path: str,
        *,
        cast_to: type[ResponseT],
        options: RequestOptions | None = None,
        **kwargs: Any,
    ) -> ResponseT:
        """
        Make an HTTP request with retry logic and error handling.

        Args:
            method: The HTTP method
            path: The API path (will be appended to base_url)
            cast_to: The type to cast the response to
            options: Optional request options
            **kwargs: Additional request parameters

        Returns:
            The parsed response of type ResponseT

        Raises:
            APIConnectionError: For connection errors
            APITimeoutError: For timeout errors
            APIStatusError: For HTTP error responses
        """
        import asyncio

        options = options or {}

        # Extract options
        max_retries = options.get("max_retries", self._max_retries)
        timeout = options.get("timeout")
        extra_headers = options.get("headers")
        extra_json = options.get("extra_json")
        extra_query = options.get("extra_query")

        # Merge extra options
        if extra_headers:
            kwargs["headers"] = _merge_mappings(kwargs.get("headers"), extra_headers)
        if extra_json and "json" in kwargs:
            kwargs["json"] = _merge_mappings(kwargs["json"], extra_json)
        if extra_query and "params" in kwargs:
            kwargs["params"] = _merge_mappings(kwargs["params"], extra_query)
        if timeout is not None:
            kwargs["timeout"] = timeout

        # Prepare request with auth
        # Extract headers from kwargs to avoid duplicate keyword argument
        headers = kwargs.pop("headers", None)
        kwargs = await self._prepare_request(headers=headers, **kwargs)

        for attempt in range(max_retries + 1):
            try:
                response = await self._client.request(method, path, **kwargs)

                # Check if we should retry
                if response.status_code >= 400:
                    if attempt < max_retries and self._should_retry(response):
                        # Special handling for 401 - clear token cache
                        if response.status_code == 401:
                            self._token_manager.clear_token()
                            # Re-prepare request with new token
                            headers = kwargs.pop("headers", None)
                            kwargs = await self._prepare_request(headers=headers, **kwargs)

                        # Wait before retry
                        await asyncio.sleep(self._calculate_retry_delay(attempt))
                        continue

                    # No more retries, raise error
                    self._handle_error_response(response)

                # Success! Parse and return the response
                return await self._parse_response(response, cast_to=cast_to)

            except httpx.TimeoutException as e:
                if attempt < max_retries:
                    await asyncio.sleep(self._calculate_retry_delay(attempt))
                    continue
                raise APITimeoutError(request=e.request) from e

            except httpx.RequestError as e:
                if attempt < max_retries:
                    await asyncio.sleep(self._calculate_retry_delay(attempt))
                    continue
                raise APIConnectionError(
                    f"Connection error: {e}",
                    request=getattr(e, "request", None),
                ) from e

        # Should not reach here, but just in case
        raise APIConnectionError(
            "Max retries exceeded",
            request=None,
        )

    async def _parse_response(
        self,
        response: httpx.Response,
        *,
        cast_to: type[ResponseT],
    ) -> ResponseT:
        """
        Parse an HTTP response into the target type.

        Args:
            response: The HTTP response
            cast_to: The type to cast the response to

        Returns:
            The parsed response of type ResponseT
        """
        # Handle empty responses
        if not response.content:
            if cast_to is type(None):
                return cast(ResponseT, None)
            raise APIError("Expected response body but got empty response")

        # Handle string responses before JSON parsing
        if cast_to is str:
            return cast(ResponseT, response.text)

        # Handle None type
        if cast_to is type(None):
            return cast(ResponseT, None)

        # Parse JSON response
        data = response.json()

        # Handle Naver Commerce API response format
        # Most responses are wrapped in {"code": "SUCCESS", "data": {...}}
        if isinstance(data, dict) and "data" in data:
            data = data["data"]

        # Cast to the target type
        if cast_to is dict:
            return cast(ResponseT, data)
        elif cast_to is list:
            return cast(ResponseT, data)
        else:
            # Check if it's a generic type like list[Model]
            origin = get_origin(cast_to)
            if origin is list:
                # Handle list[Model] types
                args = get_args(cast_to)
                if args and len(args) > 0:
                    item_type = args[0]
                    # Check if the item type is a BaseModel
                    try:
                        if issubclass(item_type, BaseModel):
                            # Parse each item in the list as a model
                            if isinstance(data, list):
                                return cast(ResponseT, [item_type.model_validate(item) for item in data])
                    except TypeError:
                        pass
                # If not a model list or parsing failed, just return the data
                return cast(ResponseT, data)

            # Check if it's a BaseModel subclass (must be a class first)
            try:
                if issubclass(cast_to, BaseModel):
                    return cast(ResponseT, cast_to.model_validate(data))
            except TypeError:
                # cast_to is not a class, just return the data
                pass

            # For other generic types, just return the data
            return cast(ResponseT, data)

    async def get(
        self,
        path: str,
        *,
        cast_to: type[ResponseT],
        options: RequestOptions | None = None,
        **kwargs: Any,
    ) -> ResponseT:
        """Make a GET request."""
        return await self._request("GET", path, cast_to=cast_to, options=options, **kwargs)

    async def post(
        self,
        path: str,
        *,
        cast_to: type[ResponseT],
        body: Body | None = None,
        files: Mapping[str, FileTypes] | None = None,
        options: RequestOptions | None = None,
        **kwargs: Any,
    ) -> ResponseT:
        """Make a POST request."""
        if body is not None:
            kwargs["json"] = body
        if files is not None:
            kwargs["files"] = files
        return await self._request("POST", path, cast_to=cast_to, options=options, **kwargs)

    async def put(
        self,
        path: str,
        *,
        cast_to: type[ResponseT],
        body: Body | None = None,
        options: RequestOptions | None = None,
        **kwargs: Any,
    ) -> ResponseT:
        """Make a PUT request."""
        if body is not None:
            kwargs["json"] = body
        return await self._request("PUT", path, cast_to=cast_to, options=options, **kwargs)

    async def patch(
        self,
        path: str,
        *,
        cast_to: type[ResponseT],
        body: Body | None = None,
        options: RequestOptions | None = None,
        **kwargs: Any,
    ) -> ResponseT:
        """Make a PATCH request."""
        if body is not None:
            kwargs["json"] = body
        return await self._request("PATCH", path, cast_to=cast_to, options=options, **kwargs)

    async def delete(
        self,
        path: str,
        *,
        cast_to: type[ResponseT],
        options: RequestOptions | None = None,
        **kwargs: Any,
    ) -> ResponseT:
        """Make a DELETE request."""
        return await self._request("DELETE", path, cast_to=cast_to, options=options, **kwargs)

    async def aclose(self) -> None:
        """Close the client and clean up resources."""
        await self._token_manager.aclose()
        await self._client.aclose()

    async def __aenter__(self) -> AsyncAPIClient:
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.aclose()
