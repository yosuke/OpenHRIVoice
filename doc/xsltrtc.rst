XSLTRTC
=======
XML transformation component.

:Vendor: AIST
:Version: 1.05
:Category: communication

Ports
-----
.. csv-table:: Ports
   :header: "Name", "Type", "DataType", "Description"
   :widths: 8, 8, 8, 26
   
   "text", "DataInPort", "TimedString", "Text data in XML format."
   "result", "DataOutPort", "TimedString", "Text data in XML format (transformed)."

.. digraph:: comp

   rankdir=LR;
   XSLTRTC [shape=Mrecord, label="XSLTRTC"];
   text [shape=plaintext, label="text"];
   text -> XSLTRTC;
   result [shape=plaintext, label="result"];
   XSLTRTC -> result;

