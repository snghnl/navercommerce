Best Practices
==============

This guide covers production-ready patterns and best practices for using the Naver Commerce SDK.

Credential Management
---------------------

Use Environment Variables
~~~~~~~~~~~~~~~~~~~~~~~~~

Never hardcode credentials in your source code:

❌ **Bad**:

.. code-block:: python

   client = NaverCommerce(
       client_id="ABC123",  # Hardcoded!
       client_secret="secret123"
   )

✅ **Good**:

.. code-block:: python

   import os

   client = NaverCommerce(
       client_id=os.getenv("NAVER_CLIENT_ID"),
       client_secret=os.getenv("NAVER_CLIENT_SECRET")
   )

✅ **Better** (SDK does this automatically):

.. code-block:: python

   # Reads from environment automatically
   client = NaverCommerce()

Secure Credential Storage
~~~~~~~~~~~~~~~~~~~~~~~~~~

- **Development**: Use ``.env`` files (excluded from git)
- **Production**: Use secrets management (AWS Secrets Manager, HashiCorp Vault, etc.)
- **CI/CD**: Use encrypted environment variables

.. code-block:: bash

   # .gitignore
   .env
   .env.local
   *.pem
   *.key

Rotate Credentials Regularly
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Implement periodic credential rotation:

.. code-block:: python

   import os
   from datetime import datetime
   from navercommerce import NaverCommerce

   def get_client():
       """Get client with credential rotation check."""
       # Check if credentials need rotation
       last_rotation = os.getenv("CREDENTIALS_LAST_ROTATED")
       if should_rotate(last_rotation):
           rotate_credentials()

       return NaverCommerce()

Resource Management
-------------------

Use Context Managers
~~~~~~~~~~~~~~~~~~~~

Always use context managers for automatic cleanup:

✅ **Synchronous**:

.. code-block:: python

   with NaverCommerce() as client:
       account = client.seller.account()
       products = client.products.list()
   # Client closed automatically

✅ **Asynchronous**:

.. code-block:: python

   async with AsyncNaverCommerce() as client:
       account = await client.seller.account()
       products = await client.products.list()
   # Client closed automatically

Reuse Client Instances
~~~~~~~~~~~~~~~~~~~~~~

Create one client instance and reuse it:

✅ **Good**:

.. code-block:: python

   # Create once
   client = NaverCommerce()

   # Reuse for multiple operations
   for product_id in product_ids:
       product = client.products.retrieve(product_id)

   # Clean up
   client.close()

❌ **Bad** (creates new client every time):

.. code-block:: python

   for product_id in product_ids:
       client = NaverCommerce()  # Don't do this!
       product = client.products.retrieve(product_id)
       client.close()

Singleton Pattern for Web Applications
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In web applications, create a single client instance:

.. code-block:: python

   # app.py (FastAPI example)
   from fastapi import FastAPI
   from navercommerce import AsyncNaverCommerce

   app = FastAPI()
   naver_client = None

   @app.on_event("startup")
   async def startup():
       global naver_client
       naver_client = AsyncNaverCommerce()

   @app.on_event("shutdown")
   async def shutdown():
       if naver_client:
           await naver_client.close()

   @app.get("/products/{product_id}")
   async def get_product(product_id: str):
       return await naver_client.products.retrieve(product_id)

Error Handling
--------------

Handle Errors Gracefully
~~~~~~~~~~~~~~~~~~~~~~~~

Always handle specific exception types:

.. code-block:: python

   from navercommerce import (
       NaverCommerce,
       NotFoundError,
       BadRequestError,
       InternalServerError,
       APIConnectionError,
   )

   client = NaverCommerce()

   try:
       product = client.products.retrieve(product_id)
   except NotFoundError:
       # Resource missing - return 404 to user
       return {"error": "Product not found"}, 404
   except BadRequestError as e:
       # Invalid request - return 400 to user
       return {"error": e.message}, 400
   except InternalServerError:
       # Server error - retry or return 503
       return {"error": "Service unavailable"}, 503
   except APIConnectionError:
       # Network error - retry or return 503
       return {"error": "Connection failed"}, 503

Log Errors with Context
~~~~~~~~~~~~~~~~~~~~~~~

Include useful context in error logs:

.. code-block:: python

   import logging
   from navercommerce import NaverCommerce, APIError

   logger = logging.getLogger(__name__)
   client = NaverCommerce()

   try:
       product = client.products.retrieve(product_id)
   except APIError as e:
       logger.error(
           "Failed to retrieve product",
           extra={
               "product_id": product_id,
               "error_type": type(e).__name__,
               "status_code": getattr(e, 'status_code', None),
               "message": e.message,
           }
       )
       raise

Implement Retry Logic for Critical Operations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Add custom retry logic for important operations:

.. code-block:: python

   import time
   from navercommerce import NaverCommerce, InternalServerError

   def critical_operation_with_retry(client, max_retries=3):
       """Critical operation with custom retry logic."""
       for attempt in range(max_retries):
           try:
               return client.orders.confirm(order_ids)
           except InternalServerError as e:
               if attempt == max_retries - 1:
                   logger.critical(
                       "Critical operation failed after all retries",
                       extra={"order_ids": order_ids, "error": str(e)}
                   )
                   raise
               wait_time = 2 ** attempt
               time.sleep(wait_time)

Performance Optimization
------------------------

Use Async for Concurrent Operations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For concurrent requests, async is faster than threading:

✅ **Async** (fastest):

.. code-block:: python

   import asyncio
   from navercommerce import AsyncNaverCommerce

   async def fetch_products(product_ids):
       async with AsyncNaverCommerce() as client:
           tasks = [client.products.retrieve(pid) for pid in product_ids]
           return await asyncio.gather(*tasks)

   # Fetch 100 products concurrently (~1-2 seconds)
   products = asyncio.run(fetch_products(product_ids))

Batch Operations Where Possible
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use batch endpoints instead of individual calls:

✅ **Good** (single request):

.. code-block:: python

   # Confirm multiple orders at once
   result = client.orders.confirm(
       product_order_ids=["id1", "id2", "id3"]
   )

❌ **Bad** (multiple requests):

.. code-block:: python

   for order_id in order_ids:
       client.orders.confirm([order_id])

Implement Caching for Read-Heavy Operations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Cache frequently accessed data:

.. code-block:: python

   from functools import lru_cache
   from navercommerce import NaverCommerce

   client = NaverCommerce()

   @lru_cache(maxsize=1000)
   def get_product_cached(product_id: str):
       """Get product with in-memory caching."""
       return client.products.retrieve(product_id)

   # First call: fetches from API
   product1 = get_product_cached("product_id")

   # Second call: returns cached result
   product2 = get_product_cached("product_id")

Use Pagination Efficiently
~~~~~~~~~~~~~~~~~~~~~~~~~~~

For large datasets, process pages incrementally:

.. code-block:: python

   from navercommerce import NaverCommerce

   client = NaverCommerce()

   def process_all_products(batch_size=100):
       """Process all products in batches."""
       page = 1
       while True:
           products = client.products.list(page=page, size=batch_size)
           if not products:
               break

           # Process this batch
           for product in products:
               process_product(product)

           page += 1

Security
--------

Validate Input Data
~~~~~~~~~~~~~~~~~~~

Always validate user input before passing to the SDK:

.. code-block:: python

   from navercommerce import NaverCommerce

   def create_product(name: str, price: int):
       # Validate input
       if not name or len(name) > 100:
           raise ValueError("Invalid product name")

       if price < 0:
           raise ValueError("Price cannot be negative")

       # Input validated - safe to call API
       client = NaverCommerce()
       return client.products.create(
           name=name,
           sale_price=price,
           # ... other fields
       )

Limit API Permissions
~~~~~~~~~~~~~~~~~~~~~

Request only the minimum necessary API permissions in the Naver developer portal.

Monitor for Suspicious Activity
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Implement monitoring for unusual patterns:

.. code-block:: python

   import logging

   logger = logging.getLogger(__name__)

   def monitor_api_usage(operation: str):
       """Monitor API usage for anomalies."""
       # Log API calls
       logger.info(f"API call: {operation}")

       # Check rate limits
       if exceeds_rate_limit():
           logger.warning("Rate limit threshold exceeded")
           alert_security_team()

   # Use with API calls
   monitor_api_usage("products.create")
   product = client.products.create(...)

Testing
-------

Use Mock Servers for Tests
~~~~~~~~~~~~~~~~~~~~~~~~~~

Test with mock HTTP responses using respx:

.. code-block:: python

   import respx
   from httpx import Response
   from navercommerce import NaverCommerce

   @respx.mock
   def test_get_account():
       # Mock the API response
       respx.get("https://api.commerce.naver.com/seller/account").mock(
           return_value=Response(200, json={
               "sellerId": "test123",
               "sellerName": "Test Seller"
           })
       )

       client = NaverCommerce(
           client_id="test",
           client_secret="test"
       )

       account = client.seller.account()
       assert account.seller_id == "test123"

Test Error Handling
~~~~~~~~~~~~~~~~~~~

Test error paths, not just success cases:

.. code-block:: python

   import pytest
   from navercommerce import NaverCommerce, NotFoundError

   @respx.mock
   def test_product_not_found():
       # Mock 404 response
       respx.get("https://api.commerce.naver.com/products/invalid").mock(
           return_value=Response(404, json={"error": "Not found"})
       )

       client = NaverCommerce()

       with pytest.raises(NotFoundError):
           client.products.retrieve("invalid")

Integration Tests with Test Credentials
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use separate test credentials for integration tests:

.. code-block:: python

   # tests/integration/test_products.py
   import os
   import pytest
   from navercommerce import NaverCommerce

   @pytest.mark.integration
   def test_create_product_integration():
       """Integration test using real API (test environment)."""
       client = NaverCommerce(
           client_id=os.getenv("NAVER_TEST_CLIENT_ID"),
           client_secret=os.getenv("NAVER_TEST_CLIENT_SECRET"),
           base_url=os.getenv("NAVER_TEST_BASE_URL"),
       )

       product = client.products.create(
           name="Test Product",
           sale_price=1000,
           # ... other fields
       )

       assert product.name == "Test Product"

       # Clean up
       client.products.delete(product.id)

Monitoring and Logging
----------------------

Structured Logging
~~~~~~~~~~~~~~~~~~

Use structured logging for better searchability:

.. code-block:: python

   import logging
   import json
   from navercommerce import NaverCommerce

   logger = logging.getLogger(__name__)

   class StructuredLogger:
       @staticmethod
       def log_api_call(operation: str, **kwargs):
           logger.info(json.dumps({
               "event": "api_call",
               "operation": operation,
               **kwargs
           }))

   # Usage
   client = NaverCommerce()
   StructuredLogger.log_api_call(
       "products.list",
       page=1,
       size=20
   )
   products = client.products.list(page=1, size=20)

Track API Performance
~~~~~~~~~~~~~~~~~~~~~

Monitor API call performance:

.. code-block:: python

   import time
   from navercommerce import NaverCommerce

   def track_performance(operation):
       """Decorator to track API call performance."""
       def decorator(func):
           def wrapper(*args, **kwargs):
               start = time.time()
               try:
                   result = func(*args, **kwargs)
                   duration = time.time() - start
                   logger.info(f"{operation} took {duration:.2f}s")
                   return result
               except Exception as e:
                   duration = time.time() - start
                   logger.error(f"{operation} failed after {duration:.2f}s: {e}")
                   raise
           return wrapper
       return decorator

   @track_performance("get_products")
   def get_products():
       client = NaverCommerce()
       return client.products.list()

Implement Health Checks
~~~~~~~~~~~~~~~~~~~~~~~~

Add health check endpoints:

.. code-block:: python

   from fastapi import FastAPI
   from navercommerce import AsyncNaverCommerce, APIError

   app = FastAPI()

   @app.get("/health")
   async def health_check():
       """Check if Naver API is accessible."""
       try:
           async with AsyncNaverCommerce() as client:
               await client.seller.account()
           return {"status": "healthy", "naver_api": "connected"}
       except APIError as e:
           return {
               "status": "unhealthy",
               "naver_api": "disconnected",
               "error": str(e)
           }, 503

Production Deployment
---------------------

Use Environment-Specific Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import os
   from navercommerce import NaverCommerce

   env = os.getenv("APP_ENV", "development")

   if env == "production":
       client = NaverCommerce(
           timeout=60,
           max_retries=3
       )
   elif env == "staging":
       client = NaverCommerce(
           timeout=90,
           max_retries=2
       )
   else:  # development
       client = NaverCommerce(
           timeout=120,
           max_retries=0
       )

Implement Circuit Breakers
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Prevent cascading failures:

.. code-block:: python

   from datetime import datetime, timedelta

   class CircuitBreaker:
       def __init__(self, failure_threshold=5, timeout=60):
           self.failure_threshold = failure_threshold
           self.timeout = timeout
           self.failures = 0
           self.last_failure = None
           self.state = "closed"  # closed, open, half_open

       def call(self, func):
           if self.state == "open":
               if datetime.now() - self.last_failure > timedelta(seconds=self.timeout):
                   self.state = "half_open"
               else:
                   raise Exception("Circuit breaker is open")

           try:
               result = func()
               self.on_success()
               return result
           except Exception as e:
               self.on_failure()
               raise

       def on_success(self):
           self.failures = 0
           self.state = "closed"

       def on_failure(self):
           self.failures += 1
           self.last_failure = datetime.now()
           if self.failures >= self.failure_threshold:
               self.state = "open"

Rate Limiting
~~~~~~~~~~~~~

Implement client-side rate limiting:

.. code-block:: python

   import time
   from collections import deque

   class RateLimiter:
       def __init__(self, max_calls: int, period: int):
           self.max_calls = max_calls
           self.period = period
           self.calls = deque()

       def __call__(self, func):
           def wrapper(*args, **kwargs):
               now = time.time()

               # Remove old calls
               while self.calls and self.calls[0] < now - self.period:
                   self.calls.popleft()

               # Check rate limit
               if len(self.calls) >= self.max_calls:
                   sleep_time = self.period - (now - self.calls[0])
                   time.sleep(sleep_time)

               self.calls.append(time.time())
               return func(*args, **kwargs)

           return wrapper

   # Usage: Max 100 calls per 60 seconds
   rate_limiter = RateLimiter(max_calls=100, period=60)

   @rate_limiter
   def get_products():
       client = NaverCommerce()
       return client.products.list()

Summary
-------

Key Best Practices:

1. **Security**: Use environment variables, never hardcode credentials
2. **Resource Management**: Use context managers, reuse client instances
3. **Error Handling**: Handle specific exceptions, log with context
4. **Performance**: Use async for concurrency, implement caching
5. **Testing**: Mock HTTP calls, test error paths
6. **Monitoring**: Structured logging, performance tracking, health checks
7. **Production**: Environment-specific config, circuit breakers, rate limiting

See Also
--------

- :doc:`error-handling` - Comprehensive error handling guide
- :doc:`configuration` - Configuration options
- :doc:`sync-vs-async` - Choosing sync vs async
