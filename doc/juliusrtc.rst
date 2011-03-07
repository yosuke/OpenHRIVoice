JuliusRTC
=========
Julius (English and Japanese) speech recognition component.

:Vendor: AIST
:Version: 1.05
:Category: communication

Ports
-----
.. csv-table:: Ports
   :header: "Name", "Type", "DataType", "Description"
   :widths: 8, 8, 8, 26
   
   "data", "DataInPort", "TimedOctetSeq", "Audio data (in packets) to be recognized."
   "activegrammar", "DataInPort", "TimedString", "Grammar ID to be activated."
   "status", "DataOutPort", "TimedString", "Status of the recognizer (one of 'LISTEN [accepting speech]', 'STARTREC [start recognition process]', 'ENDREC [end recognition process]', 'REJECTED [rejected speech input]')"
   "result", "DataOutPort", "TimedString", "Recognition result in XML format."
   "log", "DataOutPort", "TimedOctetSeq", "Log of audio data."

.. digraph:: comp

   rankdir=LR;
   JuliusRTC [shape=Mrecord, label="JuliusRTC"];
   data [shape=plaintext, label="data"];
   data -> JuliusRTC;
   activegrammar [shape=plaintext, label="activegrammar"];
   activegrammar -> JuliusRTC;
   status [shape=plaintext, label="status"];
   JuliusRTC -> status;
   result [shape=plaintext, label="result"];
   JuliusRTC -> result;
   log [shape=plaintext, label="log"];
   JuliusRTC -> log;

Configuration parameters
------------------------
.. csv-table:: Configuration parameters
   :header: "Name", "Description"
   :widths: 12, 38
   
   "phonemodel", ""
   "voiceactivitydetection", ""
   "language", ""

