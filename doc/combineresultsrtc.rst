CombineResultsRTC
=================
Combine Results from Speech Recognizers

:Vendor: Yosuke Matsusaka, AIST
:Version: 1.05
:Category: Speech

Ports
-----
.. csv-table:: Ports
   :header: "Name", "Type", "DataType", "Description"
   :widths: 8, 8, 8, 26
   
   "status1", "DataInPort", "TimedString", "Status of recognizer 1."
   "result1", "DataInPort", "TimedString", "Recognition result of recognizer 1."
   "status2", "DataInPort", "TimedString", "Status of recognizer 2."
   "result2", "DataInPort", "TimedString", "Recognition result of recognizer 2."
   "statusout", "DataOutPort", "TimedString", "Status of both combined."
   "resultout", "DataOutPort", "TimedString", "Recognition result of both combined."

.. digraph:: comp

   rankdir=LR;
   CombineResultsRTC [shape=Mrecord, label="CombineResultsRTC"];
   status1 [shape=plaintext, label="status1"];
   status1 -> CombineResultsRTC;
   result1 [shape=plaintext, label="result1"];
   result1 -> CombineResultsRTC;
   status2 [shape=plaintext, label="status2"];
   status2 -> CombineResultsRTC;
   result2 [shape=plaintext, label="result2"];
   result2 -> CombineResultsRTC;
   statusout [shape=plaintext, label="statusout"];
   CombineResultsRTC -> statusout;
   resultout [shape=plaintext, label="resultout"];
   CombineResultsRTC -> resultout;

