Advanced Topics
===============

Deep dives into SDK internals and advanced usage patterns.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   oauth-flow
   retry-logic
   architecture

Overview
--------

This section covers advanced topics for developers who want to understand how the SDK works internally or implement advanced patterns.

Topics Covered
--------------

:doc:`oauth-flow`
   OAuth 2.0 implementation details, token lifecycle, and thread safety

:doc:`retry-logic`
   Exponential backoff strategy, retry conditions, and configuration

:doc:`architecture`
   SDK design patterns, 3-tier architecture, and comparison to other SDKs

Who Should Read This
--------------------

These guides are for developers who:

- Want to understand SDK internals
- Need to extend or customize the SDK
- Are debugging authentication or retry issues
- Want to contribute to the SDK
- Are evaluating the SDK for production use

Prerequisites
-------------

Before reading these guides, you should:

- Be familiar with basic SDK usage (:doc:`../getting-started/index`)
- Understand HTTP and REST APIs
- Know Python async/await basics (for async topics)

Next Steps
----------

Start with :doc:`architecture` for an overview of the SDK design, then explore specific topics as needed.
