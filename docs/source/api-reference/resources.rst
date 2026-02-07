Resource Classes
================

Resource classes provide organized access to API endpoints.

Overview
--------

All resources are accessed via the client:

.. code-block:: python

   from navercommerce import NaverCommerce

   client = NaverCommerce()

   # Access resources
   client.seller      # Seller resource
   client.products    # Products resource
   client.orders      # Orders resource
   # ... etc

Seller Resource
---------------

.. autoclass:: navercommerce.resources.Seller
   :members:
   :undoc-members:
   :show-inheritance:

Products Resource
-----------------

.. autoclass:: navercommerce.resources.Products
   :members:
   :undoc-members:
   :show-inheritance:

Products.Metadata
~~~~~~~~~~~~~~~~~

.. autoclass:: navercommerce.resources.products.Metadata
   :members:
   :undoc-members:
   :show-inheritance:

Products.Delivery
~~~~~~~~~~~~~~~~~

.. autoclass:: navercommerce.resources.products.Delivery
   :members:
   :undoc-members:
   :show-inheritance:

Products.Management
~~~~~~~~~~~~~~~~~~~

.. autoclass:: navercommerce.resources.products.Management
   :members:
   :undoc-members:
   :show-inheritance:

Products.Notices
~~~~~~~~~~~~~~~~

.. autoclass:: navercommerce.resources.products.Notices
   :members:
   :undoc-members:
   :show-inheritance:

Products.Images
~~~~~~~~~~~~~~~

.. autoclass:: navercommerce.resources.products.Images
   :members:
   :undoc-members:
   :show-inheritance:

Orders Resource
---------------

.. autoclass:: navercommerce.resources.Orders
   :members:
   :undoc-members:
   :show-inheritance:

Settlement Resource
-------------------

.. autoclass:: navercommerce.resources.Settlement
   :members:
   :undoc-members:
   :show-inheritance:

Inquiries Resource
------------------

.. autoclass:: navercommerce.resources.Inquiries
   :members:
   :undoc-members:
   :show-inheritance:

Inquiries.QnAs
~~~~~~~~~~~~~~

.. autoclass:: navercommerce.resources.inquiries.QnAs
   :members:
   :undoc-members:
   :show-inheritance:

Inquiries.Notices
~~~~~~~~~~~~~~~~~

.. autoclass:: navercommerce.resources.inquiries.Notices
   :members:
   :undoc-members:
   :show-inheritance:

Commerce Solutions Resource
---------------------------

.. autoclass:: navercommerce.resources.CommerceSolutions
   :members:
   :undoc-members:
   :show-inheritance:

Analytics Resource
------------------

.. autoclass:: navercommerce.resources.Analytics
   :members:
   :undoc-members:
   :show-inheritance:

Analytics.Marketing
~~~~~~~~~~~~~~~~~~~

.. autoclass:: navercommerce.resources.analytics.Marketing
   :members:
   :undoc-members:
   :show-inheritance:

Analytics.Sales
~~~~~~~~~~~~~~~

.. autoclass:: navercommerce.resources.analytics.Sales
   :members:
   :undoc-members:
   :show-inheritance:

See Also
--------

- :doc:`../resources/index` - Resource guides with examples
- :doc:`client` - Client classes
- :doc:`types` - Type definitions
