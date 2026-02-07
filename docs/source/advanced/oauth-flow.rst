OAuth 2.0 Flow
==============

Deep dive into the SDK's OAuth 2.0 implementation.

Overview
--------

The SDK uses OAuth 2.0 Client Credentials flow for authentication:

1. **Token Request**: SDK requests access token using client credentials
2. **Token Storage**: Token is cached in memory
3. **Token Usage**: Token is included in API requests
4. **Token Refresh**: When expired, SDK automatically gets a new token
5. **Retry on Auth Failure**: Failed requests are retried with fresh token

OAuth 2.0 Client Credentials Flow
----------------------------------

The SDK implements the OAuth 2.0 Client Credentials grant type as defined in `RFC 6749 <https://tools.ietf.org/html/rfc6749#section-4.4>`_.

Flow Diagram
~~~~~~~~~~~~

.. code-block:: text

   Client                    Naver OAuth Server         Naver API
     |                              |                      |
     | 1. Token Request             |                      |
     |----------------------------->|                      |
     |   (client_id, client_secret) |                      |
     |                              |                      |
     | 2. Access Token Response     |                      |
     |<-----------------------------|                      |
     |   (access_token, expires_in) |                      |
     |                              |                      |
     | 3. API Request (with token)  |                      |
     |-------------------------------------------------->  |
     |                              |                      |
     | 4. API Response              |                      |
     |<--------------------------------------------------|  |
     |                              |                      |
     | 5. Token Expired (401)       |                      |
     |<--------------------------------------------------|  |
     |                              |                      |
     | 6. Refresh Token Request     |                      |
     |----------------------------->|                      |
     |                              |                      |
     | 7. New Access Token          |                      |
     |<-----------------------------|                      |
     |                              |                      |
     | 8. Retry API Request         |                      |
     |-------------------------------------------------->  |

Token Lifecycle
---------------

Initial Token Acquisition
~~~~~~~~~~~~~~~~~~~~~~~~~~

On the first API call, the SDK:

1. Checks if a token is cached
2. If no token, requests one from OAuth server
3. Caches the token in memory
4. Proceeds with the API request

.. code-block:: python

   client = NaverCommerce()

   # First call: Fetches token automatically
   account = client.seller.account()

Token Caching
~~~~~~~~~~~~~

Tokens are cached in memory for the lifetime of the client instance:

- **In-Memory**: Tokens are stored in the client instance
- **Not Persisted**: Tokens are not saved to disk or database
- **Instance-Specific**: Each client instance has its own token cache

.. code-block:: python

   client = NaverCommerce()

   # First call: Fetches token
   account = client.seller.account()

   # Subsequent calls: Reuses cached token
   channels = client.seller.channels()  # No token request!
   addresses = client.seller.addresses()  # No token request!

Token Expiration Handling
~~~~~~~~~~~~~~~~~~~~~~~~~~

When a token expires:

1. API request returns 401 Unauthorized
2. SDK detects token expiration
3. SDK requests a new token
4. SDK retries the original request
5. User sees no interruption

.. code-block:: python

   client = NaverCommerce()

   # Token expires during this call
   # SDK automatically:
   # 1. Gets new token
   # 2. Retries request
   # 3. Returns result
   account = client.seller.account()

Thread Safety
-------------

Token Manager Implementation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The SDK's token manager is **thread-safe**, allowing concurrent requests from multiple threads:

.. code-block:: python

   import concurrent.futures
   from navercommerce import NaverCommerce

   client = NaverCommerce()

   def get_account():
       return client.seller.account()

   # Safe: Multiple threads can use the same client
   with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
       futures = [executor.submit(get_account) for _ in range(100)]
       results = [f.result() for f in futures]

Thread Safety Mechanisms
~~~~~~~~~~~~~~~~~~~~~~~~~

The SDK uses:

- **Lock-based synchronization**: Prevents race conditions during token refresh
- **Atomic operations**: Token read/write operations are atomic
- **Connection pooling**: httpx handles concurrent HTTP requests safely

Security Considerations
-----------------------

Credential Storage
~~~~~~~~~~~~~~~~~~

**Never hardcode credentials**:

❌ Bad:

.. code-block:: python

   client = NaverCommerce(
       client_id="hardcoded_id",
       client_secret="hardcoded_secret"
   )

✅ Good:

.. code-block:: python

   # Use environment variables
   client = NaverCommerce()

Token Storage
~~~~~~~~~~~~~

Tokens are stored in memory only:

- **Not persisted**: Tokens are never written to disk
- **Process-bound**: Tokens are lost when process exits
- **Instance-bound**: Each client instance has its own token

This is **secure by default** - no risk of token leakage to disk.

Credential Rotation
~~~~~~~~~~~~~~~~~~~

To rotate credentials:

1. Update environment variables or configuration
2. Create a new client instance
3. Old client will continue using old credentials
4. New client will use new credentials

.. code-block:: python

   # Old client (old credentials)
   old_client = NaverCommerce()

   # Update credentials
   os.environ["NAVER_CLIENT_ID"] = "new_client_id"
   os.environ["NAVER_CLIENT_SECRET"] = "new_client_secret"

   # New client (new credentials)
   new_client = NaverCommerce()

Error Handling
--------------

OAuth-Specific Exceptions
~~~~~~~~~~~~~~~~~~~~~~~~~

The SDK raises specific exceptions for OAuth errors:

.. code-block:: python

   from navercommerce import (
       NaverCommerce,
       AuthenticationError,
       OAuthError,
       TokenRefreshError
   )

   try:
       client = NaverCommerce(
           client_id="invalid",
           client_secret="invalid"
       )
       account = client.seller.account()
   except AuthenticationError as e:
       # Invalid credentials
       print(f"Auth failed: {e.message}")
   except TokenRefreshError as e:
       # Token refresh failed
       print(f"Token refresh failed: {e.message}")
   except OAuthError as e:
       # General OAuth error
       print(f"OAuth error: {e.message}")

Automatic Retry on Auth Failure
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The SDK automatically retries requests that fail with 401:

1. Request fails with 401
2. SDK assumes token expired
3. SDK requests new token
4. SDK retries original request
5. If still 401, raises AuthenticationError

.. code-block:: python

   # This handles token expiration automatically
   account = client.seller.account()

Configuration
-------------

Token Request Timeout
~~~~~~~~~~~~~~~~~~~~~

Token requests respect the global timeout setting:

.. code-block:: python

   # 30 second timeout for all requests, including token requests
   client = NaverCommerce(timeout=30)

Custom OAuth Endpoint
~~~~~~~~~~~~~~~~~~~~~

Override the OAuth token endpoint (for testing):

.. code-block:: python

   # Not recommended for production
   client = NaverCommerce(
       base_url="https://custom.oauth.server"
   )

Troubleshooting
---------------

Common Issues
~~~~~~~~~~~~~

**Issue**: "Authentication failed" on first request

- **Cause**: Invalid client ID or secret
- **Solution**: Verify credentials in Naver developer portal

**Issue**: Frequent "Token refresh failed" errors

- **Cause**: Credentials revoked or expired
- **Solution**: Generate new credentials in developer portal

**Issue**: "Token expired" even after retry

- **Cause**: System clock skew
- **Solution**: Synchronize system clock with NTP server

Debug Logging
~~~~~~~~~~~~~

Enable debug logging to see OAuth flow:

.. code-block:: python

   import logging

   logging.basicConfig(level=logging.DEBUG)
   logger = logging.getLogger("navercommerce")

   client = NaverCommerce()
   account = client.seller.account()  # Watch debug output

See Also
--------

- :doc:`../getting-started/authentication` - Basic authentication setup
- :doc:`../user-guide/error-handling` - Error handling guide
- `RFC 6749 - OAuth 2.0 <https://tools.ietf.org/html/rfc6749>`_
