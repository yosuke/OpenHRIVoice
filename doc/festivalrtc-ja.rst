FestivalRTC
===========
英語音声合成コンポーネント

:Vendor: AIST
:Version: 1.05
:Category: communication

Ports
-----
.. csv-table:: Ports
   :header: "Name", "Type", "DataType", "Description"
   :widths: 8, 8, 8, 26
   
   "text", "DataInPort", "TimedString", "合成されるテキストデータ"
   "result", "DataOutPort", "TimedOctetSeq", "合成された音声データ"
   "status", "DataOutPort", "TimedString", "音声合成の状態 ('started'か'finished')"
   "duration", "DataOutPort", "TimedString", "各音韻の時間情報（リップシンクに使用）"

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
   
   "rate", "出力される音声の周波数（16kHzに固定）"
   "character", "音声のキャラクタ（男性に固定）"
   "format", "出力される音声のフォーマット（16bitに固定）"

