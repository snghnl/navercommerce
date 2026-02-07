Basic Usage
===========

This example demonstrates basic synchronous usage of the Naver Commerce SDK.

Overview
--------

This example covers:

- Initializing the synchronous client
- Getting seller account information
- Listing sales channels
- Retrieving the address book
- Proper resource cleanup with context managers

Complete Code
-------------

.. literalinclude:: ../../../examples/basic_usage.py
   :language: python
   :linenos:

Walkthrough
-----------

1. **Import the Client**

   The example imports ``NaverCommerce``, the main synchronous client:

   .. code-block:: python

      from navercommerce import NaverCommerce

2. **Initialize Client**

   The client is initialized using environment variables for credentials:

   .. code-block:: python

      client = NaverCommerce()

   This automatically reads ``NAVER_CLIENT_ID`` and ``NAVER_CLIENT_SECRET`` from the environment.

3. **Get Seller Information**

   Retrieve seller account details:

   .. code-block:: python

      account = client.seller.account()
      print(f"Seller: {account.seller_name}")

4. **List Sales Channels**

   Get all sales channels for the seller:

   .. code-block:: python

      channels = client.seller.channels()
      for channel in channels:
          print(f"Channel: {channel.channel_name}")

5. **Get Address Book**

   Retrieve saved addresses:

   .. code-block:: python

      addresses = client.seller.addresses()

6. **Resource Cleanup**

   Use context managers for automatic cleanup:

   .. code-block:: python

      with NaverCommerce() as client:
          # All operations
          pass
      # Client closed automatically

Running the Example
-------------------

1. Set credentials:

   .. code-block:: bash

      export NAVER_CLIENT_ID="your_client_id"
      export NAVER_CLIENT_SECRET="your_client_secret"

2. Run the script:

   .. code-block:: bash

      python examples/basic_usage.py

Expected Output
---------------

.. code-block:: text

   Seller: Your Seller Name
   Seller ID: seller123

   Sales Channels:
   Channel: Main Channel (ID: 12345)

   Address Book:
   Address 1: 123 Main St, Seoul

Related Examples
----------------

- :doc:`async-usage` - Async version of this example
- :doc:`product-management` - Working with products

See Also
--------

- :doc:`../getting-started/quickstart` - Quick start guide
- :doc:`../resources/seller` - Seller resource documentation
