Inquiries Resource
==================

The Inquiries resource manages customer Q&As and seller notices.

Sub-Resources
-------------

QnAs Sub-Resource (3 methods)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Access via ``client.inquiries.qnas``.

.. code-block:: python

   from navercommerce import NaverCommerce

   client = NaverCommerce()

   # List Q&As
   qnas = client.inquiries.qnas.list(page=0, size=20)
   for qna in qnas:
       print(f"Q: {qna.question}")
       print(f"Status: {qna.status}")

   # Answer a question
   client.inquiries.qnas.answer(
       question_id="question_id",
       answer_content="Thank you for your question. The answer is..."
   )

   # List answer templates
   templates = client.inquiries.qnas.list_templates()
   for template in templates:
       print(f"Template: {template.name}")

Notices Sub-Resource (5 methods)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Access via ``client.inquiries.notices``.

.. code-block:: python

   # Create notice
   notice = client.inquiries.notices.create(
       notice_type="EVENT",
       title="50% Off Sale!",
       content="Limited time offer..."
   )

   # List notices
   notices = client.inquiries.notices.list(page=0, size=20)

   # Retrieve specific notice
   notice = client.inquiries.notices.retrieve("notice_id")

   # Update notice
   notice = client.inquiries.notices.update(
       notice_id="notice_id",
       title="Updated Title",
       content="Updated content"
   )

   # Delete notice
   client.inquiries.notices.delete("notice_id")

Complete Example
----------------

.. code-block:: python

   from navercommerce import NaverCommerce

   client = NaverCommerce()

   # 1. Create a notice for sale
   sale_notice = client.inquiries.notices.create(
       notice_type="EVENT",
       title="Flash Sale - 50% Off!",
       content="All items 50% off for the next 24 hours!"
   )

   # 2. List pending Q&As
   qnas = client.inquiries.qnas.list(page=0, size=50)

   # 3. Answer each Q&A
   for qna in qnas:
       if qna.status == "PENDING":
           client.inquiries.qnas.answer(
               question_id=qna.id,
               answer_content="Thank you for your question..."
           )

   print(f"Created notice: {sale_notice.title}")
   print(f"Answered {len(qnas)} questions")

See Also
--------

- :doc:`../api-reference/resources` - Complete API reference
