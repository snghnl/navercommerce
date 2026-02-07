Retry Logic
===========

Understanding the SDK's automatic retry mechanism with exponential backoff.

Overview
--------

The SDK automatically retries failed requests for transient errors:

- **Network errors**: Connection timeouts, DNS failures
- **Rate limiting**: 429 Too Many Requests
- **Server errors**: 500, 502, 503, 504

Retry Strategy
--------------

Exponential Backoff
~~~~~~~~~~~~~~~~~~~

Wait time increases exponentially between retries:

.. code-block:: text

   Attempt 1: Request → Fail
                ↓
             Wait ~0.5s
                ↓
   Attempt 2: Request → Fail
                ↓
             Wait ~1s
                ↓
   Attempt 3: Request → Success ✓

Wait Time Formula
~~~~~~~~~~~~~~~~~

The base wait time follows the formula:

.. code-block:: python

   wait_time = (2 ** attempt) * 0.5  # seconds

   # Actual wait times:
   # Attempt 1: (2^0) * 0.5 = 0.5 seconds
   # Attempt 2: (2^1) * 0.5 = 1.0 seconds
   # Attempt 3: (2^2) * 0.5 = 2.0 seconds
   # Attempt 4: (2^3) * 0.5 = 4.0 seconds
   # Attempt 5: (2^4) * 0.5 = 8.0 seconds

Jitter
~~~~~~

A small random jitter is added to prevent thundering herd:

.. code-block:: python

   import random

   actual_wait = wait_time * (0.5 + random.random() * 0.5)
   # Randomly varies wait time by ±25%

Retry Conditions
----------------

When Retries Happen
~~~~~~~~~~~~~~~~~~~

The SDK retries for these conditions:

✅ **Network Errors**:

.. code-block:: python

   # Connection timeout
   requests.exceptions.ConnectTimeout

   # DNS resolution failure
   socket.gaierror

   # Connection refused
   ConnectionRefusedError

✅ **Rate Limiting** (429):

.. code-block:: python

   # Too many requests
   HTTP 429 Too Many Requests

✅ **Server Errors** (5xx):

.. code-block:: python

   # Internal server error
   HTTP 500 Internal Server Error

   # Bad gateway
   HTTP 502 Bad Gateway

   # Service unavailable
   HTTP 503 Service Unavailable

   # Gateway timeout
   HTTP 504 Gateway Timeout

When Retries DON'T Happen
~~~~~~~~~~~~~~~~~~~~~~~~~~

The SDK does NOT retry for these conditions:

❌ **Client Errors** (4xx):

.. code-block:: python

   # Bad request - fix your code!
   HTTP 400 Bad Request

   # Unauthorized - check credentials
   HTTP 401 Unauthorized

   # Forbidden - check permissions
   HTTP 403 Forbidden

   # Not found - resource doesn't exist
   HTTP 404 Not Found

❌ **Successful Responses** (2xx):

.. code-block:: python

   HTTP 200 OK
   HTTP 201 Created
   HTTP 204 No Content

Configuration
-------------

Default Configuration
~~~~~~~~~~~~~~~~~~~~~

By default, the SDK retries up to **2 times** (3 total attempts):

.. code-block:: python

   client = NaverCommerce()  # max_retries=2 by default

Custom Retry Count
~~~~~~~~~~~~~~~~~~

Adjust the maximum number of retries:

.. code-block:: python

   # No retries (fail fast)
   client = NaverCommerce(max_retries=0)

   # Standard retries
   client = NaverCommerce(max_retries=2)

   # Aggressive retries
   client = NaverCommerce(max_retries=5)

Total Attempt Count
~~~~~~~~~~~~~~~~~~~

Total attempts = 1 initial + max_retries:

.. code-block:: python

   # max_retries=0 → 1 total attempt
   client = NaverCommerce(max_retries=0)

   # max_retries=2 → 3 total attempts
   client = NaverCommerce(max_retries=2)

   # max_retries=5 → 6 total attempts
   client = NaverCommerce(max_retries=5)

Use Case Examples
-----------------

High Reliability
~~~~~~~~~~~~~~~~

For critical operations, use more retries:

.. code-block:: python

   # Tolerate transient failures
   client = NaverCommerce(
       max_retries=5,      # More retries
       timeout=120         # Longer timeout
   )

   # Critical order confirmation
   result = client.orders.confirm(product_order_ids=order_ids)

Fast Failure
~~~~~~~~~~~~

For operations where you want to fail quickly:

.. code-block:: python

   # Detect problems immediately
   client = NaverCommerce(
       max_retries=0,      # No retries
       timeout=10          # Short timeout
   )

   # Health check
   try:
       client.seller.account()
       print("API is healthy")
   except APIError:
       print("API is down")

Balanced Approach
~~~~~~~~~~~~~~~~~

Default settings work well for most cases:

.. code-block:: python

   # Reasonable balance
   client = NaverCommerce(
       max_retries=2,      # Some retries
       timeout=60          # Standard timeout
   )

Retry Behavior by Error Type
-----------------------------

Network Errors
~~~~~~~~~~~~~~

**Behavior**: Always retried up to max_retries

.. code-block:: python

   # Network error → retry automatically
   try:
       account = client.seller.account()
   except APIConnectionError as e:
       # Only raised after all retries exhausted
       print(f"Failed after {max_retries} retries: {e}")

Rate Limiting (429)
~~~~~~~~~~~~~~~~~~~

**Behavior**: Retried with exponential backoff

.. code-block:: python

   # Rate limited → wait and retry
   # SDK handles this automatically
   products = client.products.list()

Server Errors (5xx)
~~~~~~~~~~~~~~~~~~~

**Behavior**: Retried (server might recover)

.. code-block:: python

   # Server error → retry automatically
   try:
       orders = client.orders.list(start_date="2024-01-01")
   except InternalServerError as e:
       # Only raised after all retries exhausted
       print(f"Server error persists: {e}")

Client Errors (4xx)
~~~~~~~~~~~~~~~~~~~

**Behavior**: NOT retried (indicates bug in your code)

.. code-block:: python

   # Bad request → immediate error
   try:
       product = client.products.retrieve("invalid_id")
   except NotFoundError:
       # Raised immediately, no retries
       print("Product doesn't exist")

Monitoring Retries
------------------

Log Retry Attempts
~~~~~~~~~~~~~~~~~~

Enable logging to see retry behavior:

.. code-block:: python

   import logging

   logging.basicConfig(
       level=logging.DEBUG,
       format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
   )

   client = NaverCommerce(max_retries=3)
   account = client.seller.account()
   # Logs will show retry attempts

Custom Retry Handler
~~~~~~~~~~~~~~~~~~~~

For advanced monitoring, implement a custom handler:

.. code-block:: python

   import time
   from navercommerce import NaverCommerce, InternalServerError

   def retry_with_monitoring(func, max_retries=3):
       """Custom retry with monitoring."""
       for attempt in range(max_retries + 1):
           try:
               return func()
           except InternalServerError as e:
               if attempt == max_retries:
                   raise
               wait_time = (2 ** attempt) * 0.5
               print(f"Retry {attempt + 1}/{max_retries} after {wait_time}s")
               time.sleep(wait_time)

   client = NaverCommerce(max_retries=0)  # Disable SDK retries

   # Use custom retry
   account = retry_with_monitoring(lambda: client.seller.account())

Best Practices
--------------

1. **Use Default Retries**

   The default (max_retries=2) works well for most cases.

2. **Don't Retry Client Errors**

   400-level errors indicate bugs - fix your code instead of retrying.

3. **Log Retry Events**

   Monitor retry frequency to detect API issues early.

4. **Increase Retries for Critical Operations**

   For important operations, use max_retries=5.

5. **Combine with Circuit Breaker**

   For production, combine retries with circuit breaker pattern.

See Also
--------

- :doc:`../user-guide/error-handling` - Error handling guide
- :doc:`../user-guide/configuration` - Configuration options
- :doc:`../user-guide/best-practices` - Production patterns
