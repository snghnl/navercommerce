"""Exception hierarchy for the Naver Commerce SDK."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Optional

if TYPE_CHECKING:
    import httpx


class NaverCommerceError(Exception):
    """Base exception for all Naver Commerce SDK errors."""

    pass


class APIError(NaverCommerceError):
    """Base exception for all API-related errors."""

    def __init__(
        self,
        message: str,
        *,
        code: Optional[str] = None,
        timestamp: Optional[str] = None,
        trace_id: Optional[str] = None,
        invalid_inputs: Optional[List[Dict[str, Any]]] = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.code = code
        self.timestamp = timestamp
        self.trace_id = trace_id
        self.invalid_inputs = invalid_inputs or []

    def __repr__(self) -> str:
        items = [f"message={self.message!r}"]
        if self.code:
            items.append(f"code={self.code!r}")
        if self.trace_id:
            items.append(f"trace_id={self.trace_id!r}")
        return f"{self.__class__.__name__}({', '.join(items)})"


class APIConnectionError(APIError):
    """Exception raised when the client fails to connect to the API."""

    def __init__(
        self,
        message: str = "Connection error occurred",
        *,
        request: Optional[httpx.Request] = None,
    ) -> None:
        super().__init__(message)
        self.request = request


class APITimeoutError(APIConnectionError):
    """Exception raised when a request times out."""

    def __init__(
        self,
        message: str = "Request timed out",
        *,
        request: Optional[httpx.Request] = None,
    ) -> None:
        super().__init__(message, request=request)


class APIStatusError(APIError):
    """Exception raised when the API returns a non-success status code."""

    def __init__(
        self,
        message: str,
        *,
        response: httpx.Response,
        body: Optional[Dict[str, Any]] = None,
        code: Optional[str] = None,
        timestamp: Optional[str] = None,
        trace_id: Optional[str] = None,
        invalid_inputs: Optional[List[Dict[str, Any]]] = None,
    ) -> None:
        super().__init__(
            message,
            code=code,
            timestamp=timestamp,
            trace_id=trace_id,
            invalid_inputs=invalid_inputs,
        )
        self.response = response
        self.status_code = response.status_code
        self.body = body
        self.request = response.request

    def __repr__(self) -> str:
        items = [
            f"message={self.message!r}",
            f"status_code={self.status_code}",
        ]
        if self.code:
            items.append(f"code={self.code!r}")
        if self.trace_id:
            items.append(f"trace_id={self.trace_id!r}")
        return f"{self.__class__.__name__}({', '.join(items)})"


class BadRequestError(APIStatusError):
    """
    Exception raised when the API returns a 400 Bad Request status code.

    Common error codes:
    - E400S00: Invalid request parameter
    - E400S01: Missing required parameter
    - E400S02: Invalid parameter format
    - E400S03: Invalid parameter value
    - E400S98: Business logic validation failed
    - E400S99: Other bad request error
    """

    pass


class AuthenticationError(APIStatusError):
    """
    Exception raised when the API returns a 401 Unauthorized status code.

    Common error codes:
    - E401A01: Invalid or expired access token
    """

    pass


class PermissionDeniedError(APIStatusError):
    """
    Exception raised when the API returns a 403 Forbidden status code.

    Common error codes:
    - E403A01: Insufficient permissions for the requested resource
    """

    pass


class NotFoundError(APIStatusError):
    """
    Exception raised when the API returns a 404 Not Found status code.

    Common error codes:
    - E404S00: Requested resource not found
    """

    pass


class ConflictError(APIStatusError):
    """
    Exception raised when the API returns a 409 Conflict status code.

    Common error codes:
    - E409S00: Resource conflict (e.g., duplicate)
    """

    pass


class InternalServerError(APIStatusError):
    """
    Exception raised when the API returns a 500 Internal Server Error status code.

    Common error codes:
    - E500A01: Authentication server error
    - E500S00: Internal server error
    - E500S99: Unexpected server error
    """

    pass


class OAuthError(NaverCommerceError):
    """Base exception for OAuth-related errors."""

    pass


class TokenExpiredError(OAuthError):
    """Exception raised when an access token has expired."""

    def __init__(self, message: str = "Access token has expired") -> None:
        super().__init__(message)


class TokenRefreshError(OAuthError):
    """Exception raised when token refresh fails."""

    def __init__(
        self,
        message: str = "Failed to refresh access token",
        *,
        cause: Optional[Exception] = None,
    ) -> None:
        super().__init__(message)
        self.cause = cause


# Error code to exception mapping
ERROR_CODE_TO_EXCEPTION: Dict[str, type[APIStatusError]] = {
    # 400 errors
    "E400S00": BadRequestError,
    "E400S01": BadRequestError,
    "E400S02": BadRequestError,
    "E400S03": BadRequestError,
    "E400S98": BadRequestError,
    "E400S99": BadRequestError,
    # 401 errors
    "E401A01": AuthenticationError,
    # 403 errors
    "E403A01": PermissionDeniedError,
    # 404 errors
    "E404S00": NotFoundError,
    # 409 errors
    "E409S00": ConflictError,
    # 500 errors
    "E500A01": InternalServerError,
    "E500S00": InternalServerError,
    "E500S99": InternalServerError,
}

# HTTP status code to exception mapping (fallback)
STATUS_CODE_TO_EXCEPTION: Dict[int, type[APIStatusError]] = {
    400: BadRequestError,
    401: AuthenticationError,
    403: PermissionDeniedError,
    404: NotFoundError,
    409: ConflictError,
    500: InternalServerError,
    502: InternalServerError,
    503: InternalServerError,
    504: InternalServerError,
}
