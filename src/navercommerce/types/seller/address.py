"""Seller address types for the Naver Commerce SDK."""

from __future__ import annotations

from typing import Optional

from ..._models import BaseModel


class Address(BaseModel):
    """
    Address information.

    Attributes:
        address_id: Unique address identifier
        name: Address name/label
        recipient_name: Name of the recipient
        tel_no: Telephone number
        mobile_no: Mobile phone number
        zip_code: Postal/ZIP code
        address: Street address
        address_detail: Detailed address (apartment number, etc.)
        is_default: Whether this is the default address
    """

    address_id: str
    name: str
    recipient_name: str
    tel_no: Optional[str] = None
    mobile_no: Optional[str] = None
    zip_code: str
    address: str
    address_detail: Optional[str] = None
    is_default: bool = False


class AddressBook(BaseModel):
    """
    Collection of addresses in the seller's address book.

    Attributes:
        addresses: List of addresses
        total_count: Total number of addresses
    """

    addresses: list[Address]
    total_count: int
