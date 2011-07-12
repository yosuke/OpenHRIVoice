#!/bin/sh

echo "exiting existing components..."
rtexit /localhost/`hostname`.host_cxt/PulseAudioOutput0.rtc
rtexit /localhost/`hostname`.host_cxt/MARYRTC0.rtc
rtexit /localhost/`hostname`.host_cxt/ConsoleIn0.rtc
sleep 3

echo "launching components..."
gnome-terminal -x python ConsoleIn.py
gnome-terminal -x maryrtc
gnome-terminal -x pulseaudiooutput
sleep 3

echo "connecting components..."
rtcon /localhost/`hostname`.host_cxt/ConsoleIn0.rtc:out /localhost/`hostname`.host_cxt/MARYRTC0.rtc:text
rtcon /localhost/`hostname`.host_cxt/MARYRTC0.rtc:result /localhost/`hostname`.host_cxt/PulseAudioOutput0.rtc:AudioDataIn

echo "configureing components... 16000Hz male"
rtconf /localhost/`hostname`.host_cxt/PulseAudioOutput0.rtc set OutputSampleRate 16000
rtconf /localhost/`hostname`.host_cxt/MARYRTC0.rtc set rate 16000
rtconf /localhost/`hostname`.host_cxt/MARYRTC0.rtc set character male

sleep 1

echo "activating components..."
rtact /localhost/`hostname`.host_cxt/PulseAudioOutput0.rtc
rtact /localhost/`hostname`.host_cxt/MARYRTC0.rtc
rtact /localhost/`hostname`.host_cxt/ConsoleIn0.rtc

echo "synthesising for 15 seconds..."
sleep 15

echo "deactivating components..."
rtdeact /localhost/`hostname`.host_cxt/PulseAudioOutput0.rtc
rtdeact /localhost/`hostname`.host_cxt/MARYRTC0.rtc
rtdeact /localhost/`hostname`.host_cxt/ConsoleIn0.rtc

sleep 1

echo "configureing components... 16000Hz female"
rtconf /localhost/`hostname`.host_cxt/PulseAudioOutput0.rtc set OutputSampleRate 16000
rtconf /localhost/`hostname`.host_cxt/MARYRTC0.rtc set rate 16000
rtconf /localhost/`hostname`.host_cxt/MARYRTC0.rtc set character female

sleep 1

echo "activating components..."
rtact /localhost/`hostname`.host_cxt/PulseAudioOutput0.rtc
rtact /localhost/`hostname`.host_cxt/MARYRTC0.rtc
rtact /localhost/`hostname`.host_cxt/ConsoleIn0.rtc

echo "synthesising for 15 seconds..."
sleep 15

echo "existing components..."
rtexit /localhost/`hostname`.host_cxt/PulseAudioOutput0.rtc
rtexit /localhost/`hostname`.host_cxt/MARYRTC0.rtc
rtexit /localhost/`hostname`.host_cxt/ConsoleIn0.rtc
