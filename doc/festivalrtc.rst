FestivalRTC0.rtc
================
Festival speech synthesis component (python implementation)

:Vendor: AIST
:Version: 1.03
:Category: communication

Ports
-----
.. csv-table:: Ports
   :header: "Name", "Type", "DataType", "Description"
   :widths: 8, 8, 8, 26
   
   "text", "DataInPort", "TimedString", "Text to be synthesized."
   "result", "DataOutPort", "TimedOctetSeq", "Synthesized audio data."
   "status", "DataOutPort", "TimedString", "Status of audio output (one of 'started', 'finished')."
   "duration", "DataOutPort", "TimedString", "Time aliment information of each phonemes (to be used to lip-sync)."

Configuration parameters
------------------------
.. csv-table:: Configration parameters
   :header: "Name", "Description"
   :widths: 12, 38
   
   "rate", "Sampling frequency of output audio (fixed to 16kHz)."
   "character", "Character of voice (fixed to male)."
   "format", "Format of output audio (fixed to 16bit)."

