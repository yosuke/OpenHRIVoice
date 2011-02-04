JuliusRTC0.rtc
==============
Julius speech recognition component (python implementation)

:Vendor: AIST
:Version: 1.03
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

Configuration parameters
------------------------
.. csv-table:: Configration parameters
   :header: "Name", "Description"
   :widths: 12, 38
   
   "phonemodel", ""
   "voiceactivitydetection", ""
   "language", ""

