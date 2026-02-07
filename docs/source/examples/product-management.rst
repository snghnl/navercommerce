Product Management
==================

This example demonstrates complete product lifecycle management including creation, updates, and deletion.

Overview
--------

This example covers:

- Creating products with full details
- Retrieving product information
- Updating product attributes
- Deleting products
- Listing products with pagination
- Working with categories and brands

Complete Code
-------------

.. literalinclude:: ../../../examples/product_management.py
   :language: python
   :linenos:

Walkthrough
-----------

1. **Create a Product**

   Create a new product with all required fields:

   .. code-block:: python

      product = client.products.create(
          name="Sample Product",
          sale_price=29900,
          category_id="50000000",  # Electronics
          origin_area_code="01",    # Korea
          stock_quantity=100,
          status="SALE"
      )

2. **Retrieve Product**

   Get product details by ID:

   .. code-block:: python

      product = client.products.retrieve(product_id)
      print(f"Product: {product.name}")
      print(f"Price: {product.sale_price}원")

3. **Update Product**

   Modify product attributes:

   .. code-block:: python

      updated = client.products.update(
          product_id,
          name="Updated Product Name",
          sale_price=34900
      )

4. **List Products**

   Get all products with pagination:

   .. code-block:: python

      products = client.products.list(page=1, size=20)
      for product in products:
          print(f"{product.name}: {product.sale_price}원")

5. **Delete Product**

   Remove a product from catalog:

   .. code-block:: python

      client.products.delete(product_id)

Working with Categories
-----------------------

Browse and select product categories:

.. code-block:: python

   # List all categories
   categories = client.products.list_categories()

   # Get specific category
   category = client.products.get_category("50000000")
   print(f"Category: {category.name}")

Working with Brands
-------------------

Manage product brands:

.. code-block:: python

   # List brands
   brands = client.products.list_brands()
   for brand in brands:
       print(f"Brand: {brand.name}")

Running the Example
-------------------

1. Set credentials:

   .. code-block:: bash

      export NAVER_CLIENT_ID="your_client_id"
      export NAVER_CLIENT_SECRET="your_client_secret"

2. Run the script:

   .. code-block:: bash

      python examples/product_management.py

Expected Output
---------------

.. code-block:: text

   Creating product...
   Created: Sample Product (ID: prod_123)

   Retrieving product...
   Product: Sample Product
   Price: 29900원

   Updating product...
   Updated price: 34900원

   Listing products...
   Found 15 products

   Deleting product...
   Product deleted successfully

Error Handling
--------------

The example includes proper error handling:

.. code-block:: python

   try:
       product = client.products.retrieve("invalid_id")
   except NotFoundError:
       print("Product not found")
   except APIError as e:
       print(f"API error: {e.message}")

Related Examples
----------------

- :doc:`basic-usage` - Basic SDK usage
- :doc:`order-processing` - Processing orders

See Also
--------

- :doc:`../resources/products` - Products resource guide
- :doc:`../user-guide/error-handling` - Error handling patterns
