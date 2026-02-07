Orders Resource
===============

The Orders resource manages the complete order lifecycle including confirmations, shipping, returns, exchanges, and cancellations.

Available Methods (20)
----------------------

Order Listing & Retrieval
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from navercommerce import NaverCommerce

   client = NaverCommerce()

   # List orders by date range
   orders = client.orders.list(
       start_date="2024-01-01",
       end_date="2024-01-31"
   )

   # Get order details
   order = client.orders.retrieve("order_id")

   # List last changed statuses
   statuses = client.orders.list_last_changed_statuses()

Order Confirmation
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Confirm orders
   result = client.orders.confirm(
       product_order_ids=["order_id_1", "order_id_2"]
   )

Shipping & Dispatch
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Dispatch orders
   client.orders.dispatch(
       dispatch_product_orders=[{
           "productOrderId": "order_id",
           "deliveryMethod": "DELIVERY",
           "deliveryCompanyCode": "CJGLS",
           "trackingNumber": "1234567890",
           "dispatchDate": "2024-01-15T10:00:00.000+09:00"
       }]
   )

   # Notify delivery delay
   client.orders.notify_delay(
       product_order_id="order_id",
       dispatch_due_date="2024-01-20",
       delayed_dispatch_reason="Stock shortage"
   )

Return Workflow
~~~~~~~~~~~~~~~

.. code-block:: python

   # 1. Customer requests return
   client.orders.return_request(
       product_order_id="order_id",
       return_reason="CHANGE_MIND"
   )

   # 2. Seller approves return
   client.orders.return_approve(product_order_id="order_id")

   # 3. Handle return receipt
   client.orders.return_receipt(
       product_order_id="order_id",
       return_receive_date="2024-01-25"
   )

   # 4. Withhold return (if needed)
   client.orders.return_withhold(
       product_order_id="order_id",
       withhold_reason="DAMAGED"
   )

Cancel Workflow
~~~~~~~~~~~~~~~

.. code-block:: python

   # 1. Request cancellation
   client.orders.cancel_request(
       product_order_id="order_id",
       cancel_reason="SOLD_OUT"
   )

   # 2. Approve cancellation
   client.orders.cancel_approve(product_order_id="order_id")

Exchange Workflow
~~~~~~~~~~~~~~~~~

.. code-block:: python

   # 1. Approve exchange collection
   client.orders.exchange_collect_approve(
       product_order_id="order_id"
   )

   # 2. Receive collected item
   client.orders.exchange_collect_receipt(
       product_order_id="order_id"
   )

   # 3. Dispatch replacement
   client.orders.exchange_dispatch(
       product_order_id="order_id",
       re_delivery_method="DELIVERY"
   )

   # 4. Withhold exchange (if needed)
   client.orders.exchange_withhold(
       product_order_id="order_id",
       withhold_reason="DAMAGED"
   )

Other Operations
~~~~~~~~~~~~~~~~

.. code-block:: python

   # Change delivery date
   client.orders.change_hope_delivery(
       product_order_id="order_id",
       hope_delivery_ymd="20241231"
   )

   # Change address
   client.orders.change_address(
       product_order_id="order_id",
       new_address="123 New Street",
       zipcode="12345"
   )

Complete Example
----------------

.. code-block:: python

   from navercommerce import NaverCommerce

   client = NaverCommerce()

   # 1. List pending orders
   orders = client.orders.list(
       start_date="2024-01-01",
       end_date="2024-01-31"
   )

   # 2. Confirm orders
   order_ids = [order['productOrderId'] for order in orders]
   client.orders.confirm(product_order_ids=order_ids)

   # 3. Dispatch orders
   for order_id in order_ids:
       client.orders.dispatch(
           dispatch_product_orders=[{
               "productOrderId": order_id,
               "deliveryMethod": "DELIVERY",
               "deliveryCompanyCode": "CJGLS",
               "trackingNumber": f"TRACK{order_id}",
               "dispatchDate": "2024-01-15T10:00:00.000+09:00"
           }]
       )

   print(f"Processed {len(order_ids)} orders")

Best Practices
--------------

1. **Batch Confirmations**: Confirm multiple orders in one call
2. **Track Order Status**: Use ``list_last_changed_statuses()`` to monitor changes
3. **Handle Errors**: Expect and handle order-specific errors gracefully
4. **Validate Dates**: Ensure dates are in the correct format (ISO 8601)

See Also
--------

- :doc:`../api-reference/resources` - Complete API reference
- :doc:`../examples/order-processing` - More examples
