Type Definitions
================

Pydantic models for type-safe requests and responses.

Overview
--------

All API responses are parsed into typed Pydantic models:

.. code-block:: python

   from navercommerce import NaverCommerce
   from navercommerce.types import Account

   client = NaverCommerce()

   # Response is typed
   account: Account = client.seller.account()
   print(account.seller_name)  # IDE autocomplete works!

Seller Types
------------

.. automodule:: navercommerce.types.seller
   :members:
   :undoc-members:
   :show-inheritance:

Product Types
-------------

.. automodule:: navercommerce.types.products
   :members:
   :undoc-members:
   :show-inheritance:

Order Types
-----------

.. automodule:: navercommerce.types.orders
   :members:
   :undoc-members:
   :show-inheritance:

Settlement Types
----------------

.. automodule:: navercommerce.types.settlement
   :members:
   :undoc-members:
   :show-inheritance:

Inquiries Types
---------------

.. automodule:: navercommerce.types.inquiries
   :members:
   :undoc-members:
   :show-inheritance:

Commerce Solutions Types
------------------------

.. automodule:: navercommerce.types.commerce_solutions
   :members:
   :undoc-members:
   :show-inheritance:

Analytics Types
---------------

.. automodule:: navercommerce.types.analytics
   :members:
   :undoc-members:
   :show-inheritance:

Common Types
------------

.. automodule:: navercommerce.types.common
   :members:
   :undoc-members:
   :show-inheritance:

Using Types
-----------

Type Hints
~~~~~~~~~~

Use types for better IDE support:

.. code-block:: python

   from navercommerce import NaverCommerce
   from navercommerce.types import Product

   client = NaverCommerce()

   def process_product(product: Product) -> None:
       print(f"{product.name}: {product.sale_price}원")

   product = client.products.retrieve("product_id")
   process_product(product)

Validation
~~~~~~~~~~

Pydantic validates all data automatically:

.. code-block:: python

   # Invalid data raises validation error
   product = Product(
       name="Test",
       sale_price="invalid"  # Should be int, not str
   )
   # ValidationError: value is not a valid integer

See Also
--------

- `Pydantic Documentation <https://docs.pydantic.dev/>`_
- :doc:`../user-guide/core-concepts` - Type safety overview
