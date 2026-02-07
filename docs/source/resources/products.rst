Products Resource
=================

The Products resource provides comprehensive product management, including CRUD operations, categories, brands, metadata, delivery settings, and images.

Overview
--------

The Products resource is the largest resource with **64 endpoints** organized into sub-resources:

- **Main Methods** (8): CRUD operations, listing, categories
- **Metadata** (25): Brands, attributes, origin areas, manufacturers, models, sizes
- **Delivery** (9): Bundle groups, hope delivery groups, return companies
- **Management** (7): Bulk updates, status changes, stock updates
- **Notices** (2): Product notice types
- **Images** (1): Image uploads

Main Methods
------------

CRUD Operations
~~~~~~~~~~~~~~~

.. code-block:: python

   from navercommerce import NaverCommerce

   client = NaverCommerce()

   # Create product
   product = client.products.create(
       name="Sample Product",
       sale_price=29900,
       category_id="50000000",
       origin_area_code="01",  # Korea
       stock_quantity=100,
       status="SALE"
   )

   # Retrieve product
   product = client.products.retrieve("product_id")

   # Update product
   product = client.products.update(
       "product_id",
       name="Updated Name",
       sale_price=34900
   )

   # Delete product
   client.products.delete("product_id")

Listing Products
~~~~~~~~~~~~~~~~

.. code-block:: python

   # List products with pagination
   products = client.products.list(page=1, size=20)
   for product in products:
       print(f"{product.name}: {product.sale_price}원")

Categories and Brands
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # List all categories
   categories = client.products.list_categories()

   # Get specific category
   category = client.products.get_category("category_id")

   # List brands
   brands = client.products.list_brands()

Metadata Sub-Resource
---------------------

Access product metadata via ``client.products.metadata``.

Brands
~~~~~~

.. code-block:: python

   brands = client.products.metadata.list_brands()

Attributes
~~~~~~~~~~

.. code-block:: python

   # List attributes for category
   attrs = client.products.metadata.list_attributes(category_id="50000000")

   # Get attribute values
   values = client.products.metadata.list_attribute_values(attribute_id="123")

   # Get units for attribute value
   units = client.products.metadata.list_attribute_value_units(attribute_value_id="456")

Origin Areas
~~~~~~~~~~~~

.. code-block:: python

   # List all origin areas
   areas = client.products.metadata.list_origin_areas()

   # Query by code
   areas = client.products.metadata.query_origin_areas(code="01")

   # List sub-areas
   sub_areas = client.products.metadata.list_sub_origin_areas(parent_code="01")

Manufacturers & Models
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   manufacturers = client.products.metadata.list_manufacturers()
   models = client.products.metadata.list_models(category_id="category_id")
   model = client.products.metadata.get_model("model_id")

Delivery Sub-Resource
---------------------

Access delivery settings via ``client.products.delivery``.

Bundle Groups
~~~~~~~~~~~~~

.. code-block:: python

   # List bundle groups
   groups = client.products.delivery.list_bundle_groups()

   # Create bundle group
   group = client.products.delivery.create_bundle_group(
       name="Electronics Bundle"
   )

   # Update bundle group
   group = client.products.delivery.update_bundle_group(
       group_id="group_id",
       name="Updated Bundle"
   )

Management Sub-Resource
-----------------------

Access management operations via ``client.products.management``.

Bulk Operations
~~~~~~~~~~~~~~~

.. code-block:: python

   # Bulk update products
   client.products.management.bulk_update(
       products=[
           {"productId": "123", "salePrice": 10000},
           {"productId": "456", "salePrice": 15000}
       ]
   )

Status & Stock
~~~~~~~~~~~~~~

.. code-block:: python

   # Change product status
   client.products.management.change_status(
       product_id="product_id",
       status="SALE"
   )

   # Update option stock
   client.products.management.update_option_stock(
       product_id="product_id",
       stock_quantity=50
   )

Images Sub-Resource
-------------------

Upload product images via ``client.products.images``.

.. code-block:: python

   # Upload product image
   with open("product.jpg", "rb") as f:
       image = client.products.images.upload(
           file=f.read(),
           image_type="REPRESENTATIVE"
       )
       print(f"Image URL: {image.url}")

Complete Example
----------------

.. code-block:: python

   from navercommerce import NaverCommerce

   client = NaverCommerce()

   # 1. Upload image
   with open("product.jpg", "rb") as f:
       image = client.products.images.upload(
           file=f.read(),
           image_type="REPRESENTATIVE"
       )

   # 2. Create product with image
   product = client.products.create(
       name="New Product",
       sale_price=29900,
       category_id="50000000",
       origin_area_code="01",
       stock_quantity=100,
       status="SALE",
       images=[{
           "url": image.url,
           "imageType": "REPRESENTATIVE"
       }]
   )

   # 3. Update stock
   client.products.management.update_option_stock(
       product_id=product.id,
       stock_quantity=150
   )

   print(f"Created product: {product.name} (ID: {product.id})")

See Also
--------

- :doc:`../api-reference/resources` - Complete API reference
- :doc:`../examples/product-management` - More examples
