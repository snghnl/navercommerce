"""
Order processing example for the Naver Commerce SDK.

This example demonstrates:
- Listing orders by date range
- Retrieving order details
- Confirming orders
- Shipping orders
- Canceling orders

Before running:
Set environment variables:
   export NAVER_CLIENT_ID="your_client_id"
   export NAVER_CLIENT_SECRET="your_client_secret"
"""

from datetime import datetime, timedelta

from navercommerce import NaverCommerce


def main():
    """Run order processing example."""
    client = NaverCommerce()

    print("=== Naver Commerce SDK Order Processing ===\n")

    # Calculate date range (last 30 days)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)

    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")

    # 1. List orders
    print(f"1. Listing orders from {start_date_str} to {end_date_str}...")
    try:
        orders = client.orders.list(
            start_date=start_date_str,
            end_date=end_date_str
        )
        print(f"   Found {len(orders)} orders")

        # Show first 5 orders
        for order in orders[:5]:
            print(f"\n   Order ID: {order.product_order_id}")
            print(f"   Product: {order.product_name}")
            print(f"   Quantity: {order.quantity}")
            print(f"   Price: {order.total_price}원")
            print(f"   Status: {order.order_status}")
            if order.shipping_info:
                print(f"   Shipping: {order.shipping_info.shipping_company}")

        # Get a sample order ID for next steps
        if orders:
            sample_order_id = orders[0].product_order_id
            print()

            # 2. Retrieve order details
            print(f"2. Retrieving details for order {sample_order_id}...")
            try:
                order_detail = client.orders.retrieve(sample_order_id)
                print(f"   Order ID: {order_detail.order_id}")
                print(f"   Order Date: {order_detail.order_date}")
                if order_detail.total_payment_amount:
                    print(f"   Total Amount: {order_detail.total_payment_amount}원")
                if order_detail.orderer:
                    print(f"   Orderer: {order_detail.orderer.name}")
                if order_detail.receiver:
                    print(f"   Receiver: {order_detail.receiver.name}")
                print()
            except Exception as e:
                print(f"   Error: {e}\n")

            # 3. Confirm orders (example - use with caution)
            print("3. Confirming orders...")
            print("   (Skipped in example - uncomment to actually confirm)")
            # Uncomment to actually confirm orders:
            # try:
            #     result = client.orders.confirm(
            #         product_order_ids=[sample_order_id]
            #     )
            #     print(f"   Confirmed: {result}")
            # except Exception as e:
            #     print(f"   Error: {e}")
            print()

            # 4. Ship orders (example - use with caution)
            print("4. Shipping orders...")
            print("   (Skipped in example - uncomment to actually ship)")
            # Uncomment to actually ship orders:
            # try:
            #     result = client.orders.ship(
            #         product_order_ids=[sample_order_id],
            #         shipping_company="CJ대한통운",
            #         tracking_number="123456789012",
            #         shipping_date=datetime.now().strftime("%Y-%m-%d")
            #     )
            #     print(f"   Shipped: {result}")
            # except Exception as e:
            #     print(f"   Error: {e}")
            print()

            # 5. Cancel orders (example - use with caution)
            print("5. Canceling orders...")
            print("   (Skipped in example - uncomment to actually cancel)")
            # Uncomment to actually cancel orders:
            # try:
            #     result = client.orders.cancel(
            #         product_order_ids=[sample_order_id],
            #         cancel_reason="Customer request"
            #     )
            #     print(f"   Canceled: {result}")
            # except Exception as e:
            #     print(f"   Error: {e}")
            print()

    except Exception as e:
        print(f"   Error listing orders: {e}\n")

    # Example: Filter by order status
    print("6. Filtering orders by status...")
    print("   (This shows how to use the order status enum)")
    try:
        all_orders = client.orders.list(
            start_date=start_date_str,
            end_date=end_date_str
        )

        # Count orders by status
        from collections import Counter
        status_counts = Counter(order.order_status.value for order in all_orders)

        print("   Order status breakdown:")
        for status, count in status_counts.items():
            print(f"   - {status}: {count} orders")
        print()

    except Exception as e:
        print(f"   Error: {e}\n")

    print("=== Example completed ===")
    print("\nNote: Order confirmation, shipping, and cancellation are commented out")
    print("to prevent accidental modifications. Uncomment to use in production.")


if __name__ == "__main__":
    main()
