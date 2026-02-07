Quick Start
===========

This guide shows you how to make your first API calls with the Naver Commerce SDK.

Synchronous Quick Start
------------------------

The simplest way to use the SDK is with the synchronous client:

.. code-block:: python

   from navercommerce import NaverCommerce

   # Initialize the client
   client = NaverCommerce(
       client_id="your_client_id",
       client_secret="your_client_secret"
   )

   # Get seller account information
   account = client.seller.account()
   print(f"Seller: {account.seller_name}")
   print(f"Seller ID: {account.seller_id}")

   # List sales channels
   channels = client.seller.channels()
   for channel in channels:
       print(f"Channel: {channel.channel_name}")
       print(f"Channel No: {channel.channel_no}")

Asynchronous Quick Start
-------------------------

For async applications, use the ``AsyncNaverCommerce`` client:

.. code-block:: python

   import asyncio
   from navercommerce import AsyncNaverCommerce

   async def main():
       # Use context manager for automatic cleanup
       async with AsyncNaverCommerce(
           client_id="your_client_id",
           client_secret="your_client_secret"
       ) as client:
           # Get seller account information
           account = await client.seller.account()
           print(f"Seller: {account.seller_name}")

           # List sales channels
           channels = await client.seller.channels()
           for channel in channels:
               print(f"Channel: {channel.channel_name}")

   # Run the async function
   asyncio.run(main())

.. tip::

   Always use the ``async with`` context manager with ``AsyncNaverCommerce`` to ensure proper cleanup of HTTP connections.

Working with Products
---------------------

Here's a complete example of creating and managing a product:

.. code-block:: python

   from navercommerce import NaverCommerce

   client = NaverCommerce()

   # Create a new product
   product = client.products.create(
       name="Sample Product",
       sale_price=29900,
       category_id="50000000",  # Electronics category
       origin_area_code="01",    # Korea
       stock_quantity=100,
       status="SALE"
   )
   print(f"Created product: {product.name} (ID: {product.id})")

   # Retrieve the product
   retrieved = client.products.retrieve(product.id)
   print(f"Product price: {retrieved.sale_price}원")

   # Update the product
   updated = client.products.update(
       product.id,
       name="Updated Product Name",
       sale_price=34900
   )
   print(f"Updated price: {updated.sale_price}원")

   # List all products (with pagination)
   products = client.products.list(page=1, size=20)
   for p in products:
       print(f"{p.name}: {p.sale_price}원")

Working with Orders
-------------------

Retrieve and manage orders:

.. code-block:: python

   from navercommerce import NaverCommerce

   client = NaverCommerce()

   # List orders by date range
   orders = client.orders.list(
       start_date="2024-01-01",
       end_date="2024-01-31"
   )

   for order in orders:
       print(f"Order ID: {order['productOrderId']}")
       print(f"Product: {order['productName']}")
       print(f"Status: {order['productOrderStatus']}")

   # Get detailed order information
   order_id = "2024010112345678"
   order_detail = client.orders.retrieve(order_id)
   print(f"Order date: {order_detail.order_date}")
   print(f"Total amount: {order_detail.total_amount}원")

   # Confirm orders
   result = client.orders.confirm(
       product_order_ids=[order_id]
   )
   print(f"Confirmed: {result}")

Error Handling Example
----------------------

Always handle potential errors in production code:

.. code-block:: python

   from navercommerce import (
       NaverCommerce,
       AuthenticationError,
       BadRequestError,
       NotFoundError,
       APIError
   )

   client = NaverCommerce()

   try:
       # Try to get a product
       product = client.products.retrieve("invalid_product_id")
   except AuthenticationError as e:
       print(f"Authentication failed: {e.message}")
       # Handle invalid credentials
   except NotFoundError as e:
       print(f"Product not found: {e.message}")
       # Handle missing resource
   except BadRequestError as e:
       print(f"Invalid request: {e.message}")
       if hasattr(e, 'invalid_inputs'):
           print(f"Invalid fields: {e.invalid_inputs}")
   except APIError as e:
       print(f"API error: {e.message}")
       # Handle other API errors

Async Error Handling
~~~~~~~~~~~~~~~~~~~~~

Error handling works the same way with async:

.. code-block:: python

   import asyncio
   from navercommerce import AsyncNaverCommerce, NotFoundError

   async def main():
       async with AsyncNaverCommerce() as client:
           try:
               product = await client.products.retrieve("invalid_id")
           except NotFoundError as e:
               print(f"Product not found: {e.message}")

   asyncio.run(main())

Using Configuration Options
----------------------------

Customize the client behavior with configuration options:

.. code-block:: python

   from navercommerce import NaverCommerce

   client = NaverCommerce(
       client_id="your_client_id",
       client_secret="your_client_secret",
       timeout=120,        # Request timeout in seconds
       max_retries=5,      # Maximum retry attempts
       base_url="https://api.commerce.naver.com"  # Custom base URL
   )

Context Managers
----------------

For better resource management, use context managers:

Synchronous:

.. code-block:: python

   from navercommerce import NaverCommerce

   with NaverCommerce() as client:
       account = client.seller.account()
       # Client is automatically closed when exiting the context

Asynchronous:

.. code-block:: python

   import asyncio
   from navercommerce import AsyncNaverCommerce

   async def main():
       async with AsyncNaverCommerce() as client:
           account = await client.seller.account()
           # Client is automatically closed when exiting the context

   asyncio.run(main())

Next Steps
----------

Now that you've made your first API calls, explore these resources:

- :doc:`../user-guide/index` - Learn core concepts and best practices
- :doc:`../resources/index` - Detailed guide for each resource
- :doc:`../examples/index` - More complete examples
- :doc:`../api-reference/index` - Full API reference documentation

Common Recipes
--------------

Batch Operations
~~~~~~~~~~~~~~~~

Process multiple items efficiently:

.. code-block:: python

   from navercommerce import NaverCommerce

   client = NaverCommerce()

   # Get all products across multiple pages
   all_products = []
   page = 1
   while True:
       products = client.products.list(page=page, size=100)
       if not products:
           break
       all_products.extend(products)
       page += 1

   print(f"Total products: {len(all_products)}")

Async Batch Operations
~~~~~~~~~~~~~~~~~~~~~~~

Use async for concurrent operations:

.. code-block:: python

   import asyncio
   from navercommerce import AsyncNaverCommerce

   async def get_multiple_products(client, product_ids):
       tasks = [client.products.retrieve(pid) for pid in product_ids]
       return await asyncio.gather(*tasks)

   async def main():
       async with AsyncNaverCommerce() as client:
           product_ids = ["id1", "id2", "id3"]
           products = await get_multiple_products(client, product_ids)
           for product in products:
               print(f"{product.name}: {product.sale_price}원")

   asyncio.run(main())

See Also
--------

- :doc:`../user-guide/sync-vs-async` - When to use sync vs async
- :doc:`../user-guide/error-handling` - Comprehensive error handling
- :doc:`../user-guide/best-practices` - Production tips and patterns
