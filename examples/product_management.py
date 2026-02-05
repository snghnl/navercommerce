"""
Product management example for the Naver Commerce SDK.

This example demonstrates:
- Creating products
- Retrieving products
- Updating products
- Listing products with pagination
- Browsing categories and brands
- Deleting products

Before running:
Set environment variables:
   export NAVER_CLIENT_ID="your_client_id"
   export NAVER_CLIENT_SECRET="your_client_secret"
"""

from navercommerce import NaverCommerce


def main():
    """Run product management example."""
    client = NaverCommerce()

    print("=== Naver Commerce SDK Product Management ===\n")

    # 1. List categories
    print("1. Listing product categories...")
    try:
        categories = client.products.list_categories()
        print(f"   Total categories: {len(categories)}")
        for category in categories[:5]:  # Show first 5
            print(f"   - {category.name} (ID: {category.id})")
        print()
    except Exception as e:
        print(f"   Error: {e}\n")

    # 2. List brands
    print("2. Listing brands...")
    try:
        brands = client.products.list_brands(page=1, size=10)
        print(f"   Total brands: {len(brands)}")
        for brand in brands[:5]:  # Show first 5
            print(f"   - {brand.name} (ID: {brand.id})")
        print()
    except Exception as e:
        print(f"   Error: {e}\n")

    # 3. Create a product
    print("3. Creating a new product...")
    try:
        product = client.products.create(
            name="SDK Test Product",
            sale_price=29900,
            category_id="50000000",  # Replace with actual category ID
            origin_area_code="01",  # Korea
            stock_quantity=100,
            status="SALE",
            detail_content="<p>This is a test product created by the SDK</p>",
        )
        print(f"   Created product: {product.name}")
        print(f"   Product ID: {product.id}")
        print(f"   Price: {product.sale_price}원")
        print()

        product_id = product.id

        # 4. Retrieve the product
        print("4. Retrieving the product...")
        try:
            retrieved_product = client.products.retrieve(product_id)
            print(f"   Retrieved: {retrieved_product.name}")
            print(f"   Status: {retrieved_product.status}")
            print(f"   Stock: {retrieved_product.stock_quantity}")
            print()
        except Exception as e:
            print(f"   Error: {e}\n")

        # 5. Update the product
        print("5. Updating the product...")
        try:
            updated_product = client.products.update(
                product_id,
                name="SDK Test Product (Updated)",
                sale_price=34900,
                stock_quantity=150,
            )
            print(f"   Updated: {updated_product.name}")
            print(f"   New price: {updated_product.sale_price}원")
            print()
        except Exception as e:
            print(f"   Error: {e}\n")

        # 6. List products
        print("6. Listing products...")
        try:
            products = client.products.list(page=1, size=5)
            print(f"   Found {len(products)} products")
            for p in products:
                print(f"   - {p.name}: {p.sale_price}원 (Status: {p.status})")
            print()
        except Exception as e:
            print(f"   Error: {e}\n")

        # 7. Delete the product
        print("7. Deleting the test product...")
        try:
            client.products.delete(product_id)
            print("   Product deleted successfully")
            print()
        except Exception as e:
            print(f"   Error: {e}\n")

    except Exception as e:
        print(f"   Error creating product: {e}\n")

    print("=== Example completed ===")


if __name__ == "__main__":
    main()
