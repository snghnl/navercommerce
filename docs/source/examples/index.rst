Examples
========

Complete, working examples demonstrating common use cases for the Naver Commerce SDK.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   basic-usage
   async-usage
   product-management
   order-processing

Overview
--------

These examples are fully functional Python scripts that you can run directly. All examples are located in the ``examples/`` directory of the repository.

Running the Examples
--------------------

1. **Set up credentials**:

   .. code-block:: bash

      export NAVER_CLIENT_ID="your_client_id"
      export NAVER_CLIENT_SECRET="your_client_secret"

2. **Install the SDK**:

   .. code-block:: bash

      pip install navercommerce

3. **Run an example**:

   .. code-block:: bash

      python examples/basic_usage.py

Example Categories
------------------

:doc:`basic-usage`
   Synchronous client usage, seller info, and basic operations

:doc:`async-usage`
   Asynchronous client usage with concurrent operations

:doc:`product-management`
   Complete product CRUD operations and management

:doc:`order-processing`
   Order lifecycle from listing to fulfillment

Next Steps
----------

After exploring these examples:

- Read the :doc:`../user-guide/index` for in-depth concepts
- Check the :doc:`../resources/index` for specific resource documentation
- Review the :doc:`../api-reference/index` for complete API details
