"""Tests for the Products resource."""

import pytest
import respx
from httpx import Response


def test_products_create(client, respx_mock, mock_oauth_token, mock_product_response):
    """Test products.create() method."""
    # Mock OAuth token
    respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
        return_value=Response(200, json=mock_oauth_token)
    )

    # Mock create product endpoint
    respx_mock.post("https://test.api.commerce.naver.com/external/v2/products").mock(
        return_value=Response(200, json=mock_product_response)
    )

    # Call the method
    product = client.products.create(
        name="Test Product",
        sale_price=29900,
        category_id="50000000",
        origin_area_code="01",
    )

    # Assertions
    assert product.id == "prod123"
    assert product.name == "Test Product"
    assert product.sale_price == 29900


def test_products_retrieve(client, respx_mock, mock_oauth_token, mock_product_response):
    """Test products.retrieve() method."""
    # Mock OAuth token
    respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
        return_value=Response(200, json=mock_oauth_token)
    )

    # Mock retrieve product endpoint
    respx_mock.get("https://test.api.commerce.naver.com/external/v2/products/prod123").mock(
        return_value=Response(200, json=mock_product_response)
    )

    # Call the method
    product = client.products.retrieve("prod123")

    # Assertions
    assert product.id == "prod123"
    assert product.name == "Test Product"


def test_products_update(client, respx_mock, mock_oauth_token):
    """Test products.update() method."""
    # Mock OAuth token
    respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
        return_value=Response(200, json=mock_oauth_token)
    )

    # Mock update response
    updated_response = {
        "code": "SUCCESS",
        "data": {
            "id": "prod123",
            "name": "Updated Product",
            "status": "SALE",
            "salePrice": 34900,
        },
    }

    respx_mock.put("https://test.api.commerce.naver.com/external/v2/products/prod123").mock(
        return_value=Response(200, json=updated_response)
    )

    # Call the method
    product = client.products.update("prod123", name="Updated Product", sale_price=34900)

    # Assertions
    assert product.id == "prod123"
    assert product.name == "Updated Product"
    assert product.sale_price == 34900


def test_products_delete(client, respx_mock, mock_oauth_token):
    """Test products.delete() method."""
    # Mock OAuth token
    respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
        return_value=Response(200, json=mock_oauth_token)
    )

    # Mock delete endpoint (returns empty response)
    respx_mock.delete(
        "https://test.api.commerce.naver.com/external/v2/products/origin-products/prod123"
    ).mock(return_value=Response(204))

    # Call the method (should not raise)
    result = client.products.delete("prod123")
    assert result is None


def test_products_list(client, respx_mock, mock_oauth_token, mock_product_list_response):
    """Test products.list() method."""
    # Mock OAuth token
    respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
        return_value=Response(200, json=mock_oauth_token)
    )

    # Mock list endpoint
    respx_mock.get("https://test.api.commerce.naver.com/external/v2/products").mock(
        return_value=Response(200, json=mock_product_list_response)
    )

    # Call the method
    products = client.products.list(page=1, size=10)

    # Assertions
    assert len(products) == 2
    assert products[0].id == "prod1"
    assert products[1].id == "prod2"


def test_products_list_categories(client, respx_mock, mock_oauth_token, mock_category_list_response):
    """Test products.list_categories() method."""
    # Mock OAuth token
    respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
        return_value=Response(200, json=mock_oauth_token)
    )

    # Mock categories endpoint
    respx_mock.get("https://test.api.commerce.naver.com/external/v1/products/categories").mock(
        return_value=Response(200, json=mock_category_list_response)
    )

    # Call the method
    categories = client.products.list_categories()

    # Assertions
    assert len(categories) == 2
    assert categories[0].id == "50000000"
    assert categories[0].name == "Fashion"


def test_products_get_category(client, respx_mock, mock_oauth_token):
    """Test products.get_category() method."""
    # Mock OAuth token
    respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
        return_value=Response(200, json=mock_oauth_token)
    )

    # Mock category response
    category_response = {
        "code": "SUCCESS",
        "data": {
            "id": "50000000",
            "name": "Fashion",
            "wholeCategoryName": "Fashion > Clothing",
            "lastLevel": True,
        },
    }

    respx_mock.get("https://test.api.commerce.naver.com/external/v1/products/categories/50000000").mock(
        return_value=Response(200, json=category_response)
    )

    # Call the method
    category = client.products.get_category("50000000")

    # Assertions
    assert category.id == "50000000"
    assert category.name == "Fashion"


@pytest.mark.asyncio
async def test_async_products_create(async_client, respx_mock, mock_oauth_token, mock_product_response):
    """Test async products.create() method."""
    # Mock OAuth token
    respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
        return_value=Response(200, json=mock_oauth_token)
    )

    # Mock create product endpoint
    respx_mock.post("https://test.api.commerce.naver.com/external/v2/products").mock(
        return_value=Response(200, json=mock_product_response)
    )

    # Call the method
    product = await async_client.products.create(
        name="Test Product",
        sale_price=29900,
        category_id="50000000",
        origin_area_code="01",
    )

    # Assertions
    assert product.id == "prod123"
    assert product.name == "Test Product"
