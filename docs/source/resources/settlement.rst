Settlement Resource
===================

The Settlement resource provides access to commission details, daily settlement reports, and VAT information.

Available Methods (5)
---------------------

Commission Details
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from navercommerce import NaverCommerce

   client = NaverCommerce()

   commission = client.settlement.get_commission_details(
       start_date="2024-01-01",
       end_date="2024-01-31",
       page=0,
       size=100
   )

   for item in commission:
       print(f"Order ID: {item.order_id}")
       print(f"Commission: {item.commission_amount}원")

Daily Settlement
~~~~~~~~~~~~~~~~

.. code-block:: python

   daily = client.settlement.get_daily_settlement(
       start_date="2024-01-01",
       end_date="2024-01-31"
   )

   for settlement in daily:
       print(f"Date: {settlement.settlement_date}")
       print(f"Amount: {settlement.settlement_amount}원")

VAT Reports
~~~~~~~~~~~

.. code-block:: python

   # Daily VAT report
   vat_daily = client.settlement.get_vat_daily(
       start_date="2024-01-01",
       end_date="2024-01-31"
   )

   # VAT by case
   vat_case = client.settlement.get_vat_case(
       start_date="2024-01-01",
       end_date="2024-01-31"
   )

Case Settlement
~~~~~~~~~~~~~~~

.. code-block:: python

   case_settlement = client.settlement.get_case_settlement(
       start_date="2024-01-01",
       end_date="2024-01-31"
   )

Complete Example
----------------

.. code-block:: python

   from navercommerce import NaverCommerce
   from datetime import datetime, timedelta

   client = NaverCommerce()

   # Get last month's settlement data
   end_date = datetime.now()
   start_date = end_date - timedelta(days=30)

   # Commission details
   commission = client.settlement.get_commission_details(
       start_date=start_date.strftime("%Y-%m-%d"),
       end_date=end_date.strftime("%Y-%m-%d"),
       page=0,
       size=100
   )

   # Daily settlement
   daily = client.settlement.get_daily_settlement(
       start_date=start_date.strftime("%Y-%m-%d"),
       end_date=end_date.strftime("%Y-%m-%d")
   )

   # VAT report
   vat = client.settlement.get_vat_daily(
       start_date=start_date.strftime("%Y-%m-%d"),
       end_date=end_date.strftime("%Y-%m-%d")
   )

   print(f"Commission entries: {len(commission)}")
   print(f"Daily settlements: {len(daily)}")
   print(f"VAT entries: {len(vat)}")

See Also
--------

- :doc:`../api-reference/resources` - Complete API reference
