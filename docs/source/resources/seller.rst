Seller Resource
===============

The Seller resource provides access to seller account information, sales channels, and address book.

Available Methods
-----------------

==================  ==================================  ===========
Method              Endpoint                            Description
==================  ==================================  ===========
``account()``       GET /seller/account                 Get seller account information
``channels()``      GET /seller/channels                List sales channels
``addresses()``     GET /seller/addresses               Get address book
==================  ==================================  ===========

Usage Examples
--------------

Get Account Information
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from navercommerce import NaverCommerce

   client = NaverCommerce()

   account = client.seller.account()
   print(f"Seller ID: {account.seller_id}")
   print(f"Seller Name: {account.seller_name}")
   print(f"Business Type: {account.business_type}")

List Sales Channels
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   channels = client.seller.channels()
   for channel in channels:
       print(f"Channel: {channel.channel_name}")
       print(f"Channel No: {channel.channel_no}")
       print(f"Status: {channel.status}")

Get Address Book
~~~~~~~~~~~~~~~~

.. code-block:: python

   addresses = client.seller.addresses()
   for address in addresses:
       print(f"Name: {address.name}")
       print(f"Address: {address.address}")
       print(f"Zipcode: {address.zipcode}")

Async Usage
-----------

.. code-block:: python

   import asyncio
   from navercommerce import AsyncNaverCommerce

   async def main():
       async with AsyncNaverCommerce() as client:
           account = await client.seller.account()
           channels = await client.seller.channels()
           addresses = await client.seller.addresses()

   asyncio.run(main())

See Also
--------

- :doc:`../api-reference/resources` - Full API reference
- :doc:`../getting-started/authentication` - Setting up credentials
