"""Tests for the Inquiries resource."""

import pytest
from httpx import Response


# Q&A tests
def test_qnas_list_basic(client, respx_mock, mock_oauth_token, mock_qna_list_response):
    """Test qnas.list() basic call."""
    respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
        return_value=Response(200, json=mock_oauth_token)
    )

    respx_mock.get("https://test.api.commerce.naver.com/external/v1/contents/qnas").mock(
        return_value=Response(200, json=mock_qna_list_response)
    )

    result = client.inquiries.qnas.list()

    assert len(result.contents) == 2
    assert result.contents[0].question_id == "q1"
    assert result.contents[1].question_id == "q2"


def test_qnas_list_with_pagination(client, respx_mock, mock_oauth_token, mock_qna_list_response):
    """Test qnas.list() with pagination."""
    respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
        return_value=Response(200, json=mock_oauth_token)
    )

    respx_mock.get("https://test.api.commerce.naver.com/external/v1/contents/qnas").mock(
        return_value=Response(200, json=mock_qna_list_response)
    )

    result = client.inquiries.qnas.list(page=0, size=10)

    # Check pagination info (stored as extra fields due to model_config)
    assert hasattr(result, 'pagination')
    assert result.pagination['page'] == 0
    assert result.pagination['size'] == 10


def test_qnas_list_empty(client, respx_mock, mock_oauth_token):
    """Test qnas.list() with empty results."""
    respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
        return_value=Response(200, json=mock_oauth_token)
    )

    empty_response = {
        "code": "SUCCESS",
        "data": {
            "contents": [],
            "pagination": {"page": 0, "size": 10, "totalElements": 0, "totalPages": 0},
        },
    }

    respx_mock.get("https://test.api.commerce.naver.com/external/v1/contents/qnas").mock(
        return_value=Response(200, json=empty_response)
    )

    result = client.inquiries.qnas.list()

    assert len(result.contents) == 0
    assert result.pagination['totalElements'] == 0


def test_qnas_answer(client, respx_mock, mock_oauth_token, mock_answer_response):
    """Test qnas.answer() method."""
    respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
        return_value=Response(200, json=mock_oauth_token)
    )

    respx_mock.put("https://test.api.commerce.naver.com/external/v1/contents/qnas/q123").mock(
        return_value=Response(200, json=mock_answer_response)
    )

    result = client.inquiries.qnas.answer(
        question_id="q123",
        answer_content="Thank you for your question.",
    )

    assert result is not None
    # Response is unwrapped, so we get the data directly
    assert result.get("questionId") == "q123"
    assert result.get("answered") is True


def test_qnas_answer_with_template(client, respx_mock, mock_oauth_token, mock_answer_response):
    """Test qnas.answer() with template."""
    respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
        return_value=Response(200, json=mock_oauth_token)
    )

    request_body = None

    def handler(request):
        nonlocal request_body
        import json
        request_body = json.loads(request.content)
        return Response(200, json=mock_answer_response)

    respx_mock.put("https://test.api.commerce.naver.com/external/v1/contents/qnas/q123").mock(side_effect=handler)

    client.inquiries.qnas.answer(
        question_id="q123",
        answer_content="Standard answer",
        template_id="template_1",
    )

    assert request_body["answerContent"] == "Standard answer"
    assert request_body["template_id"] == "template_1"


def test_qnas_list_templates(client, respx_mock, mock_oauth_token, mock_qna_template_response):
    """Test qnas.list_templates() method."""
    respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
        return_value=Response(200, json=mock_oauth_token)
    )

    respx_mock.get("https://test.api.commerce.naver.com/external/v1/contents/qnas/templates").mock(
        return_value=Response(200, json=mock_qna_template_response)
    )

    result = client.inquiries.qnas.list_templates()

    assert len(result.templates) == 2
    assert result.templates[0].template_name == "Shipping Info"


# Notices tests
def test_notices_create(client, respx_mock, mock_oauth_token, mock_notice_create_response):
    """Test notices.create() method."""
    respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
        return_value=Response(200, json=mock_oauth_token)
    )

    respx_mock.post("https://test.api.commerce.naver.com/external/v1/contents/seller-notices").mock(
        return_value=Response(200, json=mock_notice_create_response)
    )

    result = client.inquiries.notices.create(
        notice_type="EVENT",
        title="New Product Launch",
        content="Exciting new product coming soon!",
    )

    assert result.get("noticeId") == "n456"
    assert result.get("created") is True


def test_notices_list(client, respx_mock, mock_oauth_token, mock_notice_list_response):
    """Test notices.list() method."""
    respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
        return_value=Response(200, json=mock_oauth_token)
    )

    respx_mock.get("https://test.api.commerce.naver.com/external/v1/contents/seller-notices").mock(
        return_value=Response(200, json=mock_notice_list_response)
    )

    result = client.inquiries.notices.list()

    assert len(result.contents) == 2
    assert result.contents[0].title == "Summer Sale"


def test_notices_list_with_pagination(client, respx_mock, mock_oauth_token, mock_notice_list_response):
    """Test notices.list() with pagination."""
    respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
        return_value=Response(200, json=mock_oauth_token)
    )

    respx_mock.get("https://test.api.commerce.naver.com/external/v1/contents/seller-notices").mock(
        return_value=Response(200, json=mock_notice_list_response)
    )

    result = client.inquiries.notices.list(page=1, size=20)

    # Check pagination info (stored as extra fields)
    assert hasattr(result, 'pagination')
    assert result.pagination['page'] == 1
    assert result.pagination['size'] == 20


def test_notices_retrieve(client, respx_mock, mock_oauth_token, mock_notice_item_response):
    """Test notices.retrieve() method."""
    respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
        return_value=Response(200, json=mock_oauth_token)
    )

    respx_mock.get("https://test.api.commerce.naver.com/external/v1/contents/seller-notices/n123").mock(
        return_value=Response(200, json=mock_notice_item_response)
    )

    result = client.inquiries.notices.retrieve("n123")

    assert result.notice_id == "n123"
    assert result.title == "Summer Sale"


def test_notices_update(client, respx_mock, mock_oauth_token, mock_notice_update_response):
    """Test notices.update() method."""
    respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
        return_value=Response(200, json=mock_oauth_token)
    )

    respx_mock.put("https://test.api.commerce.naver.com/external/v1/contents/seller-notices/n123").mock(
        return_value=Response(200, json=mock_notice_update_response)
    )

    result = client.inquiries.notices.update(
        notice_id="n123",
        title="Updated Title",
        content="Updated content",
    )

    assert result.get("noticeId") == "n123"
    assert result.get("updated") is True


def test_notices_delete(client, respx_mock, mock_oauth_token, mock_notice_delete_response):
    """Test notices.delete() method."""
    respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
        return_value=Response(200, json=mock_oauth_token)
    )

    respx_mock.delete("https://test.api.commerce.naver.com/external/v1/contents/seller-notices/n123").mock(
        return_value=Response(200, json=mock_notice_delete_response)
    )

    result = client.inquiries.notices.delete("n123")

    assert result.get("noticeId") == "n123"
    assert result.get("deleted") is True


# Async tests
@pytest.mark.asyncio
async def test_async_qnas_list(async_client, respx_mock, mock_oauth_token, mock_qna_list_response):
    """Test async qnas.list()."""
    respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
        return_value=Response(200, json=mock_oauth_token)
    )

    respx_mock.get("https://test.api.commerce.naver.com/external/v1/contents/qnas").mock(
        return_value=Response(200, json=mock_qna_list_response)
    )

    result = await async_client.inquiries.qnas.list()

    assert len(result.contents) == 2


@pytest.mark.asyncio
async def test_async_qnas_answer(async_client, respx_mock, mock_oauth_token, mock_answer_response):
    """Test async qnas.answer()."""
    respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
        return_value=Response(200, json=mock_oauth_token)
    )

    respx_mock.put("https://test.api.commerce.naver.com/external/v1/contents/qnas/q123").mock(
        return_value=Response(200, json=mock_answer_response)
    )

    result = await async_client.inquiries.qnas.answer(
        question_id="q123",
        answer_content="Thank you",
    )

    assert result.get("questionId") == "q123"
    assert result.get("answered") is True


@pytest.mark.asyncio
async def test_async_qnas_list_templates(async_client, respx_mock, mock_oauth_token, mock_qna_template_response):
    """Test async qnas.list_templates()."""
    respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
        return_value=Response(200, json=mock_oauth_token)
    )

    respx_mock.get("https://test.api.commerce.naver.com/external/v1/contents/qnas/templates").mock(
        return_value=Response(200, json=mock_qna_template_response)
    )

    result = await async_client.inquiries.qnas.list_templates()

    assert len(result.templates) == 2


@pytest.mark.asyncio
async def test_async_notices_create(async_client, respx_mock, mock_oauth_token, mock_notice_create_response):
    """Test async notices.create()."""
    respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
        return_value=Response(200, json=mock_oauth_token)
    )

    respx_mock.post("https://test.api.commerce.naver.com/external/v1/contents/seller-notices").mock(
        return_value=Response(200, json=mock_notice_create_response)
    )

    result = await async_client.inquiries.notices.create(
        notice_type="EVENT",
        title="New Event",
        content="Event details",
    )

    assert result.get("noticeId") == "n456"
    assert result.get("created") is True


@pytest.mark.asyncio
async def test_async_notices_list(async_client, respx_mock, mock_oauth_token, mock_notice_list_response):
    """Test async notices.list()."""
    respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
        return_value=Response(200, json=mock_oauth_token)
    )

    respx_mock.get("https://test.api.commerce.naver.com/external/v1/contents/seller-notices").mock(
        return_value=Response(200, json=mock_notice_list_response)
    )

    result = await async_client.inquiries.notices.list()

    assert len(result.contents) == 2


@pytest.mark.asyncio
async def test_async_notices_retrieve(async_client, respx_mock, mock_oauth_token, mock_notice_item_response):
    """Test async notices.retrieve()."""
    respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
        return_value=Response(200, json=mock_oauth_token)
    )

    respx_mock.get("https://test.api.commerce.naver.com/external/v1/contents/seller-notices/n123").mock(
        return_value=Response(200, json=mock_notice_item_response)
    )

    result = await async_client.inquiries.notices.retrieve("n123")

    assert result.notice_id == "n123"


@pytest.mark.asyncio
async def test_async_notices_update(async_client, respx_mock, mock_oauth_token, mock_notice_update_response):
    """Test async notices.update()."""
    respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
        return_value=Response(200, json=mock_oauth_token)
    )

    respx_mock.put("https://test.api.commerce.naver.com/external/v1/contents/seller-notices/n123").mock(
        return_value=Response(200, json=mock_notice_update_response)
    )

    result = await async_client.inquiries.notices.update(
        notice_id="n123",
        title="Updated",
    )

    assert result.get("noticeId") == "n123"
    assert result.get("updated") is True


@pytest.mark.asyncio
async def test_async_notices_delete(async_client, respx_mock, mock_oauth_token, mock_notice_delete_response):
    """Test async notices.delete()."""
    respx_mock.post("https://test.api.commerce.naver.com/external/v1/oauth2/token").mock(
        return_value=Response(200, json=mock_oauth_token)
    )

    respx_mock.delete("https://test.api.commerce.naver.com/external/v1/contents/seller-notices/n123").mock(
        return_value=Response(200, json=mock_notice_delete_response)
    )

    result = await async_client.inquiries.notices.delete("n123")

    assert result.get("noticeId") == "n123"
    assert result.get("deleted") is True


# Integration tests
def test_inquiries_has_qnas_subresource(client):
    """Test that inquiries resource has qnas sub-resource."""
    assert hasattr(client.inquiries, "qnas")
    assert client.inquiries.qnas is not None


def test_inquiries_has_notices_subresource(client):
    """Test that inquiries resource has notices sub-resource."""
    assert hasattr(client.inquiries, "notices")
    assert client.inquiries.notices is not None


def test_inquiries_subresources_are_cached(client):
    """Test that sub-resources use cached_property."""
    # Access twice, should be same instance
    qnas1 = client.inquiries.qnas
    qnas2 = client.inquiries.qnas
    assert qnas1 is qnas2

    notices1 = client.inquiries.notices
    notices2 = client.inquiries.notices
    assert notices1 is notices2
