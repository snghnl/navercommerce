Architecture
============

Understanding the SDK's design patterns and architecture.

Overview
--------

The Naver Commerce SDK follows a **3-tier layered architecture** inspired by the OpenAI Python SDK, providing clean separation of concerns and code reusability.

Architecture Diagram
--------------------

.. code-block:: text

   ┌─────────────────────────────────────────────────────────┐
   │                   Application Code                      │
   └─────────────────────────────────────────────────────────┘
                            ↓
   ┌─────────────────────────────────────────────────────────┐
   │  Layer 3: Main Clients                                  │
   │  ┌───────────────────┐    ┌───────────────────┐        │
   │  │  NaverCommerce    │    │ AsyncNaverCommerce│        │
   │  │  (Synchronous)    │    │  (Asynchronous)   │        │
   │  └───────────────────┘    └───────────────────┘        │
   └─────────────────────────────────────────────────────────┘
                            ↓
   ┌─────────────────────────────────────────────────────────┐
   │  Layer 2: API Clients & Resources                      │
   │  ┌──────────────────────────────────────────────────┐  │
   │  │  Resource Organization                           │  │
   │  │  • Products  • Orders    • Seller                │  │
   │  │  • Settlement • Inquiries • Analytics            │  │
   │  │  • CommerceSolutions                             │  │
   │  └──────────────────────────────────────────────────┘  │
   └─────────────────────────────────────────────────────────┘
                            ↓
   ┌─────────────────────────────────────────────────────────┐
   │  Layer 1: Base Client                                   │
   │  ┌──────────────────────────────────────────────────┐  │
   │  │  • HTTP Communication (httpx)                    │  │
   │  │  • OAuth 2.0 Token Management                    │  │
   │  │  • Retry Logic with Exponential Backoff          │  │
   │  │  • Error Handling & Exception Mapping            │  │
   │  │  • Request/Response Processing                   │  │
   │  └──────────────────────────────────────────────────┘  │
   └─────────────────────────────────────────────────────────┘
                            ↓
   ┌─────────────────────────────────────────────────────────┐
   │              Naver Commerce API                         │
   └─────────────────────────────────────────────────────────┘

Layer 1: Base Client
--------------------

The foundation layer handles all HTTP communication and cross-cutting concerns.

Responsibilities
~~~~~~~~~~~~~~~~

- **HTTP Requests**: Makes HTTP calls using httpx
- **Authentication**: Manages OAuth 2.0 token lifecycle
- **Retry Logic**: Implements exponential backoff for transient failures
- **Error Handling**: Converts HTTP errors to typed exceptions
- **Connection Pooling**: Manages HTTP connection pool

Key Components
~~~~~~~~~~~~~~

.. code-block:: python

   class BaseClient:
       def __init__(self, client_id, client_secret, timeout, max_retries):
           self._http_client = httpx.Client()
           self._token_manager = TokenManager()
           self._retry_config = RetryConfig(max_retries)

       def request(self, method, endpoint, **kwargs):
           # 1. Get access token
           token = self._token_manager.get_token()

           # 2. Make HTTP request with retry logic
           response = self._retry_request(method, endpoint, token, **kwargs)

           # 3. Handle errors
           if response.status_code >= 400:
               raise self._map_error(response)

           # 4. Return response
           return response

Layer 2: API Clients & Resources
---------------------------------

The middle layer organizes endpoints into logical resource groups.

Resource Organization
~~~~~~~~~~~~~~~~~~~~~

Resources group related API endpoints:

.. code-block:: python

   class Products:
       """Product resource with CRUD operations."""

       def __init__(self, client: BaseClient):
           self._client = client
           self.metadata = ProductsMetadata(client)
           self.delivery = ProductsDelivery(client)
           # ... other sub-resources

       def create(self, **kwargs) -> Product:
           """Create a product."""
           response = self._client.request("POST", "/products", json=kwargs)
           return Product.model_validate(response.json())

       def retrieve(self, product_id: str) -> Product:
           """Retrieve a product."""
           response = self._client.request("GET", f"/products/{product_id}")
           return Product.model_validate(response.json())

Type Safety
~~~~~~~~~~~

All responses are validated with Pydantic:

.. code-block:: python

   from pydantic import BaseModel

   class Product(BaseModel):
       id: str
       name: str
       sale_price: int
       status: str

   # Response is automatically validated
   product = client.products.retrieve("product_id")
   # product is guaranteed to have correct types

Layer 3: Main Clients
---------------------

The top layer provides the public API surface.

Dual Client Design
~~~~~~~~~~~~~~~~~~

Separate sync and async clients with identical APIs:

.. code-block:: python

   # Synchronous
   class NaverCommerce:
       def __init__(self, **kwargs):
           self._client = SyncBaseClient(**kwargs)
           self.seller = Seller(self._client)
           self.products = Products(self._client)
           # ... other resources

   # Asynchronous
   class AsyncNaverCommerce:
       def __init__(self, **kwargs):
           self._client = AsyncBaseClient(**kwargs)
           self.seller = AsyncSeller(self._client)
           self.products = AsyncProducts(self._client)
           # ... other resources

Context Manager Support
~~~~~~~~~~~~~~~~~~~~~~~

Both clients support context managers for cleanup:

.. code-block:: python

   # Sync
   with NaverCommerce() as client:
       account = client.seller.account()

   # Async
   async with AsyncNaverCommerce() as client:
       account = await client.seller.account()

Design Patterns
---------------

Repository Pattern
~~~~~~~~~~~~~~~~~~

Each resource acts as a repository for its domain:

.. code-block:: python

   # Products repository
   class Products:
       def create(self, **kwargs): ...
       def retrieve(self, id): ...
       def update(self, id, **kwargs): ...
       def delete(self, id): ...
       def list(self, **params): ...

Composition Over Inheritance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Resources compose sub-resources:

.. code-block:: python

   class Products:
       def __init__(self, client):
           self._client = client
           # Compose sub-resources
           self.metadata = ProductsMetadata(client)
           self.delivery = ProductsDelivery(client)
           self.management = ProductsManagement(client)

Builder Pattern
~~~~~~~~~~~~~~~

Fluent API for resource access:

.. code-block:: python

   client.products.metadata.list_brands()
   client.products.delivery.list_bundle_groups()
   client.inquiries.qnas.list()

Comparison to Other SDKs
------------------------

OpenAI SDK
~~~~~~~~~~

The architecture is inspired by OpenAI's Python SDK:

**Similarities**:
- 3-tier architecture
- Resource-based organization
- Automatic retry logic
- Sync/async support

**Differences**:
- OAuth 2.0 vs API key authentication
- Different resource organization
- Domain-specific type models

Stripe SDK
~~~~~~~~~~

**Similarities**:
- Resource organization
- Type-safe responses
- Automatic retries

**Differences**:
- Stripe uses nested resources more heavily
- Different authentication mechanism
- More complex pagination

AWS SDK (boto3)
~~~~~~~~~~~~~~~

**Similarities**:
- Service/resource organization
- Credential management
- Retry logic

**Differences**:
- AWS uses service clients, not resources
- More complex authentication
- Different API paradigm (RPC vs REST)

Code Organization
-----------------

Project Structure
~~~~~~~~~~~~~~~~~

.. code-block:: text

   navercommerce/
   ├── __init__.py              # Public API exports
   ├── _client.py               # Main clients (Layer 3)
   ├── _base_client.py          # Base client (Layer 1)
   ├── _token_manager.py        # OAuth token management
   ├── _exceptions.py           # Exception hierarchy
   ├── resources/               # Layer 2
   │   ├── seller.py
   │   ├── products.py
   │   ├── orders.py
   │   ├── settlement.py
   │   ├── inquiries.py
   │   ├── commerce_solutions.py
   │   └── analytics.py
   └── types/                   # Pydantic models
       ├── seller.py
       ├── products.py
       ├── orders.py
       └── ...

Module Boundaries
~~~~~~~~~~~~~~~~~

Clear separation between layers:

- **Layer 1**: ``_base_client.py``, ``_token_manager.py``
- **Layer 2**: ``resources/`` directory
- **Layer 3**: ``_client.py``
- **Cross-cutting**: ``_exceptions.py``, ``types/``

Extension Points
----------------

Custom Resources
~~~~~~~~~~~~~~~~

Add custom resources by extending the base:

.. code-block:: python

   from navercommerce._base_client import BaseClient

   class CustomResource:
       def __init__(self, client: BaseClient):
           self._client = client

       def custom_method(self):
           return self._client.request("GET", "/custom")

   # Add to client
   NaverCommerce.custom = CustomResource(client._client)

Custom Retry Logic
~~~~~~~~~~~~~~~~~~

Override retry behavior:

.. code-block:: python

   class CustomClient(NaverCommerce):
       def __init__(self, **kwargs):
           super().__init__(**kwargs)
           # Customize retry logic
           self._client._max_retries = 10

Benefits of This Architecture
------------------------------

1. **Separation of Concerns**

   Each layer has a single, well-defined responsibility.

2. **Code Reusability**

   Base client is shared by sync and async implementations.

3. **Testability**

   Each layer can be tested independently with mocks.

4. **Extensibility**

   Easy to add new resources or customize behavior.

5. **Maintainability**

   Clear structure makes codebase easy to navigate.

6. **Type Safety**

   Pydantic models catch errors at development time.

See Also
--------

- :doc:`../user-guide/core-concepts` - SDK concepts overview
- :doc:`oauth-flow` - OAuth implementation details
- :doc:`retry-logic` - Retry mechanism details
- `OpenAI SDK <https://github.com/openai/openai-python>`_ - Architecture inspiration
