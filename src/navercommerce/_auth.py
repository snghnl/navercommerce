"""OAuth 2.0 token management for the Naver Commerce SDK."""

from __future__ import annotations

import time
from threading import Lock
from typing import Any, Optional

import httpx

from ._constants import (
    OAUTH_TOKEN_URL,
    TOKEN_EXPIRY_SECONDS,
    TOKEN_REFRESH_THRESHOLD_SECONDS,
)
from ._exceptions import TokenRefreshError


class TokenInfo:
    """Container for OAuth token information."""

    def __init__(
        self,
        access_token: str,
        expires_in: int,
        token_type: str = "Bearer",
    ) -> None:
        self.access_token = access_token
        self.expires_in = expires_in
        self.token_type = token_type
        self.issued_at = time.time()

    @property
    def expires_at(self) -> float:
        """Return the timestamp when this token expires."""
        return self.issued_at + self.expires_in

    @property
    def is_expired(self) -> bool:
        """Check if the token is expired."""
        return time.time() >= self.expires_at

    @property
    def should_refresh(self) -> bool:
        """
        Check if the token should be refreshed.
        Returns True if token will expire within the refresh threshold.
        """
        remaining = self.expires_at - time.time()
        return remaining <= (self.expires_in - TOKEN_REFRESH_THRESHOLD_SECONDS)

    def __repr__(self) -> str:
        return f"TokenInfo(token_type={self.token_type!r}, expires_in={self.expires_in})"


class OAuth2TokenManager:
    """
    Manages OAuth 2.0 access tokens with automatic refresh.

    This class handles:
    - Fetching access tokens using client credentials
    - Caching tokens to avoid unnecessary requests
    - Automatic token refresh when nearing expiration
    - Thread-safe token management
    """

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        base_url: str,
        http_client: Optional[httpx.Client] = None,
    ) -> None:
        self._client_id = client_id
        self._client_secret = client_secret
        self._base_url = base_url
        self._http_client = http_client
        self._owns_http_client = http_client is None

        self._token: Optional[TokenInfo] = None
        self._lock = Lock()

    def get_token(self) -> str:
        """
        Get a valid access token.

        Returns a cached token if available and not expired.
        Otherwise, fetches a new token from the API.

        Returns:
            The access token string.

        Raises:
            TokenRefreshError: If token fetch/refresh fails.
        """
        with self._lock:
            # Return cached token if it's still valid
            if self._token and not self._token.should_refresh:
                return self._token.access_token

            # Fetch new token
            self._refresh_token()
            assert self._token is not None  # for type checker
            return self._token.access_token

    def _refresh_token(self) -> None:
        """
        Fetch a new access token from the OAuth endpoint.

        Raises:
            TokenRefreshError: If the token request fails.
        """
        try:
            client = self._http_client or self._get_http_client()

            response = client.post(
                f"{self._base_url}{OAUTH_TOKEN_URL}",
                data={
                    "client_id": self._client_id,
                    "client_secret": self._client_secret,
                    "grant_type": "client_credentials",
                },
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                },
            )
            response.raise_for_status()

            data = response.json()
            self._token = TokenInfo(
                access_token=data["access_token"],
                expires_in=data.get("expires_in", TOKEN_EXPIRY_SECONDS),
                token_type=data.get("token_type", "Bearer"),
            )

        except httpx.HTTPStatusError as e:
            error_message = f"Failed to fetch access token: {e.response.status_code}"
            try:
                error_data = e.response.json()
                if "message" in error_data:
                    error_message = f"{error_message} - {error_data['message']}"
            except Exception:
                pass
            raise TokenRefreshError(error_message, cause=e) from e

        except httpx.RequestError as e:
            raise TokenRefreshError(
                f"Failed to connect to OAuth endpoint: {e}",
                cause=e,
            ) from e

        except (KeyError, ValueError) as e:
            raise TokenRefreshError(
                f"Invalid token response format: {e}",
                cause=e,
            ) from e

    def _get_http_client(self) -> httpx.Client:
        """Get or create an HTTP client for token requests."""
        if self._http_client is None:
            self._http_client = httpx.Client()
        return self._http_client

    def clear_token(self) -> None:
        """Clear the cached token, forcing a refresh on next access."""
        with self._lock:
            self._token = None

    def close(self) -> None:
        """Close the HTTP client if it's owned by this manager."""
        if self._owns_http_client and self._http_client is not None:
            self._http_client.close()
            self._http_client = None

    def __enter__(self) -> OAuth2TokenManager:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()

    def __del__(self) -> None:
        try:
            self.close()
        except Exception:
            pass


class AsyncOAuth2TokenManager:
    """
    Async version of OAuth2TokenManager.

    Manages OAuth 2.0 access tokens with automatic refresh for async contexts.
    """

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        base_url: str,
        http_client: Optional[httpx.AsyncClient] = None,
    ) -> None:
        self._client_id = client_id
        self._client_secret = client_secret
        self._base_url = base_url
        self._http_client = http_client
        self._owns_http_client = http_client is None

        self._token: Optional[TokenInfo] = None
        self._lock = Lock()  # Note: For true async, use asyncio.Lock

    async def get_token(self) -> str:
        """
        Get a valid access token.

        Returns a cached token if available and not expired.
        Otherwise, fetches a new token from the API.

        Returns:
            The access token string.

        Raises:
            TokenRefreshError: If token fetch/refresh fails.
        """
        with self._lock:
            # Return cached token if it's still valid
            if self._token and not self._token.should_refresh:
                return self._token.access_token

        # Refresh outside the lock (async operation)
        await self._refresh_token()

        with self._lock:
            assert self._token is not None  # for type checker
            return self._token.access_token

    async def _refresh_token(self) -> None:
        """
        Fetch a new access token from the OAuth endpoint.

        Raises:
            TokenRefreshError: If the token request fails.
        """
        try:
            client = self._http_client or self._get_http_client()

            response = await client.post(
                f"{self._base_url}{OAUTH_TOKEN_URL}",
                data={
                    "client_id": self._client_id,
                    "client_secret": self._client_secret,
                    "grant_type": "client_credentials",
                },
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                },
            )
            response.raise_for_status()

            data = response.json()

            with self._lock:
                self._token = TokenInfo(
                    access_token=data["access_token"],
                    expires_in=data.get("expires_in", TOKEN_EXPIRY_SECONDS),
                    token_type=data.get("token_type", "Bearer"),
                )

        except httpx.HTTPStatusError as e:
            error_message = f"Failed to fetch access token: {e.response.status_code}"
            try:
                error_data = e.response.json()
                if "message" in error_data:
                    error_message = f"{error_message} - {error_data['message']}"
            except Exception:
                pass
            raise TokenRefreshError(error_message, cause=e) from e

        except httpx.RequestError as e:
            raise TokenRefreshError(
                f"Failed to connect to OAuth endpoint: {e}",
                cause=e,
            ) from e

        except (KeyError, ValueError) as e:
            raise TokenRefreshError(
                f"Invalid token response format: {e}",
                cause=e,
            ) from e

    def _get_http_client(self) -> httpx.AsyncClient:
        """Get or create an async HTTP client for token requests."""
        if self._http_client is None:
            self._http_client = httpx.AsyncClient()
        return self._http_client

    def clear_token(self) -> None:
        """Clear the cached token, forcing a refresh on next access."""
        with self._lock:
            self._token = None

    async def aclose(self) -> None:
        """Close the HTTP client if it's owned by this manager."""
        if self._owns_http_client and self._http_client is not None:
            await self._http_client.aclose()
            self._http_client = None

    async def __aenter__(self) -> AsyncOAuth2TokenManager:
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.aclose()

    def __del__(self) -> None:
        try:
            if self._owns_http_client and self._http_client is not None:
                # Can't await in __del__, so we just close synchronously
                import asyncio
                try:
                    loop = asyncio.get_event_loop()
                    if loop.is_running():
                        loop.create_task(self.aclose())
                    else:
                        loop.run_until_complete(self.aclose())
                except Exception:
                    pass
        except Exception:
            pass
