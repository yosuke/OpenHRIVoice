============
OpenHRIVoice
============

Voice components for OpenRTM (part of OpenHRI softwares)

Requirements
------------

OpenHRIVoice requires following libraries:

Julius and Julius-runkit
  http://julius.sourceforge.jp/

Julius-voxforge
  http://www.voxforge.org/

Festival
  http://www.cstr.ed.ac.uk/projects/festival/

OpenJTalk
  http://open-jtalk.sourceforge.net/

MARY
  http://mary.dfki.de/

lxml
  http://codespeak.net/lxml/

BeautifulSoup
  http://www.crummy.com/software/BeautifulSoup/

If you are using ubuntu, required libraries will be installed by entering
following commands:

 ::

 $ sudo apt-add-repository ppa:openhri/ppa
 $ sudo apt-get update
 $ sudo apt-get install julius julius-voxforge julius-runkit festival open-jtalk python-lxml python-beautifulsoup

Installation
------------

There are several methods of installation available:

1. Install ubuntu package (recommended):

 a. Register OpenHRI private package archive:

  ::
   
  $ sudo apt-add-repository ppa:openhri/ppa

 b. Install OpenHRIVoice package:

  ::
  
  $ sudo apt-get update
  $ sudo apt-get install openhrivoice

2. Clone the source from the repository and install:

 a. Clone from the repository:

  ::
  
  $ git clone git://github.com/yosuke/openhrivoice.git openhrivoice

 b. Run setup.py:

  ::
  
  $ cd openhrivoice
  $ sudo python setup.py install

Components
----------

JuliusRTC
  Julius (English and Japanese) speech recognition component.

FestivalRTC
  English speech synthesis component.

OpenJTalkRTC
  Japanese speech synthesis component.

MARYRTC
  English and German speech sysnthesis component.

XSLTRTC
  XML transformation component.

CombineResultsRTC
  Combine results from speech recognizers component.

see https://github.com/yosuke/OpenHRIVoice/tree/master/doc for description of each components.

Utility scripts
---------------

validatesrgs
  Validate format of SRGS grammar file.

srgstopls
  Generate pronounciation dictionary from SRGS grammar.

plstosinglewordgrammar
  Generate SRGS grammar from pronounciation dictionary.

bundlexinclude
  Bundle multiple XML file defined as xinclude.

srgstojulius
  Generate Julius grammar from SRGS grammar.

juliustographviz
  Draw graph from Julius grammar.

Examples:

- Validate format of the SRGS grammar.

  ::
  
  $ validatesrgs sample.grxml

- Generate PLS lexicon from the SRGS grammar.

  ::
  
  $ srgstopls sample.grxml > sample-lex.xml
 
- Generate single words SRGS grammar from the PLS lexicon.

  ::
  
  $ plstosinglewordgrammar sample-lex.xml > sample.grxml

- Draw graph of the SRGS grammar.

  ::
  
  $ srgstojulius sample.grxml | juliustographviz | dot -Txlib


Changelog
---------

openhrivoice-1.0

- First version.
