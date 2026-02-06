"""Tests for response wrapper classes."""

from __future__ import annotations

import pytest
from httpx import Headers, Request, Response, URL

from navercommerce._models import BaseModel
from navercommerce._response import APIResponse, AsyncAPIResponse


class SampleModel(BaseModel):
    """Sample model for testing."""

    id: str
    name: str
    value: int


class TestAPIResponse:
    """Tests for the sync APIResponse class."""

    def test_initialization(self, mock_httpx_response):
        """Test APIResponse initialization."""
        response = APIResponse(
            response=mock_httpx_response,
            cast_to=dict,
        )
        assert response._response == mock_httpx_response
        assert response._cast_to == dict
        assert response._parsed is None

    def test_initialization_with_parsed(self, mock_httpx_response):
        """Test APIResponse initialization with pre-parsed data."""
        parsed_data = {"id": "123", "name": "test"}
        response = APIResponse(
            response=mock_httpx_response,
            cast_to=dict,
            parsed=parsed_data,
        )
        assert response._parsed == parsed_data

    def test_http_response_property(self, mock_httpx_response):
        """Test http_response property returns raw httpx.Response."""
        response = APIResponse(response=mock_httpx_response, cast_to=dict)
        assert response.http_response == mock_httpx_response

    def test_status_code_property(self, mock_httpx_response):
        """Test status_code property."""
        response = APIResponse(response=mock_httpx_response, cast_to=dict)
        assert response.status_code == 200

    def test_headers_property(self, mock_httpx_response):
        """Test headers property."""
        response = APIResponse(response=mock_httpx_response, cast_to=dict)
        assert isinstance(response.headers, Headers)
        assert response.headers["content-type"] == "application/json"

    def test_content_property(self, mock_httpx_response):
        """Test content property returns raw bytes."""
        response = APIResponse(response=mock_httpx_response, cast_to=dict)
        assert isinstance(response.content, bytes)
        assert b"test_id" in response.content

    def test_text_property(self, mock_httpx_response):
        """Test text property returns string content."""
        response = APIResponse(response=mock_httpx_response, cast_to=dict)
        assert isinstance(response.text, str)
        assert "test_id" in response.text

    def test_url_property(self, mock_httpx_response):
        """Test url property."""
        response = APIResponse(response=mock_httpx_response, cast_to=dict)
        assert isinstance(response.url, URL)
        assert str(response.url) == "https://test.api.example.com/v1/test"

    def test_request_property(self, mock_httpx_response):
        """Test request property."""
        response = APIResponse(response=mock_httpx_response, cast_to=dict)
        assert isinstance(response.request, Request)

    def test_parse_dict(self, mock_httpx_response):
        """Test parsing response as dict."""
        response = APIResponse(response=mock_httpx_response, cast_to=dict)
        result = response.parse()
        assert isinstance(result, dict)
        assert result["id"] == "test_id"
        assert result["name"] == "test_name"

    def test_parse_base_model(self):
        """Test parsing response as BaseModel."""
        mock_response = Response(
            200,
            json={"id": "123", "name": "Test", "value": 42},
            request=Request("GET", "https://test.api.example.com/v1/test"),
        )
        response = APIResponse(response=mock_response, cast_to=SampleModel)
        result = response.parse()
        assert isinstance(result, SampleModel)
        assert result.id == "123"
        assert result.name == "Test"
        assert result.value == 42

    def test_parse_wrapped_response(self, mock_wrapped_response):
        """Test parsing Naver API wrapped response format."""
        response = APIResponse(response=mock_wrapped_response, cast_to=dict)
        result = response.parse()
        assert isinstance(result, dict)
        assert result["id"] == "prod123"
        assert result["name"] == "Test Product"
        assert "code" not in result  # Wrapper should be removed

    def test_parse_wrapped_response_with_base_model(self):
        """Test parsing wrapped response as BaseModel."""
        mock_response = Response(
            200,
            json={
                "code": "SUCCESS",
                "data": {"id": "123", "name": "Test", "value": 42},
            },
            request=Request("GET", "https://test.api.example.com/v1/test"),
        )
        response = APIResponse(response=mock_response, cast_to=SampleModel)
        result = response.parse()
        assert isinstance(result, SampleModel)
        assert result.id == "123"
        assert result.name == "Test"

    def test_parse_list_response(self):
        """Test parsing list response."""
        mock_response = Response(
            200,
            json=[{"id": "1", "name": "Item 1"}, {"id": "2", "name": "Item 2"}],
            request=Request("GET", "https://test.api.example.com/v1/test"),
        )
        response = APIResponse(response=mock_response, cast_to=list)
        result = response.parse()
        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0]["id"] == "1"

    def test_parse_caching(self, mock_httpx_response):
        """Test that parse() caches the result."""
        response = APIResponse(response=mock_httpx_response, cast_to=dict)
        result1 = response.parse()
        result2 = response.parse()
        assert result1 is result2  # Same object instance

    def test_json_method(self, mock_httpx_response):
        """Test json() method returns raw JSON data."""
        response = APIResponse(response=mock_httpx_response, cast_to=dict)
        result = response.json()
        assert isinstance(result, dict)
        assert result["id"] == "test_id"

    def test_repr(self, mock_httpx_response):
        """Test __repr__ method."""
        response = APIResponse(response=mock_httpx_response, cast_to=dict)
        repr_str = repr(response)
        assert "APIResponse" in repr_str
        assert "status_code=200" in repr_str
        assert "cast_to=dict" in repr_str
        assert "https://test.api.example.com/v1/test" in repr_str


class TestAsyncAPIResponse:
    """Tests for the async AsyncAPIResponse class."""

    def test_initialization(self, mock_httpx_response):
        """Test AsyncAPIResponse initialization."""
        response = AsyncAPIResponse(
            response=mock_httpx_response,
            cast_to=dict,
        )
        assert response._response == mock_httpx_response
        assert response._cast_to == dict
        assert response._parsed is None

    def test_initialization_with_parsed(self, mock_httpx_response):
        """Test AsyncAPIResponse initialization with pre-parsed data."""
        parsed_data = {"id": "123", "name": "test"}
        response = AsyncAPIResponse(
            response=mock_httpx_response,
            cast_to=dict,
            parsed=parsed_data,
        )
        assert response._parsed == parsed_data

    def test_http_response_property(self, mock_httpx_response):
        """Test http_response property returns raw httpx.Response."""
        response = AsyncAPIResponse(response=mock_httpx_response, cast_to=dict)
        assert response.http_response == mock_httpx_response

    def test_status_code_property(self, mock_httpx_response):
        """Test status_code property."""
        response = AsyncAPIResponse(response=mock_httpx_response, cast_to=dict)
        assert response.status_code == 200

    def test_headers_property(self, mock_httpx_response):
        """Test headers property."""
        response = AsyncAPIResponse(response=mock_httpx_response, cast_to=dict)
        assert isinstance(response.headers, Headers)
        assert response.headers["content-type"] == "application/json"

    def test_content_property(self, mock_httpx_response):
        """Test content property returns raw bytes."""
        response = AsyncAPIResponse(response=mock_httpx_response, cast_to=dict)
        assert isinstance(response.content, bytes)
        assert b"test_id" in response.content

    def test_text_property(self, mock_httpx_response):
        """Test text property returns string content."""
        response = AsyncAPIResponse(response=mock_httpx_response, cast_to=dict)
        assert isinstance(response.text, str)
        assert "test_id" in response.text

    def test_url_property(self, mock_httpx_response):
        """Test url property."""
        response = AsyncAPIResponse(response=mock_httpx_response, cast_to=dict)
        assert isinstance(response.url, URL)
        assert str(response.url) == "https://test.api.example.com/v1/test"

    def test_request_property(self, mock_httpx_response):
        """Test request property."""
        response = AsyncAPIResponse(response=mock_httpx_response, cast_to=dict)
        assert isinstance(response.request, Request)

    @pytest.mark.asyncio
    async def test_parse_dict(self, mock_httpx_response):
        """Test parsing response as dict."""
        response = AsyncAPIResponse(response=mock_httpx_response, cast_to=dict)
        result = await response.parse()
        assert isinstance(result, dict)
        assert result["id"] == "test_id"
        assert result["name"] == "test_name"

    @pytest.mark.asyncio
    async def test_parse_base_model(self):
        """Test parsing response as BaseModel."""
        mock_response = Response(
            200,
            json={"id": "123", "name": "Test", "value": 42},
            request=Request("GET", "https://test.api.example.com/v1/test"),
        )
        response = AsyncAPIResponse(response=mock_response, cast_to=SampleModel)
        result = await response.parse()
        assert isinstance(result, SampleModel)
        assert result.id == "123"
        assert result.name == "Test"
        assert result.value == 42

    @pytest.mark.asyncio
    async def test_parse_wrapped_response(self, mock_wrapped_response):
        """Test parsing Naver API wrapped response format."""
        response = AsyncAPIResponse(response=mock_wrapped_response, cast_to=dict)
        result = await response.parse()
        assert isinstance(result, dict)
        assert result["id"] == "prod123"
        assert result["name"] == "Test Product"
        assert "code" not in result  # Wrapper should be removed

    @pytest.mark.asyncio
    async def test_parse_wrapped_response_with_base_model(self):
        """Test parsing wrapped response as BaseModel."""
        mock_response = Response(
            200,
            json={
                "code": "SUCCESS",
                "data": {"id": "123", "name": "Test", "value": 42},
            },
            request=Request("GET", "https://test.api.example.com/v1/test"),
        )
        response = AsyncAPIResponse(response=mock_response, cast_to=SampleModel)
        result = await response.parse()
        assert isinstance(result, SampleModel)
        assert result.id == "123"
        assert result.name == "Test"

    @pytest.mark.asyncio
    async def test_parse_list_response(self):
        """Test parsing list response."""
        mock_response = Response(
            200,
            json=[{"id": "1", "name": "Item 1"}, {"id": "2", "name": "Item 2"}],
            request=Request("GET", "https://test.api.example.com/v1/test"),
        )
        response = AsyncAPIResponse(response=mock_response, cast_to=list)
        result = await response.parse()
        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0]["id"] == "1"

    @pytest.mark.asyncio
    async def test_parse_caching(self, mock_httpx_response):
        """Test that parse() caches the result."""
        response = AsyncAPIResponse(response=mock_httpx_response, cast_to=dict)
        result1 = await response.parse()
        result2 = await response.parse()
        assert result1 is result2  # Same object instance

    def test_json_method(self, mock_httpx_response):
        """Test json() method returns raw JSON data."""
        response = AsyncAPIResponse(response=mock_httpx_response, cast_to=dict)
        result = response.json()
        assert isinstance(result, dict)
        assert result["id"] == "test_id"

    def test_repr(self, mock_httpx_response):
        """Test __repr__ method."""
        response = AsyncAPIResponse(response=mock_httpx_response, cast_to=dict)
        repr_str = repr(response)
        assert "AsyncAPIResponse" in repr_str
        assert "status_code=200" in repr_str
        assert "cast_to=dict" in repr_str
        assert "https://test.api.example.com/v1/test" in repr_str
