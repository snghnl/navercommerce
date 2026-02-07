Synchronous vs Asynchronous
===========================

The Naver Commerce SDK provides both synchronous and asynchronous clients. This guide helps you choose the right one for your use case.

Quick Comparison
----------------

=======================  ========================  ===========================
Feature                  Synchronous               Asynchronous
=======================  ========================  ===========================
**Class**                ``NaverCommerce``         ``AsyncNaverCommerce``
**Import**               ``from navercommerce``    ``from navercommerce``
**Calling methods**      ``client.method()``       ``await client.method()``
**Concurrency**          Threading                 asyncio
**Blocking**             Yes                       No
**Use case**             Scripts, simple apps      Web servers, high concurrency
=======================  ========================  ===========================

When to Use Synchronous
-----------------------

Use ``NaverCommerce`` (synchronous) when:

✅ **Writing Scripts**: One-off data migration, reporting, or admin tools

.. code-block:: python

   # Perfect for scripts
   from navercommerce import NaverCommerce

   client = NaverCommerce()
   account = client.seller.account()
   print(f"Seller: {account.seller_name}")

✅ **Simple Applications**: Small apps without concurrency requirements

✅ **Sequential Processing**: Operations must happen in order

.. code-block:: python

   # Process orders sequentially
   orders = client.orders.list(start_date="2024-01-01")
   for order in orders:
       client.orders.confirm([order.product_order_id])

✅ **Existing Sync Codebase**: Already using synchronous libraries (Flask, Django without async)

✅ **Easier Debugging**: Simpler stack traces and debugging experience

When to Use Asynchronous
-------------------------

Use ``AsyncNaverCommerce`` (asynchronous) when:

✅ **High Concurrency**: Need to handle many requests simultaneously

.. code-block:: python

   # Fetch 100 products concurrently
   import asyncio
   from navercommerce import AsyncNaverCommerce

   async def get_products(product_ids):
       async with AsyncNaverCommerce() as client:
           tasks = [client.products.retrieve(pid) for pid in product_ids]
           return await asyncio.gather(*tasks)

   asyncio.run(get_products(product_ids))

✅ **Async Web Frameworks**: Using FastAPI, aiohttp, Starlette, Quart, etc.

.. code-block:: python

   from fastapi import FastAPI
   from navercommerce import AsyncNaverCommerce

   app = FastAPI()
   client = AsyncNaverCommerce()

   @app.get("/seller")
   async def get_seller():
       account = await client.seller.account()
       return {"seller": account.seller_name}

✅ **I/O-Bound Workloads**: Lots of API calls with waiting time

✅ **Performance Critical**: Need maximum throughput with limited resources

✅ **Existing Async Codebase**: Already using asyncio libraries

Synchronous Usage
-----------------

Basic Usage
~~~~~~~~~~~

.. code-block:: python

   from navercommerce import NaverCommerce

   # Initialize client
   client = NaverCommerce(
       client_id="your_client_id",
       client_secret="your_client_secret"
   )

   # Call methods directly
   account = client.seller.account()
   products = client.products.list()

   # Close when done
   client.close()

With Context Manager
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from navercommerce import NaverCommerce

   # Automatic cleanup
   with NaverCommerce() as client:
       account = client.seller.account()
       products = client.products.list()
   # Client closed automatically

Threading Example
~~~~~~~~~~~~~~~~~

.. code-block:: python

   from concurrent.futures import ThreadPoolExecutor
   from navercommerce import NaverCommerce

   def fetch_product(client, product_id):
       return client.products.retrieve(product_id)

   client = NaverCommerce()
   product_ids = ["id1", "id2", "id3", "id4", "id5"]

   # Fetch products in parallel using threads
   with ThreadPoolExecutor(max_workers=5) as executor:
       products = list(executor.map(
           lambda pid: fetch_product(client, pid),
           product_ids
       ))

   client.close()

Asynchronous Usage
------------------

Basic Usage
~~~~~~~~~~~

.. code-block:: python

   import asyncio
   from navercommerce import AsyncNaverCommerce

   async def main():
       # Initialize client
       client = AsyncNaverCommerce(
           client_id="your_client_id",
           client_secret="your_client_secret"
       )

       # Await async methods
       account = await client.seller.account()
       products = await client.products.list()

       # Close when done
       await client.close()

   # Run async function
   asyncio.run(main())

With Context Manager (Recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import asyncio
   from navercommerce import AsyncNaverCommerce

   async def main():
       # Automatic cleanup
       async with AsyncNaverCommerce() as client:
           account = await client.seller.account()
           products = await client.products.list()
       # Client closed automatically

   asyncio.run(main())

Concurrent Requests
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import asyncio
   from navercommerce import AsyncNaverCommerce

   async def main():
       async with AsyncNaverCommerce() as client:
           # Fetch multiple products concurrently
           product_ids = ["id1", "id2", "id3", "id4", "id5"]
           tasks = [client.products.retrieve(pid) for pid in product_ids]

           # Wait for all tasks to complete
           products = await asyncio.gather(*tasks)

           for product in products:
               print(f"{product.name}: {product.sale_price}원")

   asyncio.run(main())

FastAPI Integration
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from fastapi import FastAPI, HTTPException
   from navercommerce import AsyncNaverCommerce, NotFoundError

   app = FastAPI()
   client = AsyncNaverCommerce()

   @app.on_event("startup")
   async def startup():
       # Initialize client on startup
       global client
       client = AsyncNaverCommerce()

   @app.on_event("shutdown")
   async def shutdown():
       # Clean up on shutdown
       await client.close()

   @app.get("/products/{product_id}")
   async def get_product(product_id: str):
       try:
           product = await client.products.retrieve(product_id)
           return {
               "name": product.name,
               "price": product.sale_price
           }
       except NotFoundError:
           raise HTTPException(status_code=404, detail="Product not found")

Performance Comparison
----------------------

Sequential Operations
~~~~~~~~~~~~~~~~~~~~~

For sequential operations, sync and async have similar performance:

.. code-block:: python

   # Synchronous - ~10 seconds for 10 requests
   client = NaverCommerce()
   for i in range(10):
       account = client.seller.account()

   # Asynchronous - ~10 seconds for 10 sequential requests
   async def sequential():
       async with AsyncNaverCommerce() as client:
           for i in range(10):
               account = await client.seller.account()

Concurrent Operations
~~~~~~~~~~~~~~~~~~~~~

Async shines when making concurrent requests:

.. code-block:: python

   # Synchronous with threads - ~2-3 seconds for 10 concurrent requests
   with ThreadPoolExecutor(max_workers=10) as executor:
       results = list(executor.map(get_account, [client] * 10))

   # Asynchronous - ~1 second for 10 concurrent requests (faster!)
   async def concurrent():
       async with AsyncNaverCommerce() as client:
           tasks = [client.seller.account() for _ in range(10)]
           results = await asyncio.gather(*tasks)

Async is typically 2-10x faster for concurrent I/O operations.

Common Patterns
---------------

Pattern 1: Batch Processing (Sync)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from navercommerce import NaverCommerce

   def process_orders():
       client = NaverCommerce()

       # Get all orders
       orders = client.orders.list(start_date="2024-01-01")

       # Process each order
       for order in orders:
           print(f"Processing {order['productOrderId']}")
           client.orders.confirm([order['productOrderId']])

   process_orders()

Pattern 2: Batch Processing (Async)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import asyncio
   from navercommerce import AsyncNaverCommerce

   async def process_orders():
       async with AsyncNaverCommerce() as client:
           # Get all orders
           orders = await client.orders.list(start_date="2024-01-01")

           # Process all orders concurrently
           tasks = [
               client.orders.confirm([order['productOrderId']])
               for order in orders
           ]
           await asyncio.gather(*tasks)

   asyncio.run(process_orders())

Pattern 3: Web API Endpoint (Async)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from fastapi import FastAPI
   from navercommerce import AsyncNaverCommerce

   app = FastAPI()

   @app.get("/seller/products")
   async def list_products(page: int = 1, size: int = 20):
       async with AsyncNaverCommerce() as client:
           products = await client.products.list(page=page, size=size)
           return {
               "products": [
                   {"name": p.name, "price": p.sale_price}
                   for p in products
               ]
           }

Mixing Sync and Async
---------------------

You **cannot** mix sync and async in the same execution context:

❌ **This Won't Work**:

.. code-block:: python

   # ERROR: Cannot await in sync function
   def sync_function():
       client = AsyncNaverCommerce()
       account = await client.seller.account()  # SyntaxError!

❌ **This Won't Work**:

.. code-block:: python

   # ERROR: Cannot call sync method in async function
   async def async_function():
       client = NaverCommerce()
       account = client.seller.account()  # Blocks event loop!

✅ **Solutions**:

1. **Use the right client for your context**

   .. code-block:: python

      # Sync context → use sync client
      def sync_function():
          client = NaverCommerce()
          account = client.seller.account()

      # Async context → use async client
      async def async_function():
          async with AsyncNaverCommerce() as client:
              account = await client.seller.account()

2. **Run sync code in async** (if you must)

   .. code-block:: python

      import asyncio
      from navercommerce import NaverCommerce

      async def call_sync_from_async():
          client = NaverCommerce()

          # Run sync code in thread pool
          account = await asyncio.to_thread(client.seller.account)

          client.close()

Decision Tree
-------------

.. code-block:: text

   Are you building a web server?
   ├─ Yes → Use AsyncNaverCommerce
   │
   └─ No → Do you need high concurrency?
       ├─ Yes → Use AsyncNaverCommerce
       │
       └─ No → Is this a simple script?
           ├─ Yes → Use NaverCommerce
           │
           └─ No → Is your codebase already async?
               ├─ Yes → Use AsyncNaverCommerce
               └─ No → Use NaverCommerce

Summary
-------

**Choose Synchronous** (``NaverCommerce``) if:

- Writing scripts or CLI tools
- Simple applications without high concurrency
- Existing synchronous codebase
- Easier debugging is important

**Choose Asynchronous** (``AsyncNaverCommerce``) if:

- Building web servers (FastAPI, aiohttp, etc.)
- High concurrency requirements
- Existing async codebase
- Maximum performance is critical

**When in doubt**, start with synchronous - it's simpler and easier to understand. You can always switch to async later if needed.

See Also
--------

- :doc:`core-concepts` - SDK architecture overview
- :doc:`best-practices` - Production patterns
- :doc:`../examples/async-usage` - Complete async examples
