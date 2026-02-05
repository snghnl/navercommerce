"""Seller address types for the Naver Commerce SDK."""

from __future__ import annotations

from typing import Optional

from pydantic import Field

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

    address_id: str = Field(alias="addressId")
    name: str
    recipient_name: str = Field(alias="recipientName")
    tel_no: Optional[str] = Field(None, alias="telNo")
    mobile_no: Optional[str] = Field(None, alias="mobileNo")
    zip_code: str = Field(alias="zipCode")
    address: str
    address_detail: Optional[str] = Field(None, alias="addressDetail")
    is_default: bool = Field(False, alias="isDefault")


class AddressBook(BaseModel):
    """
    Collection of addresses in the seller's address book.

    Attributes:
        addresses: List of addresses
        total_count: Total number of addresses
    """

    addresses: list[Address]
    total_count: int
