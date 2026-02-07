Error Handling
==============

The Naver Commerce SDK provides comprehensive error handling with specific exception types mapped to API error conditions.

Exception Hierarchy
-------------------

All SDK exceptions inherit from ``NaverCommerceError``:

.. code-block:: text

   NaverCommerceError (base exception)
   ├── APIError (generic API errors)
   │   ├── APIConnectionError (network/connection failures)
   │   ├── APITimeoutError (request timeout)
   │   └── APIStatusError (HTTP status errors)
   │       ├── BadRequestError (400)
   │       ├── AuthenticationError (401)
   │       ├── PermissionDeniedError (403)
   │       ├── NotFoundError (404)
   │       └── InternalServerError (500)
   └── OAuthError (OAuth-specific errors)
       ├── TokenExpiredError (token expired)
       └── TokenRefreshError (token refresh failed)

Importing Exceptions
--------------------

Import exceptions from the main package:

.. code-block:: python

   from navercommerce import (
       NaverCommerceError,
       APIError,
       APIConnectionError,
       APITimeoutError,
       APIStatusError,
       BadRequestError,
       AuthenticationError,
       PermissionDeniedError,
       NotFoundError,
       InternalServerError,
       OAuthError,
       TokenExpiredError,
       TokenRefreshError,
   )

Common Exception Types
----------------------

BadRequestError (400)
~~~~~~~~~~~~~~~~~~~~~

Raised when the request is malformed or contains invalid parameters:

.. code-block:: python

   from navercommerce import NaverCommerce, BadRequestError

   client = NaverCommerce()

   try:
       product = client.products.create(
           name="Test Product",
           sale_price=-100,  # Invalid: negative price
           category_id="invalid"
       )
   except BadRequestError as e:
       print(f"Bad request: {e.message}")
       print(f"Status code: {e.status_code}")  # 400

       # Check for field-level errors
       if hasattr(e, 'invalid_inputs'):
           for field, error in e.invalid_inputs.items():
               print(f"  {field}: {error}")

AuthenticationError (401)
~~~~~~~~~~~~~~~~~~~~~~~~~~

Raised when authentication fails (invalid credentials):

.. code-block:: python

   from navercommerce import NaverCommerce, AuthenticationError

   try:
       client = NaverCommerce(
           client_id="invalid_id",
           client_secret="invalid_secret"
       )
       account = client.seller.account()
   except AuthenticationError as e:
       print(f"Authentication failed: {e.message}")
       print(f"Status code: {e.status_code}")  # 401

       # Re-check your credentials
       # Update environment variables or credentials

PermissionDeniedError (403)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Raised when the client lacks permission for the requested operation:

.. code-block:: python

   from navercommerce import NaverCommerce, PermissionDeniedError

   client = NaverCommerce()

   try:
       # Try to access endpoint without proper permissions
       result = client.analytics.sales_data()
   except PermissionDeniedError as e:
       print(f"Permission denied: {e.message}")
       # Check API key permissions in Naver developer portal

NotFoundError (404)
~~~~~~~~~~~~~~~~~~~

Raised when the requested resource doesn't exist:

.. code-block:: python

   from navercommerce import NaverCommerce, NotFoundError

   client = NaverCommerce()

   try:
       product = client.products.retrieve("nonexistent_product_id")
   except NotFoundError as e:
       print(f"Product not found: {e.message}")
       # Handle missing resource gracefully

InternalServerError (500)
~~~~~~~~~~~~~~~~~~~~~~~~~

Raised when the Naver API encounters an internal error:

.. code-block:: python

   from navercommerce import NaverCommerce, InternalServerError

   client = NaverCommerce()

   try:
       products = client.products.list()
   except InternalServerError as e:
       print(f"Server error: {e.message}")
       # Retry later or contact Naver support

APIConnectionError
~~~~~~~~~~~~~~~~~~

Raised when network connection fails:

.. code-block:: python

   from navercommerce import NaverCommerce, APIConnectionError

   client = NaverCommerce()

   try:
       account = client.seller.account()
   except APIConnectionError as e:
       print(f"Connection failed: {e.message}")
       # Check internet connection or firewall settings

APITimeoutError
~~~~~~~~~~~~~~~

Raised when the request times out:

.. code-block:: python

   from navercommerce import NaverCommerce, APITimeoutError

   client = NaverCommerce(timeout=5)  # 5 second timeout

   try:
       products = client.products.list()
   except APITimeoutError as e:
       print(f"Request timed out: {e.message}")
       # Increase timeout or retry later

OAuthError
~~~~~~~~~~

Raised when OAuth token operations fail:

.. code-block:: python

   from navercommerce import NaverCommerce, OAuthError, TokenRefreshError

   client = NaverCommerce()

   try:
       account = client.seller.account()
   except TokenRefreshError as e:
       print(f"Token refresh failed: {e.message}")
       # Check credentials and OAuth configuration
   except OAuthError as e:
       print(f"OAuth error: {e.message}")

Basic Error Handling
--------------------

Catch Specific Exceptions
~~~~~~~~~~~~~~~~~~~~~~~~~

Always catch specific exceptions rather than the base exception:

✅ **Good**:

.. code-block:: python

   from navercommerce import NaverCommerce, NotFoundError, BadRequestError

   client = NaverCommerce()

   try:
       product = client.products.retrieve("product_id")
   except NotFoundError:
       print("Product not found - show error message to user")
   except BadRequestError:
       print("Invalid request - check input parameters")

❌ **Bad**:

.. code-block:: python

   try:
       product = client.products.retrieve("product_id")
   except Exception as e:  # Too broad!
       print(f"Error: {e}")

Handle Multiple Exception Types
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use multiple except blocks for different error conditions:

.. code-block:: python

   from navercommerce import (
       NaverCommerce,
       AuthenticationError,
       NotFoundError,
       BadRequestError,
       InternalServerError,
       APIConnectionError,
   )

   client = NaverCommerce()

   try:
       product = client.products.retrieve("product_id")
   except AuthenticationError as e:
       # Handle auth errors (check credentials)
       print(f"Auth failed: {e.message}")
       log_error("authentication_failed", e)
       re_authenticate()
   except NotFoundError as e:
       # Handle missing resources
       print(f"Product not found: {e.message}")
       return None
   except BadRequestError as e:
       # Handle invalid requests
       print(f"Invalid request: {e.message}")
       log_error("bad_request", e)
   except InternalServerError as e:
       # Handle server errors (retry later)
       print(f"Server error: {e.message}")
       schedule_retry()
   except APIConnectionError as e:
       # Handle network errors
       print(f"Connection failed: {e.message}")
       check_network()

Advanced Error Handling
-----------------------

Retry with Exponential Backoff
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Implement custom retry logic for specific operations:

.. code-block:: python

   import time
   from navercommerce import NaverCommerce, InternalServerError, APITimeoutError

   def fetch_product_with_retry(client, product_id, max_retries=3):
       """Fetch product with custom retry logic."""
       for attempt in range(max_retries):
           try:
               return client.products.retrieve(product_id)
           except (InternalServerError, APITimeoutError) as e:
               if attempt == max_retries - 1:
                   # Last attempt failed
                   raise
               # Wait with exponential backoff
               wait_time = 2 ** attempt
               print(f"Retry {attempt + 1}/{max_retries} after {wait_time}s")
               time.sleep(wait_time)

   client = NaverCommerce()
   product = fetch_product_with_retry(client, "product_id")

Error Context and Logging
~~~~~~~~~~~~~~~~~~~~~~~~~~

Extract useful information from exceptions for logging:

.. code-block:: python

   import logging
   from navercommerce import NaverCommerce, APIStatusError

   logger = logging.getLogger(__name__)
   client = NaverCommerce()

   try:
       product = client.products.retrieve("product_id")
   except APIStatusError as e:
       # Log detailed error information
       logger.error(
           "API error occurred",
           extra={
               "error_type": type(e).__name__,
               "status_code": e.status_code,
               "message": e.message,
               "request_id": getattr(e, 'request_id', None),
           }
       )
       raise

Graceful Degradation
~~~~~~~~~~~~~~~~~~~~

Provide fallback behavior when API calls fail:

.. code-block:: python

   from navercommerce import NaverCommerce, APIError

   client = NaverCommerce()

   def get_product_or_default(product_id):
       """Get product or return default placeholder."""
       try:
           return client.products.retrieve(product_id)
       except APIError as e:
           # Log error but don't fail
           print(f"Failed to fetch product: {e.message}")
           # Return placeholder/default
           return {
               "id": product_id,
               "name": "Product unavailable",
               "sale_price": 0,
               "available": False
           }

Async Error Handling
--------------------

Error handling in async code works the same way:

.. code-block:: python

   import asyncio
   from navercommerce import AsyncNaverCommerce, NotFoundError, APIError

   async def main():
       async with AsyncNaverCommerce() as client:
           try:
               product = await client.products.retrieve("product_id")
           except NotFoundError as e:
               print(f"Product not found: {e.message}")
           except APIError as e:
               print(f"API error: {e.message}")

   asyncio.run(main())

Concurrent Error Handling
~~~~~~~~~~~~~~~~~~~~~~~~~~

Handle errors in concurrent async operations:

.. code-block:: python

   import asyncio
   from navercommerce import AsyncNaverCommerce, NotFoundError

   async def fetch_product_safe(client, product_id):
       """Fetch product, return None on error."""
       try:
           return await client.products.retrieve(product_id)
       except NotFoundError:
           print(f"Product {product_id} not found")
           return None

   async def main():
       async with AsyncNaverCommerce() as client:
           product_ids = ["id1", "id2", "id3", "id4"]
           tasks = [fetch_product_safe(client, pid) for pid in product_ids]

           # Gather results (None for failed fetches)
           products = await asyncio.gather(*tasks)

           # Filter out None values
           valid_products = [p for p in products if p is not None]

   asyncio.run(main())

Production Patterns
-------------------

Pattern 1: Error Monitoring
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Integrate with error tracking services:

.. code-block:: python

   import sentry_sdk
   from navercommerce import NaverCommerce, APIError

   sentry_sdk.init("your_sentry_dsn")

   client = NaverCommerce()

   try:
       product = client.products.retrieve("product_id")
   except APIError as e:
       # Capture exception in Sentry
       sentry_sdk.capture_exception(e)
       raise

Pattern 2: Circuit Breaker
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Prevent cascading failures with a circuit breaker:

.. code-block:: python

   from dataclasses import dataclass
   from datetime import datetime, timedelta
   from navercommerce import NaverCommerce, APIError

   @dataclass
   class CircuitBreaker:
       failure_threshold: int = 5
       timeout: int = 60
       failures: int = 0
       last_failure_time: datetime = None

       def call(self, func, *args, **kwargs):
           # Check if circuit is open
           if self.is_open():
               raise Exception("Circuit breaker is open")

           try:
               result = func(*args, **kwargs)
               self.on_success()
               return result
           except APIError as e:
               self.on_failure()
               raise

       def is_open(self):
           if self.failures >= self.failure_threshold:
               if self.last_failure_time:
                   elapsed = datetime.now() - self.last_failure_time
                   return elapsed < timedelta(seconds=self.timeout)
           return False

       def on_success(self):
           self.failures = 0

       def on_failure(self):
           self.failures += 1
           self.last_failure_time = datetime.now()

   # Usage
   client = NaverCommerce()
   circuit_breaker = CircuitBreaker()

   try:
       product = circuit_breaker.call(
           client.products.retrieve,
           "product_id"
       )
   except Exception as e:
       print(f"Circuit breaker: {e}")

Pattern 3: Fallback Chain
~~~~~~~~~~~~~~~~~~~~~~~~~~

Try multiple strategies in sequence:

.. code-block:: python

   from navercommerce import NaverCommerce, NotFoundError, APIError

   client = NaverCommerce()

   def get_product_with_fallback(product_id):
       # Try primary method
       try:
           return client.products.retrieve(product_id)
       except NotFoundError:
           pass

       # Try alternative method
       try:
           products = client.products.list()
           for p in products:
               if p.id == product_id:
                   return p
       except APIError:
           pass

       # Final fallback: cached/default
       return get_cached_product(product_id)

Best Practices
--------------

1. **Catch Specific Exceptions**

   Always catch the most specific exception type possible.

2. **Don't Silence Errors**

   Log errors even if you handle them gracefully.

3. **Provide Context**

   Include useful information in error messages and logs.

4. **Retry Transient Failures**

   Automatically retry network errors and server errors.

5. **Fail Fast for Client Errors**

   Don't retry 400-level errors - they indicate bugs in your code.

6. **Monitor Error Rates**

   Track error frequency to detect issues early.

7. **Test Error Paths**

   Write tests for error handling, not just success cases.

8. **Document Error Behavior**

   Document which exceptions each function might raise.

Common Pitfalls
---------------

❌ **Catching Too Broad**:

.. code-block:: python

   try:
       product = client.products.retrieve("id")
   except Exception:  # Don't do this!
       pass

✅ **Catch Specific**:

.. code-block:: python

   try:
       product = client.products.retrieve("id")
   except NotFoundError:
       # Handle missing product
       pass

❌ **Ignoring Errors**:

.. code-block:: python

   try:
       client.products.delete("id")
   except:  # Don't ignore errors!
       pass

✅ **Log and Handle**:

.. code-block:: python

   try:
       client.products.delete("id")
   except APIError as e:
       logger.error(f"Failed to delete product: {e}")
       raise

Summary
-------

- Use specific exception types for precise error handling
- Log errors with context for debugging
- Retry transient failures (network, server errors)
- Don't retry client errors (400-level)
- Implement monitoring and alerting for production
- Test error handling paths

See Also
--------

- :doc:`core-concepts` - Understanding retry logic
- :doc:`best-practices` - Production error handling patterns
- :doc:`../api-reference/exceptions` - Complete exception reference
