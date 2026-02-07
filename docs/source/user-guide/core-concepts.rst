Core Concepts
=============

This guide explains the fundamental concepts and architecture of the Naver Commerce SDK.

SDK Architecture
----------------

The SDK follows a **3-tier layered architecture** inspired by the OpenAI Python SDK:

.. code-block:: text

   BaseClient (HTTP, OAuth, retry logic)
     ├─ SyncAPIClient
     │   └─ NaverCommerce (main sync client)
     └─ AsyncAPIClient
         └─ AsyncNaverCommerce (main async client)

Layer 1: Base Client
~~~~~~~~~~~~~~~~~~~~~

The ``BaseClient`` layer provides core functionality shared by both sync and async clients:

- **HTTP Communication**: Makes HTTP requests using httpx
- **OAuth 2.0 Token Management**: Automatic token acquisition and refresh
- **Retry Logic**: Exponential backoff for transient failures
- **Error Handling**: Maps HTTP status codes to specific exceptions

You typically don't interact with ``BaseClient`` directly.

Layer 2: API Clients
~~~~~~~~~~~~~~~~~~~~~

The ``SyncAPIClient`` and ``AsyncAPIClient`` layers extend the base client with:

- **Resource Organization**: Groups endpoints by resource type
- **Type Validation**: Pydantic models for request/response validation
- **Context Managers**: Automatic resource cleanup

Layer 3: Main Clients
~~~~~~~~~~~~~~~~~~~~~~

``NaverCommerce`` and ``AsyncNaverCommerce`` are the main entry points:

.. code-block:: python

   from navercommerce import NaverCommerce

   client = NaverCommerce(
       client_id="your_client_id",
       client_secret="your_client_secret"
   )

Resource Organization
---------------------

The SDK organizes API endpoints into **resources**, each representing a logical grouping of related operations:

Available Resources
~~~~~~~~~~~~~~~~~~~

=============================  ===========================================
Resource                       Description
=============================  ===========================================
``client.seller``              Seller account, channels, addresses
``client.products``            Product CRUD, categories, brands
``client.orders``              Order lifecycle, shipping, returns
``client.settlement``          Commission, daily reports, VAT
``client.inquiries``           Customer Q&As, seller notices
``client.commerce_solutions``  Subscriptions, transactions
``client.analytics``           Marketing and sales analytics
=============================  ===========================================

Each resource exposes methods for specific API endpoints:

.. code-block:: python

   # Access resources via the client
   account = client.seller.account()
   products = client.products.list()
   orders = client.orders.list(start_date="2024-01-01")

Nested Resources
~~~~~~~~~~~~~~~~~

Some resources have nested sub-resources:

.. code-block:: python

   # Product images sub-resource
   image = client.products.images.upload(file=image_data)

   # Product stock sub-resource
   stock = client.products.stock.retrieve("product_id")

Type Safety
-----------

The SDK uses **Pydantic models** for comprehensive type safety:

Request Validation
~~~~~~~~~~~~~~~~~~

Input parameters are validated before making API calls:

.. code-block:: python

   # This will raise a validation error before making the API call
   product = client.products.create(
       name="Product",
       sale_price="invalid",  # Should be int, not str
   )

Response Validation
~~~~~~~~~~~~~~~~~~~

API responses are parsed into typed Pydantic models:

.. code-block:: python

   # Response is a Pydantic model with type hints
   account = client.seller.account()

   # IDE autocomplete works
   print(account.seller_name)  # Type: str
   print(account.seller_id)    # Type: str

   # Type checking catches errors
   print(account.invalid_field)  # IDE/mypy error: field doesn't exist

Type Hints
~~~~~~~~~~

All methods have complete type hints for better IDE support:

.. code-block:: python

   from navercommerce import NaverCommerce
   from navercommerce.types import Account

   client = NaverCommerce()

   # Type checkers know this returns Account
   account: Account = client.seller.account()

   # Type checkers know this returns list of products
   products = client.products.list()  # List[Product]

OAuth 2.0 Token Management
---------------------------

The SDK automatically handles OAuth 2.0 authentication:

Token Lifecycle
~~~~~~~~~~~~~~~

1. **Initial Request**: When you make your first API call, the SDK requests an access token
2. **Token Caching**: The token is stored in memory for reuse
3. **Automatic Refresh**: When the token expires, the SDK automatically gets a new one
4. **Retry on Auth Failure**: If a request fails with 401, the SDK refreshes the token and retries

.. code-block:: python

   client = NaverCommerce(
       client_id="your_client_id",
       client_secret="your_client_secret"
   )

   # First call: Fetches token automatically
   account = client.seller.account()

   # Subsequent calls: Reuses cached token
   channels = client.seller.channels()

   # Token expired: Automatically refreshes and retries
   # You don't need to handle this!

Thread Safety
~~~~~~~~~~~~~

Token management is **thread-safe**, allowing concurrent requests:

.. code-block:: python

   import concurrent.futures

   client = NaverCommerce()

   def get_product(product_id):
       return client.products.retrieve(product_id)

   # Safe to use from multiple threads
   with concurrent.futures.ThreadPoolExecutor() as executor:
       futures = [executor.submit(get_product, pid) for pid in product_ids]
       products = [f.result() for f in futures]

HTTP Connection Pooling
-----------------------

The SDK uses **httpx** for efficient HTTP connection pooling:

- Connections are reused across requests
- Persistent connections reduce latency
- Automatic connection cleanup with context managers

.. code-block:: python

   # Recommended: Use context manager for cleanup
   with NaverCommerce() as client:
       account = client.seller.account()
       products = client.products.list()
   # Connections closed automatically

   # Or manually close
   client = NaverCommerce()
   try:
       account = client.seller.account()
   finally:
       client.close()

Retry Logic
-----------

The SDK automatically retries failed requests with **exponential backoff**:

When Retries Happen
~~~~~~~~~~~~~~~~~~~

Retries are triggered for:

- **Network errors** (connection timeout, DNS failure)
- **Rate limiting** (429 Too Many Requests)
- **Server errors** (500, 502, 503, 504)

Retries are NOT triggered for:

- **Client errors** (400, 401, 403, 404) - these indicate bad requests
- **Successful responses** (200, 201, 204)

Exponential Backoff
~~~~~~~~~~~~~~~~~~~

Wait time increases exponentially between retries:

- Retry 1: Wait ~0.5 seconds
- Retry 2: Wait ~1 second
- Retry 3: Wait ~2 seconds
- Retry 4: Wait ~4 seconds

This prevents overwhelming the server during outages.

Configuring Retries
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Customize max retries (default: 2)
   client = NaverCommerce(max_retries=5)

   # Disable retries
   client = NaverCommerce(max_retries=0)

See :doc:`configuration` for more details.

Request/Response Flow
---------------------

Here's what happens when you make an API call:

1. **Method Call**: You call a resource method (e.g., ``client.seller.account()``)
2. **Token Check**: SDK checks if it has a valid access token
3. **Token Acquisition** (if needed): SDK fetches a new token via OAuth 2.0
4. **Request Validation**: Pydantic validates request parameters
5. **HTTP Request**: SDK makes the HTTP request with retry logic
6. **Response Parsing**: Response is parsed into a Pydantic model
7. **Error Handling**: HTTP errors are converted to typed exceptions
8. **Return**: Validated response model is returned to you

.. code-block:: python

   # All of this happens automatically:
   account = client.seller.account()
   #          ↓
   # 1. Check token → 2. Get token if needed → 3. Make HTTP request
   #          ↓
   # 4. Retry on failure → 5. Parse response → 6. Return typed model

Comparison to Other SDKs
------------------------

The Naver Commerce SDK follows similar patterns to:

- **OpenAI SDK**: 3-tier architecture, resource organization, retry logic
- **Stripe SDK**: Type-safe resources, automatic retries, error handling
- **AWS SDK**: Credential management, automatic retries, client configuration

If you've used any of these SDKs, the Naver Commerce SDK will feel familiar.

Next Steps
----------

- :doc:`sync-vs-async` - Learn when to use sync vs async clients
- :doc:`error-handling` - Understand exception types and error recovery
- :doc:`../advanced/architecture` - Deep dive into SDK architecture
- :doc:`../advanced/oauth-flow` - OAuth 2.0 implementation details
