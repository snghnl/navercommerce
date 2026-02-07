Analytics Resource
==================

The Analytics resource provides marketing and sales analytics data.

Sub-Resources
-------------

Marketing Analytics (10 methods)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Access via ``client.analytics.marketing``.

.. code-block:: python

   from navercommerce import NaverCommerce

   client = NaverCommerce()

   # Daily marketing data
   all_daily = client.analytics.marketing.get_all_daily(
       channel_no="12345",
       start_date="2024-01-01",
       end_date="2024-01-31"
   )

   # Detailed marketing data
   all_detail = client.analytics.marketing.get_all_detail(
       channel_no="12345",
       start_date="2024-01-01",
       end_date="2024-01-31"
   )

   # Custom analytics
   custom_detail = client.analytics.marketing.get_custom_detail(
       channel_no="12345",
       start_date="2024-01-01",
       end_date="2024-01-31"
   )

   # Hourly data
   hourly_detail = client.analytics.marketing.get_hourly_detail(
       channel_no="12345",
       start_date="2024-01-01",
       end_date="2024-01-31"
   )

   # Search analytics
   search_keyword = client.analytics.marketing.get_search_keyword(
       channel_no="12345",
       start_date="2024-01-01",
       end_date="2024-01-31"
   )

   # Website analytics
   website_daily = client.analytics.marketing.get_website_daily(
       channel_no="12345",
       start_date="2024-01-01",
       end_date="2024-01-31"
   )

Sales Analytics (6 methods)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Access via ``client.analytics.sales``.

.. code-block:: python

   # Realtime sales
   realtime = client.analytics.sales.get_realtime_daily(
       channel_no="12345"
   )

   # Delivery details
   delivery = client.analytics.sales.get_delivery_detail(
       channel_no="12345",
       start_date="2024-01-01",
       end_date="2024-01-31"
   )

   # Product details
   product = client.analytics.sales.get_product_detail(
       channel_no="12345",
       start_date="2024-01-01",
       end_date="2024-01-31"
   )

   # Hourly sales
   hourly = client.analytics.sales.get_hourly_detail(
       channel_no="12345",
       start_date="2024-01-01",
       end_date="2024-01-31"
   )

   # Shopping analytics
   shopping = client.analytics.sales.get_shopping_page_detail(
       channel_no="12345",
       start_date="2024-01-01",
       end_date="2024-01-31"
   )

Complete Example
----------------

.. code-block:: python

   from navercommerce import NaverCommerce
   from datetime import datetime, timedelta

   client = NaverCommerce()

   # Get channel number
   channels = client.seller.channels()
   channel_no = channels[0].channel_no

   # Date range: last 30 days
   end_date = datetime.now()
   start_date = end_date - timedelta(days=30)

   # Marketing analytics
   marketing_data = client.analytics.marketing.get_all_daily(
       channel_no=channel_no,
       start_date=start_date.strftime("%Y-%m-%d"),
       end_date=end_date.strftime("%Y-%m-%d")
   )

   # Sales analytics
   sales_data = client.analytics.sales.get_product_detail(
       channel_no=channel_no,
       start_date=start_date.strftime("%Y-%m-%d"),
       end_date=end_date.strftime("%Y-%m-%d")
   )

   print(f"Marketing entries: {len(marketing_data)}")
   print(f"Sales entries: {len(sales_data)}")

See Also
--------

- :doc:`../api-reference/resources` - Complete API reference
