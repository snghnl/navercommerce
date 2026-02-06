"""Pytest configuration and fixtures for Naver Commerce SDK tests."""

import pytest
import respx
from httpx import Request, Response

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


# Phase 1: Response testing fixtures


@pytest.fixture
def mock_httpx_response():
    """Mock httpx.Response for testing response wrappers."""
    return Response(
        200,
        json={"id": "test_id", "name": "test_name", "value": 123},
        headers={"content-type": "application/json"},
        request=Request("GET", "https://test.api.example.com/v1/test"),
    )


@pytest.fixture
def mock_wrapped_response():
    """Mock Naver API wrapped response format."""
    return Response(
        200,
        json={
            "code": "SUCCESS",
            "data": {
                "id": "prod123",
                "name": "Test Product",
                "status": "SALE",
            },
        },
        headers={"content-type": "application/json"},
        request=Request("GET", "https://test.api.example.com/v1/products/prod123"),
    )


# Phase 2: Base client testing fixtures


@pytest.fixture
def base_sync_client():
    """Create a SyncAPIClient instance for testing."""
    from navercommerce._base_client import SyncAPIClient

    return SyncAPIClient(
        client_id="test_client_id",
        client_secret="test_client_secret",
        base_url="https://test.api.commerce.naver.com/external",
        max_retries=3,
    )


@pytest.fixture
def base_async_client():
    """Create an AsyncAPIClient instance for testing."""
    from navercommerce._base_client import AsyncAPIClient

    return AsyncAPIClient(
        client_id="test_client_id",
        client_secret="test_client_secret",
        base_url="https://test.api.commerce.naver.com/external",
        max_retries=3,
    )


# Phase 3: Settlement testing fixtures


@pytest.fixture
def mock_settlement_commission_response():
    """Mock settlement commission details response."""
    return {
        "code": "SUCCESS",
        "data": {
            "elements": [
                {"orderId": "order1", "commission": 1000, "settlementAmount": 9000},
                {"orderId": "order2", "commission": 1500, "settlementAmount": 13500},
            ],
            "pagination": {
                "page": 0,
                "size": 100,
                "totalElements": 100,
                "totalPages": 1,
            },
        },
    }


@pytest.fixture
def mock_settlement_daily_response():
    """Mock daily settlement response."""
    return {
        "code": "SUCCESS",
        "data": {
            "elements": [
                {"settlementDate": "2024-01-01", "totalAmount": 50000},
                {"settlementDate": "2024-01-02", "totalAmount": 75000},
                {"settlementDate": "2024-01-03", "totalAmount": 60000},
            ],
            "pagination": {
                "page": 0,
                "size": 100,
                "totalElements": 31,
                "totalPages": 1,
            },
        },
    }


@pytest.fixture
def mock_settlement_vat_response():
    """Mock VAT settlement response."""
    return {
        "code": "SUCCESS",
        "data": {
            "elements": [
                {"date": "2024-01-01", "vatAmount": 5000},
                {"date": "2024-01-02", "vatAmount": 7500},
            ],
            "pagination": {
                "page": 0,
                "size": 100,
                "totalElements": 31,
                "totalPages": 1,
            },
        },
    }


@pytest.fixture
def mock_settlement_case_response():
    """Mock case settlement response."""
    return {
        "code": "SUCCESS",
        "data": {
            "elements": [
                {"caseNumber": "CASE001", "settlementAmount": 100000, "status": "COMPLETED"},
            ],
            "pagination": {
                "page": 0,
                "size": 100,
                "totalElements": 1,
                "totalPages": 1,
            },
        },
    }


# Phase 4: Inquiries testing fixtures


@pytest.fixture
def mock_qna_list_response():
    """Mock Q&A list response."""
    return {
        "code": "SUCCESS",
        "data": {
            "contents": [
                {
                    "questionId": "q1",
                    "questionContent": "What is the shipping time?",
                    "answerContent": "Ships within 24 hours",
                    "questionDate": "2024-01-01T10:00:00",
                },
                {
                    "questionId": "q2",
                    "questionContent": "What are the dimensions?",
                    "answerContent": None,
                    "questionDate": "2024-01-02T10:00:00",
                },
            ],
            "pagination": {
                "page": 0,
                "size": 10,
                "totalElements": 25,
                "totalPages": 3,
            },
        },
    }


@pytest.fixture
def mock_qna_template_response():
    """Mock Q&A template response."""
    return {
        "code": "SUCCESS",
        "data": {
            "templates": [
                {"templateId": "t1", "templateName": "Shipping Info", "content": "Ships within 24-48 hours"},
                {"templateId": "t2", "templateName": "Return Policy", "content": "30-day return policy"},
            ],
        },
    }


@pytest.fixture
def mock_answer_response():
    """Mock answer submission response."""
    return {
        "code": "SUCCESS",
        "data": {"questionId": "q123", "answered": True},
    }


@pytest.fixture
def mock_notice_list_response():
    """Mock notice list response."""
    return {
        "code": "SUCCESS",
        "data": {
            "contents": [
                {
                    "noticeId": "n1",
                    "noticeType": "EVENT",
                    "title": "Summer Sale",
                    "content": "50% off all items",
                    "createdDate": "2024-01-01T10:00:00",
                },
                {
                    "noticeId": "n2",
                    "noticeType": "NOTICE",
                    "title": "Holiday Hours",
                    "content": "Closed on New Year's Day",
                    "createdDate": "2024-01-02T10:00:00",
                },
            ],
            "pagination": {
                "page": 1,
                "size": 20,
                "totalElements": 50,
                "totalPages": 3,
            },
        },
    }


@pytest.fixture
def mock_notice_item_response():
    """Mock single notice response."""
    return {
        "code": "SUCCESS",
        "data": {
            "noticeId": "n123",
            "noticeType": "EVENT",
            "title": "Summer Sale",
            "content": "50% off all items",
            "createdDate": "2024-01-01T10:00:00",
        },
    }


@pytest.fixture
def mock_notice_create_response():
    """Mock notice creation response."""
    return {
        "code": "SUCCESS",
        "data": {"noticeId": "n456", "created": True},
    }


@pytest.fixture
def mock_notice_update_response():
    """Mock notice update response."""
    return {
        "code": "SUCCESS",
        "data": {"noticeId": "n123", "updated": True},
    }


@pytest.fixture
def mock_notice_delete_response():
    """Mock notice deletion response."""
    return {
        "code": "SUCCESS",
        "data": {"noticeId": "n123", "deleted": True},
    }
