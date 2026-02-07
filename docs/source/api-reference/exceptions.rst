Exceptions
==========

Exception hierarchy for error handling.

Exception Hierarchy
-------------------

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

Base Exception
--------------

.. autoexception:: navercommerce.NaverCommerceError
   :members:
   :show-inheritance:

API Exceptions
--------------

.. autoexception:: navercommerce.APIError
   :members:
   :show-inheritance:

.. autoexception:: navercommerce.APIConnectionError
   :members:
   :show-inheritance:

.. autoexception:: navercommerce.APITimeoutError
   :members:
   :show-inheritance:

.. autoexception:: navercommerce.APIStatusError
   :members:
   :show-inheritance:

HTTP Status Exceptions
----------------------

.. autoexception:: navercommerce.BadRequestError
   :members:
   :show-inheritance:

.. autoexception:: navercommerce.AuthenticationError
   :members:
   :show-inheritance:

.. autoexception:: navercommerce.PermissionDeniedError
   :members:
   :show-inheritance:

.. autoexception:: navercommerce.NotFoundError
   :members:
   :show-inheritance:

.. autoexception:: navercommerce.InternalServerError
   :members:
   :show-inheritance:

OAuth Exceptions
----------------

.. autoexception:: navercommerce.OAuthError
   :members:
   :show-inheritance:

.. autoexception:: navercommerce.TokenExpiredError
   :members:
   :show-inheritance:

.. autoexception:: navercommerce.TokenRefreshError
   :members:
   :show-inheritance:

Usage Examples
--------------

Catching Specific Exceptions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from navercommerce import (
       NaverCommerce,
       NotFoundError,
       BadRequestError,
       AuthenticationError
   )

   client = NaverCommerce()

   try:
       product = client.products.retrieve("product_id")
   except NotFoundError:
       print("Product not found")
   except BadRequestError as e:
       print(f"Invalid request: {e.message}")
   except AuthenticationError:
       print("Authentication failed")

Exception Attributes
~~~~~~~~~~~~~~~~~~~~

All exceptions have useful attributes:

.. code-block:: python

   try:
       product = client.products.retrieve("invalid_id")
   except APIStatusError as e:
       print(f"Status: {e.status_code}")
       print(f"Message: {e.message}")
       print(f"Request ID: {e.request_id}")

See Also
--------

- :doc:`../user-guide/error-handling` - Comprehensive error handling guide
- :doc:`../getting-started/quickstart` - Error handling examples
