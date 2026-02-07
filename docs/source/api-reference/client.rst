Client Classes
==============

Main client classes for interacting with the Naver Commerce API.

NaverCommerce (Sync)
--------------------

.. autoclass:: navercommerce.NaverCommerce
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__, __enter__, __exit__

AsyncNaverCommerce (Async)
--------------------------

.. autoclass:: navercommerce.AsyncNaverCommerce
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__, __aenter__, __aexit__

Usage Examples
--------------

Synchronous Client
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from navercommerce import NaverCommerce

   # Initialize
   client = NaverCommerce(
       client_id="your_client_id",
       client_secret="your_client_secret"
   )

   # Use client
   account = client.seller.account()

   # Cleanup
   client.close()

   # Or use context manager
   with NaverCommerce() as client:
       account = client.seller.account()

Asynchronous Client
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import asyncio
   from navercommerce import AsyncNaverCommerce

   async def main():
       async with AsyncNaverCommerce() as client:
           account = await client.seller.account()

   asyncio.run(main())

See Also
--------

- :doc:`../getting-started/quickstart` - Quick start guide
- :doc:`../user-guide/sync-vs-async` - Sync vs async comparison
- :doc:`resources` - Resource classes
