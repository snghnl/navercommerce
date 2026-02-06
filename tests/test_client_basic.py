"""Basic tests for client initialization."""

import pytest

from navercommerce import AsyncNaverCommerce, NaverCommerce


def test_import():
    """Test that we can import the main client classes."""
    assert NaverCommerce is not None
    assert AsyncNaverCommerce is not None


def test_client_requires_credentials():
    """Test that client initialization requires credentials."""
    with pytest.raises(ValueError, match="Client ID is required"):
        NaverCommerce()


def test_client_initialization():
    """Test that client can be initialized with credentials."""
    client = NaverCommerce(
        client_id="test_client_id",
        client_secret="test_client_secret",
    )
    assert client is not None


def test_client_has_resources():
    """Test that client has the expected resource properties."""
    client = NaverCommerce(
        client_id="test_client_id",
        client_secret="test_client_secret",
    )

    # These should be accessible without errors
    assert hasattr(client, "seller")
    assert hasattr(client, "products")
    assert hasattr(client, "orders")


def test_async_client_initialization():
    """Test that async client can be initialized with credentials."""
    client = AsyncNaverCommerce(
        client_id="test_client_id",
        client_secret="test_client_secret",
    )
    assert client is not None


def test_async_client_has_resources():
    """Test that async client has the expected resource properties."""
    client = AsyncNaverCommerce(
        client_id="test_client_id",
        client_secret="test_client_secret",
    )

    # These should be accessible without errors
    assert hasattr(client, "seller")
    assert hasattr(client, "products")
    assert hasattr(client, "orders")
