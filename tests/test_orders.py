"""Tests for the Orders resource."""

import pytest
from httpx import Response


def test_orders_list(client, respx_mock, mock_oauth_token, mock_order_list_response):
    """Test orders.list() method."""
    # Mock OAuth token
    respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
        return_value=Response(200, json=mock_oauth_token)
    )

    # Mock list orders endpoint (correct endpoint)
    respx_mock.post("https://test.api.commerce.naver.com/external/v1/pay-order/seller/product-orders/query").mock(
        return_value=Response(200, json=mock_order_list_response)
    )

    # Call the method
    orders = client.orders.list(start_date="2024-01-01", end_date="2024-01-31")

    # Assertions
    assert len(orders) == 2
    assert orders[0].product_order_id == "2024010112345678"
    assert orders[0].product_name == "Test Product 1"
    assert orders[1].product_order_id == "2024010112345679"


def test_orders_retrieve(client, respx_mock, mock_oauth_token):
    """Test orders.retrieve() method."""
    # Mock OAuth token
    respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
        return_value=Response(200, json=mock_oauth_token)
    )

    # Mock retrieve order response - retrieve returns OrderProductInfo
    order_response = {
        "code": "SUCCESS",
        "data": [
            {
                "productOrderId": "2024010112345678",
                "orderId": "order123",
                "productId": "prod123",
                "productName": "Test Product",
                "quantity": 1,
                "unitPrice": 29900,
                "totalPrice": 29900,
                "productOrderStatus": "PAYED",
            }
        ],
    }

    respx_mock.post("https://test.api.commerce.naver.com/external/v1/pay-order/seller/product-orders/query").mock(
        return_value=Response(200, json=order_response)
    )

    # Call the method
    order = client.orders.retrieve("2024010112345678")

    # Assertions - order is OrderProductInfo
    assert order.product_order_id == "2024010112345678"
    assert order.order_id == "order123"
    assert order.product_name == "Test Product"


def test_orders_confirm(client, respx_mock, mock_oauth_token):
    """Test orders.confirm() method."""
    # Mock OAuth token
    respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
        return_value=Response(200, json=mock_oauth_token)
    )

    # Mock confirm response
    confirm_response = {
        "code": "SUCCESS",
        "data": {"successCount": 2, "failedCount": 0},
    }

    respx_mock.post("https://test.api.commerce.naver.com/external/v1/pay-order/seller/product-orders/confirm").mock(
        return_value=Response(200, json=confirm_response)
    )

    # Call the method
    result = client.orders.confirm(product_order_ids=["order1", "order2"])

    # Assertions (result is dict since we don't have a specific type)
    assert result is not None


def test_orders_ship(client, respx_mock, mock_oauth_token):
    """Test orders.ship() method."""
    # Mock OAuth token
    respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
        return_value=Response(200, json=mock_oauth_token)
    )

    # Mock ship response
    ship_response = {
        "code": "SUCCESS",
        "data": {"successCount": 1, "failedCount": 0},
    }

    respx_mock.post("https://test.api.commerce.naver.com/external/v1/pay-order/seller/product-orders/dispatch").mock(
        return_value=Response(200, json=ship_response)
    )

    # Call the method
    result = client.orders.ship(
        product_order_ids=["order1"],
        shipping_company="CJ대한통운",
        tracking_number="123456789012",
    )

    # Assertions
    assert result is not None


def test_orders_cancel(client, respx_mock, mock_oauth_token):
    """Test orders.cancel() method."""
    # Mock OAuth token
    respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
        return_value=Response(200, json=mock_oauth_token)
    )

    # Mock cancel response
    cancel_response = {
        "code": "SUCCESS",
        "data": {"successCount": 1, "failedCount": 0},
    }

    respx_mock.post("https://test.api.commerce.naver.com/external/v1/pay-order/seller/product-orders/order1/claim/cancel/request").mock(
        return_value=Response(200, json=cancel_response)
    )

    # Call the method
    result = client.orders.cancel(product_order_ids=["order1"], cancel_reason="Out of stock")

    # Assertions
    assert result is not None


@pytest.mark.asyncio
async def test_async_orders_list(async_client, respx_mock, mock_oauth_token, mock_order_list_response):
    """Test async orders.list() method."""
    # Mock OAuth token
    respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
        return_value=Response(200, json=mock_oauth_token)
    )

    # Mock list orders endpoint (correct endpoint)
    respx_mock.post("https://test.api.commerce.naver.com/external/v1/pay-order/seller/product-orders/query").mock(
        return_value=Response(200, json=mock_order_list_response)
    )

    # Call the method
    orders = await async_client.orders.list(start_date="2024-01-01", end_date="2024-01-31")

    # Assertions
    assert len(orders) == 2
    assert orders[0].product_order_id == "2024010112345678"
