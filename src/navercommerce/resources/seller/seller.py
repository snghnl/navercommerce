"""Seller resource implementation for the Naver Commerce SDK."""

from __future__ import annotations

from typing import TYPE_CHECKING, List

from ..._resource import AsyncAPIResource, SyncAPIResource
from ...types.seller import Account, Address, Channel

if TYPE_CHECKING:
    pass


class Seller(SyncAPIResource):
    """
    Seller resource for accessing seller account information.

    This resource provides access to:
    - Seller account details
    - Sales channels
    - Address book management
    """

    def account(self) -> Account:
        """
        Get seller account information.

        Returns:
            Account information including seller ID, name, and business details.

        Example:
            ```python
            account = client.seller.account()
            print(f"Seller: {account.seller_name}")
            print(f"Email: {account.email}")
            ```
        """
        return self._get(
            "/v1/seller/account",
            cast_to=Account,
        )

    def channels(self) -> List[Channel]:
        """
        Get list of sales channels.

        Returns:
            List of sales channels available to the seller.

        Example:
            ```python
            channels = client.seller.channels()
            for channel in channels:
                print(f"Channel: {channel.channel_name}")
            ```
        """
        return self._get(
            "/v1/seller/channels",
            cast_to=List[Channel],  # type: ignore
        )

    def addresses(self) -> List[Address]:
        """
        Get seller's address book.

        Returns:
            List of addresses from the seller's address book.

        Example:
            ```python
            addresses = client.seller.addresses()
            for address in addresses:
                print(f"Address: {address.name}")
                print(f"  Recipient: {address.recipient_name}")
                print(f"  Address: {address.address}")
            ```
        """
        return self._get(
            "/v1/seller/addressbooks",
            cast_to=List[Address],  # type: ignore
        )


class AsyncSeller(AsyncAPIResource):
    """
    Async seller resource for accessing seller account information.

    This resource provides async access to:
    - Seller account details
    - Sales channels
    - Address book management
    """

    async def account(self) -> Account:
        """
        Get seller account information.

        Returns:
            Account information including seller ID, name, and business details.

        Example:
            ```python
            account = await client.seller.account()
            print(f"Seller: {account.seller_name}")
            print(f"Email: {account.email}")
            ```
        """
        return await self._get(
            "/v1/seller/account",
            cast_to=Account,
        )

    async def channels(self) -> List[Channel]:
        """
        Get list of sales channels.

        Returns:
            List of sales channels available to the seller.

        Example:
            ```python
            channels = await client.seller.channels()
            for channel in channels:
                print(f"Channel: {channel.channel_name}")
            ```
        """
        return await self._get(
            "/v1/seller/channels",
            cast_to=List[Channel],  # type: ignore
        )

    async def addresses(self) -> List[Address]:
        """
        Get seller's address book.

        Returns:
            List of addresses from the seller's address book.

        Example:
            ```python
            addresses = await client.seller.addresses()
            for address in addresses:
                print(f"Address: {address.name}")
                print(f"  Recipient: {address.recipient_name}")
                print(f"  Address: {address.address}")
            ```
        """
        return await self._get(
            "/v1/seller/addressbooks",
            cast_to=List[Address],  # type: ignore
        )
