"""
Async usage example for the Naver Commerce SDK.

This example demonstrates:
- Async client initialization
- Async API calls with asyncio
- Context manager usage for proper cleanup

Before running:
1. Set environment variables:
   export NAVER_CLIENT_ID="your_client_id"
   export NAVER_CLIENT_SECRET="your_client_secret"

2. Or pass credentials directly to the client
"""

import asyncio

from navercommerce import AsyncNaverCommerce


async def main():
    """Run async example."""
    print("=== Naver Commerce SDK Async Usage ===\n")

    # Initialize the async client using context manager
    # This ensures proper cleanup of resources
    async with AsyncNaverCommerce() as client:
        # Get seller account information
        print("1. Getting seller account information...")
        try:
            account = await client.seller.account()
            print(f"   Seller Name: {account.seller_name}")
            print(f"   Seller ID: {account.seller_id}")
            if account.email:
                print(f"   Email: {account.email}")
            print()
        except Exception as e:
            print(f"   Error: {e}\n")

        # Get sales channels
        print("2. Getting sales channels...")
        try:
            channels = await client.seller.channels()
            print(f"   Total channels: {len(channels)}")
            for channel in channels:
                default = " (default)" if channel.is_default else ""
                print(f"   - {channel.channel_name}{default}")
            print()
        except Exception as e:
            print(f"   Error: {e}\n")

        # Get address book
        print("3. Getting address book...")
        try:
            addresses = await client.seller.addresses()
            print(f"   Total addresses: {len(addresses)}")
            for address in addresses:
                default = " (default)" if address.is_default else ""
                print(f"   - {address.name}{default}")
                print(f"     Recipient: {address.recipient_name}")
                print(f"     Address: {address.address}")
                if address.address_detail:
                    print(f"     Detail: {address.address_detail}")
                print()
        except Exception as e:
            print(f"   Error: {e}\n")

        print("=== Example completed ===")


if __name__ == "__main__":
    asyncio.run(main())
