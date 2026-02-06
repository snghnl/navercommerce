"""Tests for base HTTP client implementation."""

from __future__ import annotations

import time
from unittest.mock import Mock, patch

import httpx
import pytest
from httpx import Request, Response

from navercommerce._base_client import AsyncAPIClient, SyncAPIClient
from navercommerce._exceptions import (
    APIConnectionError,
    APITimeoutError,
    AuthenticationError,
    BadRequestError,
    ConflictError,
    InternalServerError,
    NotFoundError,
    PermissionDeniedError,
)
from navercommerce._models import BaseModel


class SampleModel(BaseModel):
    """Sample model for testing."""

    id: str
    name: str


class TestSyncAPIClient:
    """Tests for SyncAPIClient."""

    # Retry logic tests (12 tests)

    def test_retry_on_429_rate_limit(self, base_sync_client, respx_mock, mock_oauth_token):
        """Test retry on 429 rate limit response."""
        # Mock OAuth token
        respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
            return_value=Response(200, json=mock_oauth_token)
        )

        # First request returns 429, second succeeds
        call_count = 0

        def handler(request):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return Response(429, json={"code": "RATE_LIMIT", "message": "Too many requests"})
            return Response(200, json={"code": "SUCCESS", "data": {"id": "123", "name": "Test"}})

        respx_mock.get("https://test.api.commerce.naver.com/external/v1/test").mock(side_effect=handler)

        with patch("time.sleep"):  # Mock sleep to speed up test
            result = base_sync_client.get("/v1/test", cast_to=dict)

        assert result["id"] == "123"
        assert call_count == 2

    def test_retry_on_500_server_error(self, base_sync_client, respx_mock, mock_oauth_token):
        """Test retry on 500 server error."""
        respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
            return_value=Response(200, json=mock_oauth_token)
        )

        call_count = 0

        def handler(request):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return Response(500, json={"code": "E500S00", "message": "Internal server error"})
            return Response(200, json={"code": "SUCCESS", "data": {"id": "123", "name": "Test"}})

        respx_mock.get("https://test.api.commerce.naver.com/external/v1/test").mock(side_effect=handler)

        with patch("time.sleep"):
            result = base_sync_client.get("/v1/test", cast_to=dict)

        assert result["id"] == "123"
        assert call_count == 2

    def test_retry_on_503_service_unavailable(self, base_sync_client, respx_mock, mock_oauth_token):
        """Test retry on 503 service unavailable."""
        respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
            return_value=Response(200, json=mock_oauth_token)
        )

        call_count = 0

        def handler(request):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return Response(503, json={"message": "Service unavailable"})
            return Response(200, json={"code": "SUCCESS", "data": {"id": "123", "name": "Test"}})

        respx_mock.get("https://test.api.commerce.naver.com/external/v1/test").mock(side_effect=handler)

        with patch("time.sleep"):
            result = base_sync_client.get("/v1/test", cast_to=dict)

        assert result["id"] == "123"
        assert call_count == 2

    def test_retry_on_401_with_token_refresh(self, base_sync_client, respx_mock, mock_oauth_token):
        """Test retry on 401 with token refresh."""
        token_call_count = 0

        def token_handler(request):
            nonlocal token_call_count
            token_call_count += 1
            return Response(200, json={"access_token": f"token_{token_call_count}", "expires_in": 3600, "token_type": "Bearer"})

        respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(side_effect=token_handler)

        call_count = 0

        def handler(request):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return Response(401, json={"code": "E401A01", "message": "Invalid access token"})
            return Response(200, json={"code": "SUCCESS", "data": {"id": "123", "name": "Test"}})

        respx_mock.get("https://test.api.commerce.naver.com/external/v1/test").mock(side_effect=handler)

        with patch("time.sleep"):
            result = base_sync_client.get("/v1/test", cast_to=dict)

        assert result["id"] == "123"
        assert call_count == 2
        assert token_call_count == 2  # First token + refresh

    def test_max_retries_exceeded(self, respx_mock, mock_oauth_token):
        """Test max retries exceeded raises error."""
        client = SyncAPIClient(
            client_id="test",
            client_secret="secret",
            base_url="https://test.api.commerce.naver.com/external",
            max_retries=2,
        )

        respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
            return_value=Response(200, json=mock_oauth_token)
        )

        respx_mock.get("https://test.api.commerce.naver.com/external/v1/test").mock(
            return_value=Response(500, json={"code": "E500S00", "message": "Server error"})
        )

        with patch("time.sleep"):
            with pytest.raises(InternalServerError) as exc_info:
                client.get("/v1/test", cast_to=dict)

        assert exc_info.value.status_code == 500

    def test_exponential_backoff_delay(self, base_sync_client):
        """Test exponential backoff delay calculation."""
        # Test delay calculation
        delay_0 = base_sync_client._calculate_retry_delay(0)
        delay_1 = base_sync_client._calculate_retry_delay(1)
        delay_2 = base_sync_client._calculate_retry_delay(2)
        delay_10 = base_sync_client._calculate_retry_delay(10)

        assert delay_0 == 0.5  # INITIAL_RETRY_DELAY
        assert delay_1 == 1.0  # 0.5 * 2^1
        assert delay_2 == 2.0  # 0.5 * 2^2
        assert delay_10 == 8.0  # Capped at MAX_RETRY_DELAY

    def test_should_retry_429(self, base_sync_client):
        """Test _should_retry returns True for 429."""
        response = Response(429, json={})
        assert base_sync_client._should_retry(response) is True

    def test_should_retry_500(self, base_sync_client):
        """Test _should_retry returns True for 5xx errors."""
        for status_code in [500, 502, 503, 504]:
            response = Response(status_code, json={})
            assert base_sync_client._should_retry(response) is True

    def test_should_retry_401(self, base_sync_client):
        """Test _should_retry returns True for 401."""
        response = Response(401, json={})
        assert base_sync_client._should_retry(response) is True

    def test_should_not_retry_400(self, base_sync_client):
        """Test _should_retry returns False for 400."""
        response = Response(400, json={})
        assert base_sync_client._should_retry(response) is False

    def test_should_not_retry_404(self, base_sync_client):
        """Test _should_retry returns False for 404."""
        response = Response(404, json={})
        assert base_sync_client._should_retry(response) is False

    def test_timeout_with_retry(self, base_sync_client, respx_mock, mock_oauth_token):
        """Test timeout error with retry."""
        respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
            return_value=Response(200, json=mock_oauth_token)
        )

        call_count = 0

        def handler(request):
            nonlocal call_count
            call_count += 1
            if call_count <= 2:
                raise httpx.TimeoutException("Timeout", request=request)
            return Response(200, json={"code": "SUCCESS", "data": {"id": "123"}})

        respx_mock.get("https://test.api.commerce.naver.com/external/v1/test").mock(side_effect=handler)

        with patch("time.sleep"):
            result = base_sync_client.get("/v1/test", cast_to=dict)

        assert result["id"] == "123"
        assert call_count == 3

    # Error handling tests (15 tests)

    def test_error_400_bad_request(self, base_sync_client, respx_mock, mock_oauth_token):
        """Test 400 Bad Request error."""
        respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
            return_value=Response(200, json=mock_oauth_token)
        )

        respx_mock.get("https://test.api.commerce.naver.com/external/v1/test").mock(
            return_value=Response(400, json={"code": "E400S00", "message": "Invalid parameter"})
        )

        with pytest.raises(BadRequestError) as exc_info:
            base_sync_client.get("/v1/test", cast_to=dict)

        assert exc_info.value.status_code == 400
        assert exc_info.value.code == "E400S00"

    def test_error_401_authentication(self, respx_mock, mock_oauth_token):
        """Test 401 Authentication error after all retries."""
        client = SyncAPIClient(
            client_id="test",
            client_secret="secret",
            base_url="https://test.api.commerce.naver.com/external",
            max_retries=1,
        )

        respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
            return_value=Response(200, json=mock_oauth_token)
        )

        respx_mock.get("https://test.api.commerce.naver.com/external/v1/test").mock(
            return_value=Response(401, json={"code": "E401A01", "message": "Invalid token"})
        )

        with patch("time.sleep"):
            with pytest.raises(AuthenticationError) as exc_info:
                client.get("/v1/test", cast_to=dict)

        assert exc_info.value.status_code == 401

    def test_error_403_permission_denied(self, base_sync_client, respx_mock, mock_oauth_token):
        """Test 403 Permission Denied error."""
        respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
            return_value=Response(200, json=mock_oauth_token)
        )

        respx_mock.get("https://test.api.commerce.naver.com/external/v1/test").mock(
            return_value=Response(403, json={"code": "E403A01", "message": "Forbidden"})
        )

        with pytest.raises(PermissionDeniedError) as exc_info:
            base_sync_client.get("/v1/test", cast_to=dict)

        assert exc_info.value.status_code == 403

    def test_error_404_not_found(self, base_sync_client, respx_mock, mock_oauth_token):
        """Test 404 Not Found error."""
        respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
            return_value=Response(200, json=mock_oauth_token)
        )

        respx_mock.get("https://test.api.commerce.naver.com/external/v1/test").mock(
            return_value=Response(404, json={"code": "E404S00", "message": "Not found"})
        )

        with pytest.raises(NotFoundError) as exc_info:
            base_sync_client.get("/v1/test", cast_to=dict)

        assert exc_info.value.status_code == 404

    def test_error_409_conflict(self, base_sync_client, respx_mock, mock_oauth_token):
        """Test 409 Conflict error."""
        respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
            return_value=Response(200, json=mock_oauth_token)
        )

        respx_mock.get("https://test.api.commerce.naver.com/external/v1/test").mock(
            return_value=Response(409, json={"code": "E409S00", "message": "Conflict"})
        )

        with pytest.raises(ConflictError) as exc_info:
            base_sync_client.get("/v1/test", cast_to=dict)

        assert exc_info.value.status_code == 409

    def test_error_500_internal_server(self, respx_mock, mock_oauth_token):
        """Test 500 Internal Server Error after all retries."""
        client = SyncAPIClient(
            client_id="test",
            client_secret="secret",
            base_url="https://test.api.commerce.naver.com/external",
            max_retries=1,
        )

        respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
            return_value=Response(200, json=mock_oauth_token)
        )

        respx_mock.get("https://test.api.commerce.naver.com/external/v1/test").mock(
            return_value=Response(500, json={"code": "E500S00", "message": "Server error"})
        )

        with patch("time.sleep"):
            with pytest.raises(InternalServerError) as exc_info:
                client.get("/v1/test", cast_to=dict)

        assert exc_info.value.status_code == 500

    def test_error_with_trace_id(self, base_sync_client, respx_mock, mock_oauth_token):
        """Test error response with trace_id."""
        respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
            return_value=Response(200, json=mock_oauth_token)
        )

        respx_mock.get("https://test.api.commerce.naver.com/external/v1/test").mock(
            return_value=Response(
                400,
                json={
                    "code": "E400S00",
                    "message": "Bad request",
                    "traceId": "abc-123-def",
                    "timestamp": "2024-01-01T00:00:00Z",
                },
            )
        )

        with pytest.raises(BadRequestError) as exc_info:
            base_sync_client.get("/v1/test", cast_to=dict)

        assert exc_info.value.trace_id == "abc-123-def"
        assert exc_info.value.timestamp == "2024-01-01T00:00:00Z"

    def test_error_with_invalid_inputs(self, base_sync_client, respx_mock, mock_oauth_token):
        """Test error response with invalid_inputs."""
        respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
            return_value=Response(200, json=mock_oauth_token)
        )

        respx_mock.get("https://test.api.commerce.naver.com/external/v1/test").mock(
            return_value=Response(
                400,
                json={
                    "code": "E400S00",
                    "message": "Validation failed",
                    "invalidInputs": [{"field": "name", "message": "Name is required"}],
                },
            )
        )

        with pytest.raises(BadRequestError) as exc_info:
            base_sync_client.get("/v1/test", cast_to=dict)

        assert len(exc_info.value.invalid_inputs) == 1
        assert exc_info.value.invalid_inputs[0]["field"] == "name"

    def test_error_code_to_exception_mapping(self, base_sync_client, respx_mock, mock_oauth_token):
        """Test error code takes precedence over status code."""
        respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
            return_value=Response(200, json=mock_oauth_token)
        )

        # 400 with NotFoundError code should raise NotFoundError, not BadRequestError
        respx_mock.get("https://test.api.commerce.naver.com/external/v1/test").mock(
            return_value=Response(400, json={"code": "E404S00", "message": "Not found"})
        )

        with pytest.raises(NotFoundError) as exc_info:
            base_sync_client.get("/v1/test", cast_to=dict)

        assert exc_info.value.status_code == 400  # HTTP status is still 400
        assert exc_info.value.code == "E404S00"  # But exception type is based on code

    def test_error_non_json_response(self, base_sync_client, respx_mock, mock_oauth_token):
        """Test error with non-JSON response body."""
        respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
            return_value=Response(200, json=mock_oauth_token)
        )

        respx_mock.get("https://test.api.commerce.naver.com/external/v1/test").mock(
            return_value=Response(500, text="Internal Server Error")
        )

        with pytest.raises(InternalServerError) as exc_info:
            base_sync_client.get("/v1/test", cast_to=dict)

        assert exc_info.value.status_code == 500
        assert exc_info.value.body is None

    def test_connection_error(self, base_sync_client, respx_mock, mock_oauth_token):
        """Test connection error."""
        respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
            return_value=Response(200, json=mock_oauth_token)
        )

        def handler(request):
            raise httpx.ConnectError("Connection failed", request=request)

        respx_mock.get("https://test.api.commerce.naver.com/external/v1/test").mock(side_effect=handler)

        with patch("time.sleep"):
            with pytest.raises(APIConnectionError) as exc_info:
                base_sync_client.get("/v1/test", cast_to=dict)

        assert "Connection error" in str(exc_info.value)

    def test_timeout_error(self, base_sync_client, respx_mock, mock_oauth_token):
        """Test timeout error after all retries."""
        respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
            return_value=Response(200, json=mock_oauth_token)
        )

        def handler(request):
            raise httpx.TimeoutException("Timeout", request=request)

        respx_mock.get("https://test.api.commerce.naver.com/external/v1/test").mock(side_effect=handler)

        with patch("time.sleep"):
            with pytest.raises(APITimeoutError):
                base_sync_client.get("/v1/test", cast_to=dict)

    def test_error_502_bad_gateway(self, respx_mock, mock_oauth_token):
        """Test 502 Bad Gateway error."""
        client = SyncAPIClient(
            client_id="test",
            client_secret="secret",
            base_url="https://test.api.commerce.naver.com/external",
            max_retries=1,
        )

        respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
            return_value=Response(200, json=mock_oauth_token)
        )

        respx_mock.get("https://test.api.commerce.naver.com/external/v1/test").mock(
            return_value=Response(502, json={"message": "Bad gateway"})
        )

        with patch("time.sleep"):
            with pytest.raises(InternalServerError) as exc_info:
                client.get("/v1/test", cast_to=dict)

        assert exc_info.value.status_code == 502

    def test_error_504_gateway_timeout(self, respx_mock, mock_oauth_token):
        """Test 504 Gateway Timeout error."""
        client = SyncAPIClient(
            client_id="test",
            client_secret="secret",
            base_url="https://test.api.commerce.naver.com/external",
            max_retries=1,
        )

        respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
            return_value=Response(200, json=mock_oauth_token)
        )

        respx_mock.get("https://test.api.commerce.naver.com/external/v1/test").mock(
            return_value=Response(504, json={"message": "Gateway timeout"})
        )

        with patch("time.sleep"):
            with pytest.raises(InternalServerError) as exc_info:
                client.get("/v1/test", cast_to=dict)

        assert exc_info.value.status_code == 504

    # Response parsing tests (8 tests)

    def test_parse_response_dict(self, base_sync_client, respx_mock, mock_oauth_token):
        """Test parsing response as dict."""
        respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
            return_value=Response(200, json=mock_oauth_token)
        )

        respx_mock.get("https://test.api.commerce.naver.com/external/v1/test").mock(
            return_value=Response(200, json={"code": "SUCCESS", "data": {"id": "123", "name": "Test"}})
        )

        result = base_sync_client.get("/v1/test", cast_to=dict)
        assert isinstance(result, dict)
        assert result["id"] == "123"

    def test_parse_response_list(self, base_sync_client, respx_mock, mock_oauth_token):
        """Test parsing response as list."""
        respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
            return_value=Response(200, json=mock_oauth_token)
        )

        respx_mock.get("https://test.api.commerce.naver.com/external/v1/test").mock(
            return_value=Response(200, json={"code": "SUCCESS", "data": [{"id": "1"}, {"id": "2"}]})
        )

        result = base_sync_client.get("/v1/test", cast_to=list)
        assert isinstance(result, list)
        assert len(result) == 2

    def test_parse_response_base_model(self, base_sync_client, respx_mock, mock_oauth_token):
        """Test parsing response as BaseModel."""
        respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
            return_value=Response(200, json=mock_oauth_token)
        )

        respx_mock.get("https://test.api.commerce.naver.com/external/v1/test").mock(
            return_value=Response(200, json={"code": "SUCCESS", "data": {"id": "123", "name": "Test"}})
        )

        result = base_sync_client.get("/v1/test", cast_to=SampleModel)
        assert isinstance(result, SampleModel)
        assert result.id == "123"

    def test_parse_response_wrapped_data(self, base_sync_client, respx_mock, mock_oauth_token):
        """Test parsing wrapped Naver API response."""
        respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
            return_value=Response(200, json=mock_oauth_token)
        )

        respx_mock.get("https://test.api.commerce.naver.com/external/v1/test").mock(
            return_value=Response(200, json={"code": "SUCCESS", "data": {"id": "123", "name": "Test"}})
        )

        result = base_sync_client.get("/v1/test", cast_to=dict)
        # Wrapped data should be unwrapped
        assert "code" not in result
        assert result["id"] == "123"

    def test_parse_response_already_unwrapped(self, base_sync_client, respx_mock, mock_oauth_token):
        """Test parsing already unwrapped response."""
        respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
            return_value=Response(200, json=mock_oauth_token)
        )

        respx_mock.get("https://test.api.commerce.naver.com/external/v1/test").mock(
            return_value=Response(200, json={"id": "123", "name": "Test"})
        )

        result = base_sync_client.get("/v1/test", cast_to=dict)
        assert result["id"] == "123"

    def test_parse_response_list_of_models(self, base_sync_client, respx_mock, mock_oauth_token):
        """Test parsing list of models."""
        respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
            return_value=Response(200, json=mock_oauth_token)
        )

        respx_mock.get("https://test.api.commerce.naver.com/external/v1/test").mock(
            return_value=Response(
                200,
                json={
                    "code": "SUCCESS",
                    "data": [
                        {"id": "1", "name": "First"},
                        {"id": "2", "name": "Second"},
                    ],
                },
            )
        )

        from typing import List

        result = base_sync_client.get("/v1/test", cast_to=List[SampleModel])  # type: ignore
        assert isinstance(result, list)
        assert len(result) == 2
        assert all(isinstance(item, SampleModel) for item in result)

    def test_parse_response_string(self, base_sync_client, respx_mock, mock_oauth_token):
        """Test parsing response as string."""
        respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
            return_value=Response(200, json=mock_oauth_token)
        )

        respx_mock.get("https://test.api.commerce.naver.com/external/v1/test").mock(
            return_value=Response(200, text="plain text response")
        )

        result = base_sync_client.get("/v1/test", cast_to=str)
        assert isinstance(result, str)
        assert result == "plain text response"

    def test_parse_response_none(self, base_sync_client, respx_mock, mock_oauth_token):
        """Test parsing response as None for empty responses."""
        respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
            return_value=Response(200, json=mock_oauth_token)
        )

        respx_mock.delete("https://test.api.commerce.naver.com/external/v1/test").mock(
            return_value=Response(204, content=b"")
        )

        result = base_sync_client.delete("/v1/test", cast_to=type(None))
        assert result is None

    # Request preparation tests (5 tests)

    def test_prepare_request_auth_header(self, base_sync_client, respx_mock, mock_oauth_token):
        """Test auth header is added to requests."""
        respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
            return_value=Response(200, json=mock_oauth_token)
        )

        request_headers = None

        def handler(request):
            nonlocal request_headers
            request_headers = dict(request.headers)
            return Response(200, json={"code": "SUCCESS", "data": {}})

        respx_mock.get("https://test.api.commerce.naver.com/external/v1/test").mock(side_effect=handler)

        base_sync_client.get("/v1/test", cast_to=dict)

        assert "authorization" in request_headers
        assert request_headers["authorization"] == f"Bearer {mock_oauth_token['access_token']}"

    def test_prepare_request_user_agent(self, base_sync_client, respx_mock, mock_oauth_token):
        """Test User-Agent header is added."""
        respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
            return_value=Response(200, json=mock_oauth_token)
        )

        request_headers = None

        def handler(request):
            nonlocal request_headers
            request_headers = dict(request.headers)
            return Response(200, json={"code": "SUCCESS", "data": {}})

        respx_mock.get("https://test.api.commerce.naver.com/external/v1/test").mock(side_effect=handler)

        base_sync_client.get("/v1/test", cast_to=dict)

        assert "user-agent" in request_headers
        assert "navercommerce-python" in request_headers["user-agent"]

    def test_prepare_request_custom_headers(self, base_sync_client, respx_mock, mock_oauth_token):
        """Test custom headers are merged."""
        respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
            return_value=Response(200, json=mock_oauth_token)
        )

        request_headers = None

        def handler(request):
            nonlocal request_headers
            request_headers = dict(request.headers)
            return Response(200, json={"code": "SUCCESS", "data": {}})

        respx_mock.get("https://test.api.commerce.naver.com/external/v1/test").mock(side_effect=handler)

        base_sync_client.get("/v1/test", cast_to=dict, headers={"X-Custom-Header": "test-value"})

        assert request_headers["x-custom-header"] == "test-value"
        assert "authorization" in request_headers  # Auth header still present

    def test_post_with_body(self, base_sync_client, respx_mock, mock_oauth_token):
        """Test POST request with JSON body."""
        respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
            return_value=Response(200, json=mock_oauth_token)
        )

        request_body = None

        def handler(request):
            nonlocal request_body
            request_body = request.content
            return Response(200, json={"code": "SUCCESS", "data": {"id": "123"}})

        respx_mock.post("https://test.api.commerce.naver.com/external/v1/test").mock(side_effect=handler)

        base_sync_client.post("/v1/test", cast_to=dict, body={"name": "Test Item", "price": 1000})

        assert request_body is not None
        import json

        body_dict = json.loads(request_body)
        assert body_dict["name"] == "Test Item"
        assert body_dict["price"] == 1000

    def test_get_with_params(self, base_sync_client, respx_mock, mock_oauth_token):
        """Test GET request with query parameters."""
        respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
            return_value=Response(200, json=mock_oauth_token)
        )

        request_url = None

        def handler(request):
            nonlocal request_url
            request_url = str(request.url)
            return Response(200, json={"code": "SUCCESS", "data": []})

        respx_mock.get("https://test.api.commerce.naver.com/external/v1/test").mock(side_effect=handler)

        base_sync_client.get("/v1/test", cast_to=list, params={"page": 1, "size": 10})

        assert "page=1" in request_url
        assert "size=10" in request_url
