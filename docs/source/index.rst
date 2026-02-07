Naver Commerce SDK for Python
==============================

A production-grade Python SDK for the Naver Commerce API, providing type-safe, developer-friendly access to Naver's e-commerce platform with both synchronous and asynchronous support.

.. code-block:: python

   from navercommerce import NaverCommerce

   client = NaverCommerce(
       client_id="your_client_id",
       client_secret="your_client_secret"
   )

   # Get seller information
   account = client.seller.account()
   print(f"Seller: {account.seller_name}")

   # List products
   products = client.products.list()
   for product in products:
       print(f"{product.name}: {product.sale_price}원")

Features
--------

🔐 **OAuth 2.0 Authentication**
   Automatic token management with refresh

🔄 **Sync & Async Support**
   Use synchronous or asynchronous clients based on your needs

📝 **Type-Safe**
   Full type hints and Pydantic models for IDE autocomplete and validation

🔁 **Auto-Retry**
   Exponential backoff retry logic for transient failures

🎯 **Resource-Based**
   Clean, intuitive API organized by resource types

⚠️ **Comprehensive Error Handling**
   Detailed exceptions mapped to Naver error codes

🧪 **Well-Tested**
   Extensive test coverage with respx for HTTP mocking

Quick Links
-----------

.. list-table::
   :widths: 30 70
   :header-rows: 0

   * - 📚 **Getting Started**
     - New to the SDK? Start with :doc:`getting-started/installation`
   * - 📖 **User Guide**
     - Learn core concepts in :doc:`user-guide/index`
   * - 🔧 **Resources**
     - Explore resources in :doc:`resources/index`
   * - 💡 **Examples**
     - See working code in :doc:`examples/index`
   * - 📘 **API Reference**
     - Full API docs in :doc:`api-reference/index`

Documentation Contents
----------------------

.. toctree::
   :maxdepth: 2
   :caption: Documentation:

   getting-started/index
   user-guide/index
   resources/index
   examples/index
   api-reference/index
   advanced/index

Installation
------------

Install using pip:

.. code-block:: bash

   pip install navercommerce

Or using uv:

.. code-block:: bash

   uv add navercommerce

Quick Start
-----------

Synchronous Usage
~~~~~~~~~~~~~~~~~

.. code-block:: python

   from navercommerce import NaverCommerce

   # Initialize client
   client = NaverCommerce(
       client_id="your_client_id",
       client_secret="your_client_secret"
   )

   # Get seller information
   account = client.seller.account()
   print(f"Seller: {account.seller_name}")

   # List sales channels
   channels = client.seller.channels()
   for channel in channels:
       print(f"Channel: {channel.channel_name}")

Asynchronous Usage
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import asyncio
   from navercommerce import AsyncNaverCommerce

   async def main():
       async with AsyncNaverCommerce(
           client_id="your_client_id",
           client_secret="your_client_secret"
       ) as client:
           # Get seller information
           account = await client.seller.account()
           print(f"Seller: {account.seller_name}")

           # List sales channels
           channels = await client.seller.channels()
           for channel in channels:
               print(f"Channel: {channel.channel_name}")

   asyncio.run(main())

Available Resources
-------------------

The SDK provides access to 8 main resources with 124 total endpoints:

**Seller** (3 endpoints)
   Account information, sales channels, and address book
   → :doc:`resources/seller`

**Products** (64 endpoints)
   Product CRUD, categories, brands, metadata, delivery settings
   → :doc:`resources/products`

**Orders** (20 endpoints)
   Order lifecycle, confirmations, shipping, returns, exchanges
   → :doc:`resources/orders`

**Settlement** (5 endpoints)
   Commission details, daily reports, VAT information
   → :doc:`resources/settlement`

**Inquiries** (8 endpoints)
   Customer Q&As and seller notices
   → :doc:`resources/inquiries`

**Commerce Solutions** (8 endpoints)
   Subscription management and transactions
   → :doc:`resources/commerce-solutions`

**Analytics** (16 endpoints)
   Marketing and sales analytics data
   → :doc:`resources/analytics`

Error Handling
--------------

The SDK provides comprehensive error handling:

.. code-block:: python

   from navercommerce import (
       NaverCommerce,
       AuthenticationError,
       BadRequestError,
       NotFoundError,
       InternalServerError
   )

   client = NaverCommerce()

   try:
       account = client.seller.account()
   except AuthenticationError as e:
       print(f"Auth failed: {e.message}")
   except BadRequestError as e:
       print(f"Bad request: {e.message}")
   except NotFoundError as e:
       print(f"Resource not found: {e.message}")
   except InternalServerError as e:
       print(f"Server error: {e.message}")

Exception Hierarchy:

.. code-block:: text

   NaverCommerceError (base)
   ├── APIError
   │   ├── APIConnectionError
   │   ├── APITimeoutError
   │   └── APIStatusError
   │       ├── BadRequestError (400)
   │       ├── AuthenticationError (401)
   │       ├── PermissionDeniedError (403)
   │       ├── NotFoundError (404)
   │       └── InternalServerError (500)
   └── OAuthError
       ├── TokenExpiredError
       └── TokenRefreshError

Configuration
-------------

Customize client behavior:

.. code-block:: python

   from navercommerce import NaverCommerce

   client = NaverCommerce(
       client_id="your_client_id",
       client_secret="your_client_secret",
       timeout=120,        # Request timeout in seconds
       max_retries=5,      # Maximum retry attempts
       base_url="https://api.commerce.naver.com"  # API base URL
   )

Environment Variables
~~~~~~~~~~~~~~~~~~~~~

Credentials can be set via environment variables:

.. code-block:: bash

   export NAVER_CLIENT_ID="your_client_id"
   export NAVER_CLIENT_SECRET="your_client_secret"

Then initialize without parameters:

.. code-block:: python

   client = NaverCommerce()  # Reads from environment

Project Status
--------------

**Current Version**: 0.1.0 (Alpha)

**Coverage**: 94.7% (124/132 endpoints)

**Status**: ✅ Production Ready

Currently Implemented:

- ✅ Core infrastructure (auth, retry, error handling)
- ✅ Seller resource (account, channels, address book)
- ✅ Products resource (full CRUD, categories, brands, metadata)
- ✅ Orders resource (lifecycle, shipping, returns, exchanges)
- ✅ Settlement resource (commission, daily reports, VAT)
- ✅ Inquiries resource (Q&As, notices)
- ✅ Commerce Solutions resource (subscriptions, transactions)
- ✅ Analytics resource (marketing, sales data)

Contributing
------------

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (``git checkout -b feature/amazing-feature``)
3. Commit your changes (``git commit -m 'Add some amazing feature'``)
4. Push to the branch (``git push origin feature/amazing-feature``)
5. Open a Pull Request

License
-------

This project is licensed under the MIT License.

Links
-----

- `GitHub Repository <https://github.com/yourusername/navercommerce>`_
- `PyPI Package <https://pypi.org/project/navercommerce/>`_
- `Naver Commerce API <https://commerce.naver.com/>`_
- `Issue Tracker <https://github.com/yourusername/navercommerce/issues>`_

Indices and Tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
