Getting Started
===============

This guide will help you get started with the Naver Commerce SDK for Python.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   authentication
   quickstart

Overview
--------

The Naver Commerce SDK provides a production-grade Python interface to the Naver Commerce API, with full support for both synchronous and asynchronous operations. The SDK is designed to be:

- **Type-safe**: Full type hints and Pydantic validation
- **Easy to use**: Intuitive, resource-based API design
- **Reliable**: Automatic retry logic and comprehensive error handling
- **Flexible**: Works with both sync and async code

Quick Example
-------------

Here's a simple example to get you started:

.. code-block:: python

   from navercommerce import NaverCommerce

   # Initialize the client
   client = NaverCommerce(
       client_id="your_client_id",
       client_secret="your_client_secret"
   )

   # Get seller information
   account = client.seller.account()
   print(f"Seller: {account.seller_name}")

   # List sales channels
   channels = client.seller.channels()
   for channel in channels:
       print(f"Channel: {channel.channel_name}")

Next Steps
----------

1. :doc:`installation` - Install the SDK
2. :doc:`authentication` - Set up OAuth 2.0 credentials
3. :doc:`quickstart` - Try your first API calls
4. :doc:`../user-guide/index` - Learn core concepts and best practices
5. :doc:`../resources/index` - Explore available resources
