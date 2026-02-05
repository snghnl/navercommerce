"""
Basic usage example for the Naver Commerce SDK.

This example demonstrates:
- Client initialization
- Getting seller account information
- Listing channels
- Getting address book

Before running:
1. Set environment variables:
   export NAVER_CLIENT_ID="your_client_id"
   export NAVER_CLIENT_SECRET="your_client_secret"

2. Or pass credentials directly to the client:
   client = NaverCommerce(
       client_id="your_client_id",
       client_secret="your_client_secret"
   )
"""

from navercommerce import NaverCommerce


def main():
    """Run basic example."""
    # Initialize the client
    # Credentials will be read from environment variables:
    # - NAVER_CLIENT_ID
    # - NAVER_CLIENT_SECRET
    client = NaverCommerce()

    print("=== Naver Commerce SDK Basic Usage ===\n")

    # Get seller account information
    print("1. Getting seller account information...")
    try:
        account = client.seller.account()
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
        channels = client.seller.channels()
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
        addresses = client.seller.addresses()
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
    main()
