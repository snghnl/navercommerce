Resource Guides
===============

Detailed guides for each resource available in the Naver Commerce SDK.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   seller
   products
   orders
   settlement
   inquiries
   commerce-solutions
   analytics

Overview
--------

The SDK organizes API endpoints into **8 resource groups**:

==========================  =================  ==========================================
Resource                    Endpoints          Description
==========================  =================  ==========================================
:doc:`seller`               3                  Seller account, channels, addresses
:doc:`products`             64                 Product CRUD, categories, brands, metadata
:doc:`orders`               20                 Order lifecycle, shipping, returns
:doc:`settlement`           5                  Commission, daily reports, VAT
:doc:`inquiries`            8                  Customer Q&As, seller notices
:doc:`commerce-solutions`   8                  Subscriptions, transactions
:doc:`analytics`            16                 Marketing and sales analytics
==========================  =================  ==========================================

**Total**: 124 endpoints across all resources

Quick Navigation
----------------

**Getting Started**:
   - :doc:`seller` - Start here for account setup
   - :doc:`products` - Manage your product catalog

**Order Management**:
   - :doc:`orders` - Process orders, shipping, returns

**Analytics & Reporting**:
   - :doc:`settlement` - View settlements and commissions
   - :doc:`analytics` - Marketing and sales insights

**Customer Service**:
   - :doc:`inquiries` - Handle customer questions and notices

**Advanced Features**:
   - :doc:`commerce-solutions` - Subscription services

Resource Access Pattern
-----------------------

All resources follow the same access pattern:

.. code-block:: python

   from navercommerce import NaverCommerce

   client = NaverCommerce()

   # Access resources via client
   account = client.seller.account()
   products = client.products.list()
   orders = client.orders.list(start_date="2024-01-01")

Each resource guide includes:

- **Overview**: What the resource does
- **Method Reference**: All available methods
- **Common Use Cases**: Practical examples
- **Best Practices**: Tips for effective usage

Next Steps
----------

Start with the :doc:`seller` guide to set up your account, then explore :doc:`products` and :doc:`orders` for core commerce operations.
