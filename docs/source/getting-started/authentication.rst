Authentication
==============

The Naver Commerce SDK uses OAuth 2.0 for authentication. You'll need to obtain API credentials from the Naver Commerce developer portal.

Getting API Credentials
------------------------

1. Log in to the `Naver Commerce <https://commerce.naver.com/>`_ developer portal
2. Create a new application or select an existing one
3. Note your **Client ID** and **Client Secret**
4. Configure the OAuth 2.0 redirect URI (if using the authorization code flow)

Authentication Methods
----------------------

The SDK supports two methods for providing credentials:

Method 1: Direct Credentials
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pass credentials directly when initializing the client:

.. code-block:: python

   from navercommerce import NaverCommerce

   client = NaverCommerce(
       client_id="your_client_id",
       client_secret="your_client_secret"
   )

Method 2: Environment Variables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Set credentials as environment variables:

.. code-block:: bash

   export NAVER_CLIENT_ID="your_client_id"
   export NAVER_CLIENT_SECRET="your_client_secret"

Then initialize the client without parameters:

.. code-block:: python

   from navercommerce import NaverCommerce

   client = NaverCommerce()  # Automatically reads from environment

Using a .env File
~~~~~~~~~~~~~~~~~

For local development, you can use a ``.env`` file:

.. code-block:: bash

   # .env
   NAVER_CLIENT_ID=your_client_id
   NAVER_CLIENT_SECRET=your_client_secret

The SDK will automatically load variables from ``.env`` files in your project directory.

.. warning::

   Never commit your ``.env`` file or credentials to version control. Add ``.env`` to your ``.gitignore`` file.

OAuth 2.0 Flow
--------------

The SDK automatically handles the OAuth 2.0 client credentials flow:

1. **Token Request**: On first API call, the SDK requests an access token using your client credentials
2. **Token Caching**: The access token is cached in memory for reuse
3. **Automatic Refresh**: When the token expires, the SDK automatically requests a new one
4. **Thread-Safe**: Token management is thread-safe for concurrent requests

.. code-block:: python

   from navercommerce import NaverCommerce

   client = NaverCommerce(
       client_id="your_client_id",
       client_secret="your_client_secret"
   )

   # First call: SDK fetches access token automatically
   account = client.seller.account()

   # Subsequent calls: SDK reuses cached token
   channels = client.seller.channels()

   # When token expires: SDK automatically refreshes it
   # You don't need to handle this manually

Token Lifecycle
---------------

Access tokens from Naver Commerce API typically have a limited lifetime (e.g., 24 hours). The SDK handles this automatically:

- **Automatic refresh**: Tokens are refreshed when they expire
- **Retry on auth failure**: If a request fails with ``401 Unauthorized``, the SDK refreshes the token and retries
- **No manual management**: You never need to manually refresh or manage tokens

Security Best Practices
-----------------------

1. **Never hardcode credentials**

   ❌ Bad:

   .. code-block:: python

      client = NaverCommerce(
          client_id="ABC123",  # Hardcoded!
          client_secret="secret123"
      )

   ✅ Good:

   .. code-block:: python

      import os

      client = NaverCommerce(
          client_id=os.getenv("NAVER_CLIENT_ID"),
          client_secret=os.getenv("NAVER_CLIENT_SECRET")
      )

2. **Use environment variables in production**

   Set environment variables in your deployment platform (e.g., AWS, Heroku, Docker) rather than using ``.env`` files.

3. **Restrict API permissions**

   Only grant your application the minimum necessary permissions in the Naver Commerce developer portal.

4. **Rotate credentials regularly**

   Periodically rotate your client secret for enhanced security.

Error Handling
--------------

The SDK provides specific exceptions for authentication errors:

.. code-block:: python

   from navercommerce import NaverCommerce, AuthenticationError, OAuthError

   client = NaverCommerce(
       client_id="invalid_id",
       client_secret="invalid_secret"
   )

   try:
       account = client.seller.account()
   except AuthenticationError as e:
       print(f"Authentication failed: {e.message}")
       print(f"Status code: {e.status_code}")
   except OAuthError as e:
       print(f"OAuth error: {e.message}")

Common authentication errors:

- ``AuthenticationError``: Invalid credentials (401)
- ``OAuthError``: Token request or refresh failed
- ``TokenExpiredError``: Token expired (automatically handled by retry)
- ``TokenRefreshError``: Failed to refresh token

Next Steps
----------

Now that you have authentication set up, try the :doc:`quickstart` to make your first API calls.

See Also
--------

- :doc:`../advanced/oauth-flow` - Deep dive into OAuth 2.0 implementation
- :doc:`../user-guide/error-handling` - Comprehensive error handling guide
- :doc:`../user-guide/configuration` - Advanced configuration options
