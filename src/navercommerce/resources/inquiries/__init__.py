"""Inquiries resource for the Naver Commerce SDK."""

from .inquiries import AsyncInquiries, Inquiries
from .qnas import AsyncQnas, Qnas
from .notices import AsyncNotices, Notices

__all__ = [
    "Inquiries",
    "AsyncInquiries",
    "Qnas",
    "AsyncQnas",
    "Notices",
    "AsyncNotices",
]
