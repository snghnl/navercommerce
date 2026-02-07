Async Usage
===========

This example demonstrates asynchronous usage of the Naver Commerce SDK with concurrent operations.

Overview
--------

This example covers:

- Using the ``AsyncNaverCommerce`` client
- Async/await syntax with the SDK
- Concurrent API calls with ``asyncio.gather()``
- Context managers for async cleanup

Complete Code
-------------

.. literalinclude:: ../../../examples/async_example.py
   :language: python
   :linenos:

Walkthrough
-----------

1. **Import Async Client**

   Import the async client and asyncio:

   .. code-block:: python

      import asyncio
      from navercommerce import AsyncNaverCommerce

2. **Define Async Function**

   All async operations must be inside an async function:

   .. code-block:: python

      async def main():
          async with AsyncNaverCommerce() as client:
              # Async operations here

3. **Await API Calls**

   All SDK methods become async and must be awaited:

   .. code-block:: python

      account = await client.seller.account()
      channels = await client.seller.channels()

4. **Concurrent Operations**

   Make multiple API calls concurrently using ``asyncio.gather()``:

   .. code-block:: python

      results = await asyncio.gather(
          client.seller.account(),
          client.seller.channels(),
          client.seller.addresses()
      )

5. **Run Async Code**

   Use ``asyncio.run()`` to execute the async function:

   .. code-block:: python

      if __name__ == "__main__":
          asyncio.run(main())

Performance Benefits
--------------------

Async is significantly faster for concurrent operations:

**Sequential (sync)**: 3 calls × 1 second = **3 seconds**

.. code-block:: python

   account = client.seller.account()    # 1 second
   channels = client.seller.channels()  # 1 second
   addresses = client.seller.addresses() # 1 second

**Concurrent (async)**: 3 calls in parallel = **~1 second**

.. code-block:: python

   results = await asyncio.gather(
       client.seller.account(),    # All three run
       client.seller.channels(),   # concurrently!
       client.seller.addresses()
   )

Running the Example
-------------------

1. Set credentials:

   .. code-block:: bash

      export NAVER_CLIENT_ID="your_client_id"
      export NAVER_CLIENT_SECRET="your_client_secret"

2. Run the script:

   .. code-block:: bash

      python examples/async_example.py

Expected Output
---------------

.. code-block:: text

   Fetching account, channels, and addresses concurrently...

   Seller: Your Seller Name
   Channels: 1
   Addresses: 3

   Total time: ~1 second (vs 3 seconds sequential)

When to Use Async
-----------------

Use async when:

- Making many concurrent API calls
- Building web servers (FastAPI, aiohttp)
- Performance is critical
- Your codebase is already async

Use sync when:

- Writing simple scripts
- Sequential operations only
- Easier debugging is preferred

Related Examples
----------------

- :doc:`basic-usage` - Synchronous version
- :doc:`product-management` - Async product operations

See Also
--------

- :doc:`../user-guide/sync-vs-async` - Detailed comparison
- :doc:`../getting-started/quickstart` - Async quick start
