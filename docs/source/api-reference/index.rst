API Reference
=============

Complete API reference documentation auto-generated from source code.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   client
   resources
   types
   exceptions

Overview
--------

This section provides detailed API documentation for all classes, methods, and types in the Naver Commerce SDK.

Main Sections
-------------

:doc:`client`
   Main client classes (``NaverCommerce`` and ``AsyncNaverCommerce``)

:doc:`resources`
   All resource classes (Products, Orders, Seller, etc.)

:doc:`types`
   Pydantic models for requests and responses

:doc:`exceptions`
   Exception hierarchy and error types

Quick Links
-----------

**Clients**:
   - :class:`navercommerce.NaverCommerce` - Synchronous client
   - :class:`navercommerce.AsyncNaverCommerce` - Asynchronous client

**Resources**:
   - :class:`navercommerce.resources.Products` - Product management
   - :class:`navercommerce.resources.Orders` - Order processing
   - :class:`navercommerce.resources.Seller` - Seller information

**Exceptions**:
   - :class:`navercommerce.NaverCommerceError` - Base exception
   - :class:`navercommerce.APIError` - API errors
   - :class:`navercommerce.AuthenticationError` - Auth failures

Navigation Tips
---------------

- Use the search box to find specific classes or methods
- Click on class names to see their full documentation
- Method signatures show type hints for parameters and return values
- Source code links are available for all documented items

Conventions
-----------

Type Hints
~~~~~~~~~~

All methods include type hints:

.. code-block:: python

   def retrieve(self, product_id: str) -> Product:
       """Retrieve a product by ID."""

Docstring Format
~~~~~~~~~~~~~~~~

Docstrings follow Google style:

.. code-block:: python

   def create(self, name: str, price: int) -> Product:
       """Create a new product.

       Args:
           name: Product name
           price: Sale price in won

       Returns:
           Created product

       Raises:
           BadRequestError: If parameters are invalid
           AuthenticationError: If not authenticated
       """
