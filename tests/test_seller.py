"""Tests for the Seller resource."""

import pytest
from httpx import Response


def test_seller_account(client, respx_mock, mock_oauth_token, mock_account_response):
    """Test seller.account() method."""
    # Mock OAuth token
    respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
        return_value=Response(200, json=mock_oauth_token)
    )

    # Mock seller account endpoint
    respx_mock.get("https://test.api.commerce.naver.com/external/v1/seller/account").mock(
        return_value=Response(200, json=mock_account_response)
    )

    # Call the method
    account = client.seller.account()

    # Assertions
    assert account.seller_id == "seller123"
    assert account.seller_name == "Test Seller"
    assert account.email == "test@example.com"


def test_seller_channels(client, respx_mock, mock_oauth_token):
    """Test seller.channels() method."""
    # Mock OAuth token
    respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
        return_value=Response(200, json=mock_oauth_token)
    )

    # Mock channels response
    channels_response = {
        "code": "SUCCESS",
        "data": [
            {"channelNo": "ch1", "channelName": "Channel 1", "isDefault": True},
            {"channelNo": "ch2", "channelName": "Channel 2", "isDefault": False},
        ],
    }

    respx_mock.get("https://test.api.commerce.naver.com/external/v1/seller/channels").mock(
        return_value=Response(200, json=channels_response)
    )

    # Call the method
    channels = client.seller.channels()

    # Assertions
    assert len(channels) == 2
    assert channels[0].channel_no == "ch1"
    assert channels[0].is_default is True
    assert channels[1].channel_no == "ch2"
    assert channels[1].is_default is False


def test_seller_addresses(client, respx_mock, mock_oauth_token):
    """Test seller.addresses() method."""
    # Mock OAuth token
    respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
        return_value=Response(200, json=mock_oauth_token)
    )

    # Mock addresses response
    addresses_response = {
        "code": "SUCCESS",
        "data": [
            {
                "addressId": "addr1",
                "name": "Home",
                "recipientName": "John Doe",
                "zipCode": "12345",
                "address": "123 Main St",
                "addressDetail": "Apt 101",
                "isDefault": True,
            },
        ],
    }

    respx_mock.get("https://test.api.commerce.naver.com/external/v1/seller/addressbooks").mock(
        return_value=Response(200, json=addresses_response)
    )

    # Call the method
    addresses = client.seller.addresses()

    # Assertions
    assert len(addresses) == 1
    assert addresses[0].address_id == "addr1"
    assert addresses[0].name == "Home"
    assert addresses[0].is_default is True


@pytest.mark.asyncio
async def test_async_seller_account(async_client, respx_mock, mock_oauth_token, mock_account_response):
    """Test async seller.account() method."""
    # Mock OAuth token
    respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
        return_value=Response(200, json=mock_oauth_token)
    )

    # Mock seller account endpoint
    respx_mock.get("https://test.api.commerce.naver.com/external/v1/seller/account").mock(
        return_value=Response(200, json=mock_account_response)
    )

    # Call the method
    account = await async_client.seller.account()

    # Assertions
    assert account.seller_id == "seller123"
    assert account.seller_name == "Test Seller"
