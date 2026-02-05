"""Seller account types for the Naver Commerce SDK."""

from __future__ import annotations

from typing import List, Optional

from ..._models import BaseModel


class Account(BaseModel):
    """
    Seller account information.

    Attributes:
        seller_id: Unique seller identifier
        seller_name: Seller's business name
        tel_no: Seller's telephone number
        email: Seller's email address
        representative_name: Name of the business representative
        business_registration_no: Business registration number
    """

    seller_id: str
    seller_name: str
    tel_no: Optional[str] = None
    email: Optional[str] = None
    representative_name: Optional[str] = None
    business_registration_no: Optional[str] = None


class Channel(BaseModel):
    """
    Sales channel information.

    Attributes:
        channel_no: Unique channel identifier
        channel_name: Channel name
        is_default: Whether this is the default channel
    """

    channel_no: str
    channel_name: str
    is_default: bool = False
