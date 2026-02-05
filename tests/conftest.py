"""Pytest configuration and fixtures for Naver Commerce SDK tests."""

import pytest
import respx
from httpx import Response

from navercommerce import AsyncNaverCommerce, NaverCommerce


@pytest.fixture
def client():
    """Create a test client instance."""
    return NaverCommerce(
        client_id="test_client_id",
        client_secret="test_client_secret",
        base_url="https://test.api.commerce.naver.com/external",
    )


@pytest.fixture
def async_client():
    """Create an async test client instance."""
    return AsyncNaverCommerce(
        client_id="test_client_id",
        client_secret="test_client_secret",
        base_url="https://test.api.commerce.naver.com/external",
    )


@pytest.fixture
def mock_oauth_token():
    """Mock OAuth token response."""
    return {
        "access_token": "test_access_token_12345",
        "expires_in": 10800,
        "token_type": "Bearer",
    }


@pytest.fixture
def mock_account_response():
    """Mock seller account response."""
    return {
        "code": "SUCCESS",
        "data": {
            "sellerId": "seller123",
            "sellerName": "Test Seller",
            "telNo": "02-1234-5678",
            "email": "test@example.com",
            "representativeName": "John Doe",
            "businessRegistrationNo": "123-45-67890",
        },
    }


@pytest.fixture
def mock_product_response():
    """Mock product response."""
    return {
        "code": "SUCCESS",
        "data": {
            "id": "prod123",
            "name": "Test Product",
            "status": "SALE",
            "salePrice": 29900,
            "stockQuantity": 100,
            "categoryId": "50000000",
            "categoryName": "Fashion",
            "originAreaCode": "01",
        },
    }


@pytest.fixture
def mock_product_list_response():
    """Mock product list response."""
    return {
        "code": "SUCCESS",
        "data": [
            {
                "id": "prod1",
                "name": "Product 1",
                "status": "SALE",
                "salePrice": 10000,
            },
            {
                "id": "prod2",
                "name": "Product 2",
                "status": "SALE",
                "salePrice": 20000,
            },
        ],
    }


@pytest.fixture
def mock_order_response():
    """Mock order response."""
    return {
        "code": "SUCCESS",
        "data": {
            "productOrderId": "2024010112345678",
            "orderId": "order123",
            "productId": "prod123",
            "productName": "Test Product",
            "quantity": 1,
            "unitPrice": 29900,
            "totalPrice": 29900,
            "productOrderStatus": "PAYED",
            "orderDate": "2024-01-01T10:00:00",
        },
    }


@pytest.fixture
def mock_order_list_response():
    """Mock order list response."""
    return {
        "code": "SUCCESS",
        "data": [
            {
                "productOrderId": "2024010112345678",
                "orderId": "order123",
                "productId": "prod123",
                "productName": "Test Product 1",
                "quantity": 1,
                "unitPrice": 10000,
                "totalPrice": 10000,
                "productOrderStatus": "PAYED",
            },
            {
                "productOrderId": "2024010112345679",
                "orderId": "order124",
                "productId": "prod124",
                "productName": "Test Product 2",
                "quantity": 2,
                "unitPrice": 15000,
                "totalPrice": 30000,
                "productOrderStatus": "DELIVERING",
            },
        ],
    }


@pytest.fixture
def mock_category_list_response():
    """Mock category list response."""
    return {
        "code": "SUCCESS",
        "data": [
            {
                "id": "50000000",
                "name": "Fashion",
                "wholeCategoryName": "Fashion",
                "lastLevel": False,
            },
            {
                "id": "50000001",
                "name": "Electronics",
                "wholeCategoryName": "Electronics",
                "lastLevel": False,
            },
        ],
    }


@pytest.fixture
def respx_mock():
    """Create a respx mock context."""
    with respx.mock:
        yield respx


def mock_api_response(respx_mock, method: str, path: str, response_data: dict):
    """Helper to mock API responses."""
    route = getattr(respx_mock, method.lower())(path)
    route.mock(return_value=Response(200, json=response_data))
    return route
