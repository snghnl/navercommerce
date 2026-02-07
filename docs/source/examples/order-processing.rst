Order Processing
================

This example demonstrates the complete order processing workflow from listing to fulfillment.

Overview
--------

This example covers:

- Listing orders by date range
- Retrieving detailed order information
- Confirming orders
- Dispatching orders with tracking
- Handling returns and cancellations
- Error handling for order operations

Complete Code
-------------

.. literalinclude:: ../../../examples/order_processing.py
   :language: python
   :linenos:

Walkthrough
-----------

1. **List Orders**

   Retrieve orders for a specific date range:

   .. code-block:: python

      orders = client.orders.list(
          start_date="2024-01-01",
          end_date="2024-01-31"
      )

2. **Get Order Details**

   Retrieve detailed information for an order:

   .. code-block:: python

      order = client.orders.retrieve("order_id")
      print(f"Order Date: {order.order_date}")
      print(f"Total Amount: {order.total_amount}원")

3. **Confirm Orders**

   Confirm multiple orders at once:

   .. code-block:: python

      client.orders.confirm(
          product_order_ids=["order_id_1", "order_id_2"]
      )

4. **Dispatch Orders**

   Ship orders with tracking information:

   .. code-block:: python

      client.orders.dispatch(
          dispatch_product_orders=[{
              "productOrderId": "order_id",
              "deliveryMethod": "DELIVERY",
              "deliveryCompanyCode": "CJGLS",
              "trackingNumber": "1234567890",
              "dispatchDate": "2024-01-15T10:00:00.000+09:00"
          }]
      )

Order Workflows
---------------

Return Workflow
~~~~~~~~~~~~~~~

.. code-block:: python

   # 1. Request return
   client.orders.return_request(
       product_order_id="order_id",
       return_reason="CHANGE_MIND"
   )

   # 2. Approve return
   client.orders.return_approve(
       product_order_id="order_id"
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
   client.orders.cancel_approve(
       product_order_id="order_id"
   )

Running the Example
-------------------

1. Set credentials:

   .. code-block:: bash

      export NAVER_CLIENT_ID="your_client_id"
      export NAVER_CLIENT_SECRET="your_client_secret"

2. Run the script:

   .. code-block:: bash

      python examples/order_processing.py

Expected Output
---------------

.. code-block:: text

   Listing orders...
   Found 25 orders

   Processing order: 2024010112345678
   Status: PAYMENT_WAITING

   Confirming orders...
   Confirmed 10 orders

   Dispatching orders...
   Dispatched 10 orders with tracking

   Order processing complete!

Best Practices
--------------

1. **Batch Operations**: Confirm multiple orders in one API call
2. **Error Handling**: Always handle order-specific errors
3. **Status Tracking**: Monitor order status changes
4. **Date Validation**: Ensure dates are in correct format

Related Examples
----------------

- :doc:`basic-usage` - Basic SDK usage
- :doc:`product-management` - Managing products

See Also
--------

- :doc:`../resources/orders` - Orders resource guide
- :doc:`../user-guide/error-handling` - Error handling guide
