Commerce Solutions Resource
===========================

The Commerce Solutions resource manages subscription services and external transactions.

Available Methods (8)
---------------------

Subscription Management
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from navercommerce import NaverCommerce

   client = NaverCommerce()

   # Approve subscription
   client.commerce_solutions.approve_subscription(
       account_uid="12345"
   )

   # Reject subscription
   client.commerce_solutions.reject_subscription(
       account_uid="12345"
   )

   # Request unsubscription
   client.commerce_solutions.request_unsubscription(
       account_uid="12345"
   )

   # Approve unsubscription
   client.commerce_solutions.approve_unsubscription(
       account_uid="12345"
   )

   # Get subscription details
   subscription = client.commerce_solutions.get_subscription(
       account_uid="12345"
   )

Seller Information
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Get seller info from token
   seller_info = client.commerce_solutions.get_seller_info_from_token(
       token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
   )

Transaction Management
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # List transactions
   transactions = client.commerce_solutions.list_transactions(
       page=0,
       size=20
   )

   # Create external transaction
   client.commerce_solutions.create_external_transaction(
       transaction_type="PAYMENT",
       amount=10000,
       description="External payment"
   )

Complete Example
----------------

.. code-block:: python

   from navercommerce import NaverCommerce

   client = NaverCommerce()

   # 1. List pending subscriptions
   transactions = client.commerce_solutions.list_transactions(
       page=0,
       size=100
   )

   # 2. Approve subscription
   account_uid = "customer_account_123"
   client.commerce_solutions.approve_subscription(
       account_uid=account_uid
   )

   # 3. Get subscription details
   subscription = client.commerce_solutions.get_subscription(
       account_uid=account_uid
   )

   print(f"Subscription status: {subscription.status}")

See Also
--------

- :doc:`../api-reference/resources` - Complete API reference
