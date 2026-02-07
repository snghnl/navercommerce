Configuration
=============

This guide covers all configuration options for customizing the Naver Commerce SDK client behavior.

Client Configuration
--------------------

Both ``NaverCommerce`` and ``AsyncNaverCommerce`` accept the same configuration parameters:

.. code-block:: python

   from navercommerce import NaverCommerce

   client = NaverCommerce(
       client_id="your_client_id",           # Required
       client_secret="your_client_secret",   # Required
       timeout=120,                          # Optional: request timeout
       max_retries=3,                        # Optional: max retry attempts
       base_url="https://api.url",           # Optional: custom base URL
   )

Authentication Configuration
----------------------------

Client Credentials
~~~~~~~~~~~~~~~~~~

Provide OAuth 2.0 credentials in two ways:

**Method 1: Direct Parameters**

.. code-block:: python

   client = NaverCommerce(
       client_id="your_client_id",
       client_secret="your_client_secret"
   )

**Method 2: Environment Variables**

.. code-block:: bash

   export NAVER_CLIENT_ID="your_client_id"
   export NAVER_CLIENT_SECRET="your_client_secret"

.. code-block:: python

   # Automatically reads from environment
   client = NaverCommerce()

Environment Variable Names
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The SDK looks for these environment variable names:

- ``NAVER_CLIENT_ID``
- ``NAVER_CLIENT_SECRET``

Using .env Files
~~~~~~~~~~~~~~~~

The SDK automatically loads from ``.env`` files:

.. code-block:: bash

   # .env
   NAVER_CLIENT_ID=your_client_id
   NAVER_CLIENT_SECRET=your_client_secret

.. code-block:: python

   # Automatically loaded
   client = NaverCommerce()

Timeout Configuration
---------------------

The ``timeout`` parameter controls how long to wait for API responses.

Default Timeout
~~~~~~~~~~~~~~~

Default timeout is **60 seconds**:

.. code-block:: python

   # Uses 60 second timeout
   client = NaverCommerce()

Custom Timeout
~~~~~~~~~~~~~~

Set a custom timeout in seconds:

.. code-block:: python

   # 120 second timeout
   client = NaverCommerce(timeout=120)

   # 30 second timeout (faster failures)
   client = NaverCommerce(timeout=30)

   # 300 second timeout (for slow operations)
   client = NaverCommerce(timeout=300)

When to Adjust Timeout
~~~~~~~~~~~~~~~~~~~~~~~

**Increase timeout** when:

- Making requests that process large amounts of data
- Experiencing frequent timeout errors
- Network latency is high

**Decrease timeout** when:

- Want faster failure detection
- Implementing strict SLAs
- Using retry logic (fail fast, retry quickly)

Timeout Errors
~~~~~~~~~~~~~~

When a timeout occurs, the SDK raises ``APITimeoutError``:

.. code-block:: python

   from navercommerce import NaverCommerce, APITimeoutError

   client = NaverCommerce(timeout=5)

   try:
       products = client.products.list()
   except APITimeoutError as e:
       print(f"Request timed out after {client.timeout}s")
       # Retry or handle error

Retry Configuration
-------------------

The SDK automatically retries failed requests with exponential backoff.

Default Retry Behavior
~~~~~~~~~~~~~~~~~~~~~~~

Default is **2 retries**:

.. code-block:: python

   # Tries up to 3 times total (1 initial + 2 retries)
   client = NaverCommerce()

Custom Max Retries
~~~~~~~~~~~~~~~~~~

Set a custom retry count:

.. code-block:: python

   # No retries (fail immediately)
   client = NaverCommerce(max_retries=0)

   # Try up to 4 times (1 initial + 3 retries)
   client = NaverCommerce(max_retries=3)

   # Aggressive retries for critical operations
   client = NaverCommerce(max_retries=5)

When Retries Happen
~~~~~~~~~~~~~~~~~~~

The SDK retries for:

✅ **Network Errors**: Connection failures, DNS errors
✅ **Rate Limiting**: 429 Too Many Requests
✅ **Server Errors**: 500, 502, 503, 504

The SDK does NOT retry for:

❌ **Client Errors**: 400, 401, 403, 404 (these indicate bugs/invalid requests)
❌ **Successful Responses**: 200, 201, 204

Retry Backoff Strategy
~~~~~~~~~~~~~~~~~~~~~~~

Wait time increases exponentially:

- **Retry 1**: Wait ~0.5 seconds
- **Retry 2**: Wait ~1 second
- **Retry 3**: Wait ~2 seconds
- **Retry 4**: Wait ~4 seconds
- **Retry 5**: Wait ~8 seconds

This prevents overwhelming the server during outages.

Configuring for Different Scenarios
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**High Reliability** (tolerate transient failures):

.. code-block:: python

   client = NaverCommerce(
       max_retries=5,      # More retry attempts
       timeout=120         # Longer timeout
   )

**Fast Failure** (detect problems quickly):

.. code-block:: python

   client = NaverCommerce(
       max_retries=0,      # No retries
       timeout=10          # Short timeout
   )

**Balanced** (default):

.. code-block:: python

   client = NaverCommerce(
       max_retries=2,      # Reasonable retries
       timeout=60          # Standard timeout
   )

Base URL Configuration
----------------------

Override the API base URL for testing or alternative endpoints.

Default Base URL
~~~~~~~~~~~~~~~~

The default is Naver Commerce's production API:

.. code-block:: python

   # Uses https://api.commerce.naver.com
   client = NaverCommerce()

Custom Base URL
~~~~~~~~~~~~~~~

Set a custom base URL:

.. code-block:: python

   # Use staging environment
   client = NaverCommerce(
       base_url="https://staging.api.commerce.naver.com"
   )

   # Use local mock server for testing
   client = NaverCommerce(
       base_url="http://localhost:8000"
   )

Use Cases for Custom Base URL
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Testing**: Point to a mock server or test environment
2. **Staging**: Use a staging API for pre-production testing
3. **Proxy**: Route requests through a proxy or API gateway
4. **Local Development**: Use a local API simulator

Example: Testing with Mock Server
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import respx
   from navercommerce import NaverCommerce

   # Start mock server
   with respx.mock:
       # Mock the API endpoint
       respx.get("http://localhost:8000/seller/account").mock(
           return_value={"sellerId": "123", "sellerName": "Test"}
       )

       # Use client with mock base URL
       client = NaverCommerce(
           client_id="test",
           client_secret="test",
           base_url="http://localhost:8000"
       )

       account = client.seller.account()
       assert account.seller_id == "123"

HTTP Client Configuration
--------------------------

Advanced httpx Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For advanced use cases, you can customize the underlying httpx client.

The SDK uses httpx for HTTP requests. While you can't directly pass httpx client options to the SDK constructor, you can extend the client classes for custom behavior:

.. code-block:: python

   from navercommerce._client import NaverCommerce
   import httpx

   class CustomNaverCommerce(NaverCommerce):
       def __init__(self, **kwargs):
           super().__init__(**kwargs)

           # Customize httpx client after initialization
           # Note: This is an advanced pattern
           self._client._client = httpx.Client(
               timeout=httpx.Timeout(60.0),
               limits=httpx.Limits(max_connections=100),
               # Add custom headers, proxies, etc.
           )

Connection Pooling
~~~~~~~~~~~~~~~~~~

The SDK automatically manages connection pooling via httpx:

- Connections are reused across requests
- Connection pool limits are set automatically
- Connections are closed when the client is closed

.. code-block:: python

   # Connections are pooled automatically
   with NaverCommerce() as client:
       for i in range(100):
           client.seller.account()  # Reuses connections
   # Connections closed automatically

Environment-Specific Configuration
-----------------------------------

Development Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # .env.development
   NAVER_CLIENT_ID=dev_client_id
   NAVER_CLIENT_SECRET=dev_client_secret

   # config/development.py
   from navercommerce import NaverCommerce

   client = NaverCommerce(
       timeout=120,        # Longer timeout for debugging
       max_retries=0,      # No retries (see errors immediately)
   )

Production Configuration
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # .env.production (set in deployment platform)
   NAVER_CLIENT_ID=prod_client_id
   NAVER_CLIENT_SECRET=prod_client_secret

   # config/production.py
   from navercommerce import NaverCommerce

   client = NaverCommerce(
       timeout=60,         # Standard timeout
       max_retries=3,      # Retry transient failures
   )

Configuration from Files
~~~~~~~~~~~~~~~~~~~~~~~~

Load configuration from a YAML or JSON file:

.. code-block:: python

   # config.yaml
   # naver:
   #   client_id: your_client_id
   #   client_secret: your_client_secret
   #   timeout: 120
   #   max_retries: 3

   import yaml
   from navercommerce import NaverCommerce

   with open("config.yaml") as f:
       config = yaml.safe_load(f)

   client = NaverCommerce(
       client_id=config['naver']['client_id'],
       client_secret=config['naver']['client_secret'],
       timeout=config['naver']['timeout'],
       max_retries=config['naver']['max_retries'],
   )

Async Configuration
-------------------

AsyncNaverCommerce uses the same configuration parameters:

.. code-block:: python

   import asyncio
   from navercommerce import AsyncNaverCommerce

   async def main():
       async with AsyncNaverCommerce(
           client_id="your_client_id",
           client_secret="your_client_secret",
           timeout=120,
           max_retries=3,
       ) as client:
           account = await client.seller.account()

   asyncio.run(main())

Configuration Best Practices
-----------------------------

1. **Use Environment Variables**

   Never hardcode credentials:

   ✅ Good:

   .. code-block:: python

      client = NaverCommerce()  # Reads from env vars

   ❌ Bad:

   .. code-block:: python

      client = NaverCommerce(
          client_id="hardcoded_id",  # Don't do this!
          client_secret="hardcoded_secret"
      )

2. **Different Configs for Different Environments**

   Use separate configurations for dev/staging/production:

   .. code-block:: python

      import os

      env = os.getenv("APP_ENV", "development")

      if env == "production":
          client = NaverCommerce(timeout=60, max_retries=3)
      else:
          client = NaverCommerce(timeout=120, max_retries=0)

3. **Document Your Configuration**

   Document why you chose specific values:

   .. code-block:: python

      client = NaverCommerce(
          # Increased timeout due to large product catalogs
          timeout=180,
          # Aggressive retries for critical order processing
          max_retries=5,
      )

4. **Test Configuration**

   Validate configuration at startup:

   .. code-block:: python

      from navercommerce import NaverCommerce, AuthenticationError

      try:
          client = NaverCommerce()
          # Test connection
          client.seller.account()
          print("✓ Configuration valid")
      except AuthenticationError:
          print("✗ Invalid credentials")
          raise

5. **Use Context Managers**

   Always use context managers for proper cleanup:

   .. code-block:: python

      # Automatic cleanup
      with NaverCommerce() as client:
          account = client.seller.account()

Summary
-------

Key Configuration Options:

- ``client_id``: OAuth client ID (required)
- ``client_secret``: OAuth client secret (required)
- ``timeout``: Request timeout in seconds (default: 60)
- ``max_retries``: Maximum retry attempts (default: 2)
- ``base_url``: API base URL (default: Naver Commerce API)

Best Practices:

- Use environment variables for credentials
- Adjust timeout based on operation type
- Configure retries based on reliability needs
- Use different configs for different environments
- Test configuration at startup

See Also
--------

- :doc:`../getting-started/authentication` - Authentication setup
- :doc:`error-handling` - Understanding retry behavior
- :doc:`best-practices` - Production configuration patterns
