"""Inquiries resource for the Naver Commerce SDK."""

from .inquiries import AsyncInquiries, Inquiries
from .notices import AsyncNotices, Notices
from .qnas import AsyncQnas, Qnas

__all__ = [
    "Inquiries",
    "AsyncInquiries",
    "Qnas",
    "AsyncQnas",
    "Notices",
    "AsyncNotices",
]
