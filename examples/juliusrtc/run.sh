#!/bin/sh

echo "exiting existing components..."
rtexit /localhost/`hostname`.host_cxt/JuliusRTC0.rtc
rtexit /localhost/`hostname`.host_cxt/OpenJTalkRTC0.rtc
rtexit /localhost/`hostname`.host_cxt/ConsoleIn0.rtc
rtexit /localhost/`hostname`.host_cxt/PulseAudioOutput0.rtc
sleep 3

echo "launching components..."
gnome-terminal -x python ConsoleIn.py
gnome-terminal -x openjtalkrtc
gnome-terminal -x juliusrtc sample.grxml
gnome-terminal -x pulseaudiooutput
sleep 3

echo "connecting components..."
rtcon /localhost/`hostname`.host_cxt/ConsoleIn0.rtc:out /localhost/`hostname`.host_cxt/OpenJTalkRTC0.rtc:text
rtcon /localhost/`hostname`.host_cxt/OpenJTalkRTC0.rtc:result /localhost/`hostname`.host_cxt/PulseAudioOutput0.rtc:AudioDataIn
rtcon /localhost/`hostname`.host_cxt/PulseAudioOutput0.rtc:AudioDataOut /localhost/`hostname`.host_cxt/JuliusRTC0.rtc:data

sleep 1

echo "activating components..."
rtact /localhost/`hostname`.host_cxt/JuliusRTC0.rtc
rtact /localhost/`hostname`.host_cxt/OpenJTalkRTC0.rtc
rtact /localhost/`hostname`.host_cxt/ConsoleIn0.rtc
rtact /localhost/`hostname`.host_cxt/PulseAudioOutput0.rtc

echo "inloop simulation for 30 seconds..."
sleep 30

echo "existing components..."
rtexit /localhost/`hostname`.host_cxt/JuliusRTC0.rtc
rtexit /localhost/`hostname`.host_cxt/OpenJTalkRTC0.rtc
rtexit /localhost/`hostname`.host_cxt/ConsoleIn0.rtc
rtexit /localhost/`hostname`.host_cxt/PulseAudioOutput0.rtc
