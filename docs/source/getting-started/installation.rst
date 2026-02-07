Installation
============

Requirements
------------

- Python 3.9 or higher
- pip or uv package manager

Installing with pip
-------------------

The easiest way to install the Naver Commerce SDK is using pip:

.. code-block:: bash

   pip install navercommerce

Installing with uv
------------------

If you're using `uv <https://github.com/astral-sh/uv>`_ (recommended for faster dependency resolution):

.. code-block:: bash

   uv add navercommerce

Installing from Source
----------------------

To install the latest development version from GitHub:

.. code-block:: bash

   git clone https://github.com/yourusername/navercommerce.git
   cd navercommerce
   pip install -e .

For Development
---------------

If you want to contribute to the SDK or run tests, install with development dependencies:

.. code-block:: bash

   # Clone the repository
   git clone https://github.com/yourusername/navercommerce.git
   cd navercommerce

   # Install with dev dependencies using uv
   uv sync --extra dev

   # Or with pip
   pip install -e ".[dev]"

This will install additional tools for:

- Testing (pytest, pytest-cov, pytest-asyncio)
- Type checking (pyright, mypy)
- Linting (ruff)
- HTTP mocking (respx)

Verifying Installation
----------------------

After installation, verify that the SDK is correctly installed:

.. code-block:: python

   import navercommerce
   print(navercommerce.__version__)

You should see the version number printed (e.g., ``0.1.0``).

Dependencies
------------

The SDK has the following core dependencies:

- `httpx <https://www.python-httpx.org/>`_ - HTTP client with both sync and async support
- `pydantic <https://docs.pydantic.dev/>`_ - Data validation using Python type hints
- `anyio <https://anyio.readthedocs.io/>`_ - Compatibility layer for async operations
- `python-dotenv <https://github.com/theskumar/python-dotenv>`_ - Environment variable management

These will be automatically installed when you install the SDK.

Next Steps
----------

Once you have the SDK installed, proceed to :doc:`authentication` to set up your API credentials.
