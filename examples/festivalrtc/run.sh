#!/bin/sh

echo "exiting existing components..."
rtexit /localhost/`hostname`.host_cxt/PulseAudioOutput0.rtc
rtexit /localhost/`hostname`.host_cxt/FestivalRTC0.rtc
rtexit /localhost/`hostname`.host_cxt/ConsoleIn0.rtc
sleep 3

echo "launching components..."
gnome-terminal -x python ConsoleIn.py
gnome-terminal -x festivalrtc
gnome-terminal -x pulseaudiooutput
sleep 3

echo "connecting components..."
rtcon /localhost/`hostname`.host_cxt/ConsoleIn0.rtc:out /localhost/`hostname`.host_cxt/FestivalRTC0.rtc:text
rtcon /localhost/`hostname`.host_cxt/FestivalRTC0.rtc:result /localhost/`hostname`.host_cxt/PulseAudioOutput0.rtc:AudioDataIn

echo "activating components..."
rtact /localhost/`hostname`.host_cxt/PulseAudioOutput0.rtc
rtact /localhost/`hostname`.host_cxt/FestivalRTC0.rtc
rtact /localhost/`hostname`.host_cxt/ConsoleIn0.rtc

echo "synthesising for 30 seconds..."
sleep 30

echo "existing components..."
rtexit /localhost/`hostname`.host_cxt/PulseAudioOutput0.rtc
rtexit /localhost/`hostname`.host_cxt/FestivalRTC0.rtc
rtexit /localhost/`hostname`.host_cxt/ConsoleIn0.rtc
