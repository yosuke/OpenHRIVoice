#!/bin/sh

rtexit /localhost/`hostname`.host_cxt/JuliusRTC0.rtc
juliusrtc ../examples/juliusrtc/sample.grxml &
sleep 2
rtdoc --format=rst /localhost/`hostname`.host_cxt/JuliusRTC0.rtc > juliusrtc.rst
rtexit /localhost/`hostname`.host_cxt/JuliusRTC0.rtc

#rtexit /localhost/`hostname`.host_cxt/MARYRTC0.rtc
#maryrtc &
#sleep 2
#rtdoc --format=rst /localhost/`hostname`.host_cxt/MARYRTC0.rtc > maryrtc.rst
#rtexit /localhost/`hostname`.host_cxt/MARYRTC0.rtc

rtexit /localhost/`hostname`.host_cxt/FestivalRTC0.rtc
festivalrtc &
sleep 2
rtdoc --format=rst /localhost/`hostname`.host_cxt/FestivalRTC0.rtc > festivalrtc.rst
rtexit /localhost/`hostname`.host_cxt/FestivalRTC0.rtc

rtexit /localhost/`hostname`.host_cxt/OpenJTalkRTC0.rtc
openjtalkrtc &
sleep 2
rtdoc --format=rst /localhost/`hostname`.host_cxt/OpenJTalkRTC0.rtc > openjtalkrtc.rst
rtexit /localhost/`hostname`.host_cxt/OpenJTalkRTC0.rtc

rtexit /localhost/`hostname`.host_cxt/XSLTRTC0.rtc
xsltrtc ../examples/xsltrtc/sample.xsl &
sleep 2
rtdoc --format=rst /localhost/`hostname`.host_cxt/XSLTRTC0.rtc > xsltrtc.rst
rtexit /localhost/`hostname`.host_cxt/XSLTRTC0.rtc
