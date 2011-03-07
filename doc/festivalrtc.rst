FestivalRTC
===========
English speech synthesis component.

:Vendor: AIST
:Version: 1.05
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

.. digraph:: comp

   rankdir=LR;
   FestivalRTC [shape=Mrecord, label="FestivalRTC"];
   text [shape=plaintext, label="text"];
   text -> FestivalRTC;
   result [shape=plaintext, label="result"];
   FestivalRTC -> result;
   status [shape=plaintext, label="status"];
   FestivalRTC -> status;
   duration [shape=plaintext, label="duration"];
   FestivalRTC -> duration;

Configuration parameters
------------------------
.. csv-table:: Configuration parameters
   :header: "Name", "Description"
   :widths: 12, 38
   
   "rate", "Sampling frequency of output audio (fixed to 16kHz)."
   "character", "Character of the voice (fixed to male)."
   "format", "Format of output audio (fixed to 16bit)."

