XSLTRTC
=======
XSLTを用いたXML変換コンポーネント

:Vendor: AIST
:Version: 1.05
:Category: communication

Ports
-----
.. csv-table:: Ports
   :header: "Name", "Type", "DataType", "Description"
   :widths: 8, 8, 8, 26
   
   "text", "DataInPort", "TimedString", "XML形式のテキストデータ"
   "result", "DataOutPort", "TimedString", "XML形式のテキストデータ（変換後）"

.. digraph:: comp

   rankdir=LR;
   XSLTRTC [shape=Mrecord, label="XSLTRTC"];
   text [shape=plaintext, label="text"];
   text -> XSLTRTC;
   result [shape=plaintext, label="result"];
   XSLTRTC -> result;

