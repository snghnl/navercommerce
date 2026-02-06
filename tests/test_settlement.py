"""Tests for the Settlement resource."""

import pytest
from httpx import Response


def test_get_commission_details_basic(client, respx_mock, mock_oauth_token, mock_settlement_commission_response):
    """Test get_commission_details() basic call."""
    respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
        return_value=Response(200, json=mock_oauth_token)
    )

    respx_mock.get("https://test.api.commerce.naver.com/external/v1/pay-settle/settle/commission-details").mock(
        return_value=Response(200, json=mock_settlement_commission_response)
    )

    result = client.settlement.get_commission_details(
        start_date="2024-01-01",
        end_date="2024-01-31",
    )

    assert result.pagination is not None
    assert result.pagination.total_elements == 100
    assert len(result.elements) == 2


def test_get_commission_details_with_pagination(client, respx_mock, mock_oauth_token, mock_settlement_commission_response):
    """Test get_commission_details() with pagination."""
    respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
        return_value=Response(200, json=mock_oauth_token)
    )

    request_params = None

    def handler(request):
        nonlocal request_params
        request_params = dict(request.url.params)
        return Response(200, json=mock_settlement_commission_response)

    respx_mock.get("https://test.api.commerce.naver.com/external/v1/pay-settle/settle/commission-details").mock(side_effect=handler)

    client.settlement.get_commission_details(
        start_date="2024-01-01",
        end_date="2024-01-31",
        page=1,
        size=50,
    )

    assert request_params["page"] == "1"
    assert request_params["size"] == "50"


def test_get_daily_settlement_basic(client, respx_mock, mock_oauth_token, mock_settlement_daily_response):
    """Test get_daily_settlement() basic call."""
    respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
        return_value=Response(200, json=mock_oauth_token)
    )

    respx_mock.get("https://test.api.commerce.naver.com/external/v1/pay-settle/settle/daily").mock(
        return_value=Response(200, json=mock_settlement_daily_response)
    )

    result = client.settlement.get_daily_settlement(
        start_date="2024-01-01",
        end_date="2024-01-31",
    )

    assert len(result.elements) == 3


def test_get_daily_settlement_with_params(client, respx_mock, mock_oauth_token, mock_settlement_daily_response):
    """Test get_daily_settlement() with params."""
    respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
        return_value=Response(200, json=mock_oauth_token)
    )

    request_params = None

    def handler(request):
        nonlocal request_params
        request_params = dict(request.url.params)
        return Response(200, json=mock_settlement_daily_response)

    respx_mock.get("https://test.api.commerce.naver.com/external/v1/pay-settle/settle/daily").mock(side_effect=handler)

    client.settlement.get_daily_settlement(
        start_date="2024-01-01",
        end_date="2024-01-31",
        page=0,
        size=100,
    )

    assert request_params["startDate"] == "2024-01-01"
    assert request_params["endDate"] == "2024-01-31"
    assert request_params["page"] == "0"
    assert request_params["size"] == "100"


def test_get_vat_daily_basic(client, respx_mock, mock_oauth_token, mock_settlement_vat_response):
    """Test get_vat_daily() basic call."""
    respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
        return_value=Response(200, json=mock_oauth_token)
    )

    respx_mock.get("https://test.api.commerce.naver.com/external/v1/pay-settle/vat/daily").mock(
        return_value=Response(200, json=mock_settlement_vat_response)
    )

    result = client.settlement.get_vat_daily(
        start_date="2024-01-01",
        end_date="2024-01-31",
    )

    assert len(result.elements) == 2


def test_get_vat_daily_date_range(client, respx_mock, mock_oauth_token, mock_settlement_vat_response):
    """Test get_vat_daily() with specific date range."""
    respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
        return_value=Response(200, json=mock_oauth_token)
    )

    request_params = None

    def handler(request):
        nonlocal request_params
        request_params = dict(request.url.params)
        return Response(200, json=mock_settlement_vat_response)

    respx_mock.get("https://test.api.commerce.naver.com/external/v1/pay-settle/vat/daily").mock(side_effect=handler)

    client.settlement.get_vat_daily(
        start_date="2024-02-01",
        end_date="2024-02-29",
    )

    assert request_params["startDate"] == "2024-02-01"
    assert request_params["endDate"] == "2024-02-29"


def test_get_case_settlement_basic(client, respx_mock, mock_oauth_token, mock_settlement_case_response):
    """Test get_case_settlement() basic call."""
    respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
        return_value=Response(200, json=mock_oauth_token)
    )

    respx_mock.get("https://test.api.commerce.naver.com/external/v1/pay-settle/settle/case").mock(
        return_value=Response(200, json=mock_settlement_case_response)
    )

    result = client.settlement.get_case_settlement(
        start_date="2024-01-01",
        end_date="2024-01-31",
    )

    assert len(result.elements) == 1


def test_get_case_settlement_with_filters(client, respx_mock, mock_oauth_token, mock_settlement_case_response):
    """Test get_case_settlement() with filters."""
    respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
        return_value=Response(200, json=mock_oauth_token)
    )

    request_params = None

    def handler(request):
        nonlocal request_params
        request_params = dict(request.url.params)
        return Response(200, json=mock_settlement_case_response)

    respx_mock.get("https://test.api.commerce.naver.com/external/v1/pay-settle/settle/case").mock(side_effect=handler)

    client.settlement.get_case_settlement(
        start_date="2024-01-01",
        end_date="2024-01-31",
        page=2,
        size=20,
    )

    assert "page" in request_params
    assert "size" in request_params


def test_get_vat_case_basic(client, respx_mock, mock_oauth_token, mock_settlement_vat_response):
    """Test get_vat_case() basic call."""
    respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
        return_value=Response(200, json=mock_oauth_token)
    )

    respx_mock.get("https://test.api.commerce.naver.com/external/v1/pay-settle/vat/case").mock(
        return_value=Response(200, json=mock_settlement_vat_response)
    )

    result = client.settlement.get_vat_case(
        start_date="2024-01-01",
        end_date="2024-01-31",
    )

    assert len(result.elements) == 2


def test_get_vat_case_with_pagination(client, respx_mock, mock_oauth_token, mock_settlement_vat_response):
    """Test get_vat_case() with pagination."""
    respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
        return_value=Response(200, json=mock_oauth_token)
    )

    request_params = None

    def handler(request):
        nonlocal request_params
        request_params = dict(request.url.params)
        return Response(200, json=mock_settlement_vat_response)

    respx_mock.get("https://test.api.commerce.naver.com/external/v1/pay-settle/vat/case").mock(side_effect=handler)

    client.settlement.get_vat_case(
        start_date="2024-01-01",
        end_date="2024-01-31",
        page=3,
        size=25,
    )

    assert request_params["page"] == "3"
    assert request_params["size"] == "25"


# Bug fix verification test
def test_get_vat_case_bug_fix_params_not_kwargs(client, respx_mock, mock_oauth_token, mock_settlement_vat_response):
    """Test bug fix: get_vat_case uses params not kwargs."""
    respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
        return_value=Response(200, json=mock_oauth_token)
    )

    request_params = None

    def handler(request):
        nonlocal request_params
        request_params = dict(request.url.params)
        return Response(200, json=mock_settlement_vat_response)

    respx_mock.get("https://test.api.commerce.naver.com/external/v1/pay-settle/vat/case").mock(side_effect=handler)

    # Call with both pagination and extra kwargs
    client.settlement.get_vat_case(
        start_date="2024-01-01",
        end_date="2024-01-31",
        page=1,
        size=10,
        custom_param="value",
    )

    # Verify all params are passed correctly
    assert request_params["startDate"] == "2024-01-01"
    assert request_params["endDate"] == "2024-01-31"
    assert request_params["page"] == "1"  # Should be from params, not kwargs
    assert request_params["size"] == "10"  # Should be from params, not kwargs
    assert request_params["custom_param"] == "value"  # kwargs should still work


# Async tests
@pytest.mark.asyncio
async def test_async_get_commission_details(async_client, respx_mock, mock_oauth_token, mock_settlement_commission_response):
    """Test async get_commission_details()."""
    respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
        return_value=Response(200, json=mock_oauth_token)
    )

    respx_mock.get("https://test.api.commerce.naver.com/external/v1/pay-settle/settle/commission-details").mock(
        return_value=Response(200, json=mock_settlement_commission_response)
    )

    result = await async_client.settlement.get_commission_details(
        start_date="2024-01-01",
        end_date="2024-01-31",
    )

    assert len(result.elements) == 2


@pytest.mark.asyncio
async def test_async_get_daily_settlement(async_client, respx_mock, mock_oauth_token, mock_settlement_daily_response):
    """Test async get_daily_settlement()."""
    respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
        return_value=Response(200, json=mock_oauth_token)
    )

    respx_mock.get("https://test.api.commerce.naver.com/external/v1/pay-settle/settle/daily").mock(
        return_value=Response(200, json=mock_settlement_daily_response)
    )

    result = await async_client.settlement.get_daily_settlement(
        start_date="2024-01-01",
        end_date="2024-01-31",
    )

    assert len(result.elements) == 3


@pytest.mark.asyncio
async def test_async_get_vat_daily(async_client, respx_mock, mock_oauth_token, mock_settlement_vat_response):
    """Test async get_vat_daily()."""
    respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
        return_value=Response(200, json=mock_oauth_token)
    )

    respx_mock.get("https://test.api.commerce.naver.com/external/v1/pay-settle/vat/daily").mock(
        return_value=Response(200, json=mock_settlement_vat_response)
    )

    result = await async_client.settlement.get_vat_daily(
        start_date="2024-01-01",
        end_date="2024-01-31",
    )

    assert len(result.elements) == 2


@pytest.mark.asyncio
async def test_async_get_case_settlement(async_client, respx_mock, mock_oauth_token, mock_settlement_case_response):
    """Test async get_case_settlement()."""
    respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
        return_value=Response(200, json=mock_oauth_token)
    )

    respx_mock.get("https://test.api.commerce.naver.com/external/v1/pay-settle/settle/case").mock(
        return_value=Response(200, json=mock_settlement_case_response)
    )

    result = await async_client.settlement.get_case_settlement(
        start_date="2024-01-01",
        end_date="2024-01-31",
    )

    assert len(result.elements) == 1


@pytest.mark.asyncio
async def test_async_get_vat_case(async_client, respx_mock, mock_oauth_token, mock_settlement_vat_response):
    """Test async get_vat_case()."""
    respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
        return_value=Response(200, json=mock_oauth_token)
    )

    respx_mock.get("https://test.api.commerce.naver.com/external/v1/pay-settle/vat/case").mock(
        return_value=Response(200, json=mock_settlement_vat_response)
    )

    result = await async_client.settlement.get_vat_case(
        start_date="2024-01-01",
        end_date="2024-01-31",
    )

    assert len(result.elements) == 2


@pytest.mark.asyncio
async def test_async_get_vat_case_bug_fix(async_client, respx_mock, mock_oauth_token, mock_settlement_vat_response):
    """Test async bug fix verification."""
    respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
        return_value=Response(200, json=mock_oauth_token)
    )

    request_params = None

    def handler(request):
        nonlocal request_params
        request_params = dict(request.url.params)
        return Response(200, json=mock_settlement_vat_response)

    respx_mock.get("https://test.api.commerce.naver.com/external/v1/pay-settle/vat/case").mock(side_effect=handler)

    await async_client.settlement.get_vat_case(
        start_date="2024-01-01",
        end_date="2024-01-31",
        page=1,
        size=10,
    )

    # Verify pagination params are correctly passed
    assert request_params["page"] == "1"
    assert request_params["size"] == "10"


# Edge case tests
def test_empty_response_handling(client, respx_mock, mock_oauth_token):
    """Test handling of empty settlement response."""
    respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
        return_value=Response(200, json=mock_oauth_token)
    )

    empty_response = {
        "code": "SUCCESS",
        "data": {
            "elements": [],
            "pagination": {"page": 0, "size": 100, "totalElements": 0, "totalPages": 0},
        },
    }

    respx_mock.get("https://test.api.commerce.naver.com/external/v1/pay-settle/settle/commission-details").mock(
        return_value=Response(200, json=empty_response)
    )

    result = client.settlement.get_commission_details(
        start_date="2024-01-01",
        end_date="2024-01-31",
    )

    assert len(result.elements) == 0
    assert result.pagination.total_elements == 0


def test_pagination_info_parsing(client, respx_mock, mock_oauth_token, mock_settlement_commission_response):
    """Test pagination info is correctly parsed."""
    respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
        return_value=Response(200, json=mock_oauth_token)
    )

    respx_mock.get("https://test.api.commerce.naver.com/external/v1/pay-settle/settle/commission-details").mock(
        return_value=Response(200, json=mock_settlement_commission_response)
    )

    result = client.settlement.get_commission_details(
        start_date="2024-01-01",
        end_date="2024-01-31",
    )

    assert result.pagination.page == 0
    assert result.pagination.size == 100
    assert result.pagination.total_elements == 100
    assert result.pagination.total_pages == 1


def test_date_format_validation(client, respx_mock, mock_oauth_token, mock_settlement_daily_response):
    """Test date parameters are passed in correct format."""
    respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
        return_value=Response(200, json=mock_oauth_token)
    )

    request_params = None

    def handler(request):
        nonlocal request_params
        request_params = dict(request.url.params)
        return Response(200, json=mock_settlement_daily_response)

    respx_mock.get("https://test.api.commerce.naver.com/external/v1/pay-settle/settle/daily").mock(side_effect=handler)

    client.settlement.get_daily_settlement(
        start_date="2024-12-01",
        end_date="2024-12-31",
    )

    # Verify date format is preserved
    assert request_params["startDate"] == "2024-12-01"
    assert request_params["endDate"] == "2024-12-31"
