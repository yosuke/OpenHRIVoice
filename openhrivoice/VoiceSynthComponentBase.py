#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Base class for speech synthesis components

Copyright (C) 2010
    Yosuke Matsusaka
    Intelligent Systems Research Institute,
    National Institute of Advanced Industrial Science and Technology (AIST),
    Japan
    All rights reserved.
Licensed under the Eclipse Public License -v 1.0 (EPL)
http://www.opensource.org/licenses/eclipse-1.0.txt
'''

import os
import sys
import time
import subprocess
import signal
import tempfile
import traceback
import platform
import codecs
import locale
import wave
import optparse
import OpenRTM_aist
import RTC
try:
    import gettext
    _ = gettext.translation(domain='openhrivoice', localedir=os.path.dirname(__file__)+'/../share/locale').ugettext
except:
    _ = lambda s: s

class VoiceSynthBase:
    def __init__(self):
        self._durationdata = ""
        self._fp = None
        self._history = []
        self._cache = {}
        self._cachesize = 10
        self._copyrights = []
        
    def gettempname(self):
        # get temp file name
        fn = tempfile.mkstemp()
        os.close(fn[0])
        return fn[1]

    def synth(self, data, samplerate, character):
        if self._fp is not None:
            self._fp.close()
            self._fp = None
        try:
            (self._durationdata, wavfile) = self._cache[(data, samplerate, character)]
            self._fp = wave.open(wavfile, 'rb')
        except KeyError:
            (self._durationdata, wavfile) = self.synthreal(data, samplerate, character)
            self._history.append((data, samplerate, character))
            self._cache[(data, samplerate, character)] = (self._durationdata, wavfile)
            self._fp = wave.open(wavfile, 'rb')
            if len(self._history) > self._cachesize:
                d = self._history.pop(0)
                (logdata, wavfile) = self._cache[d]
                del self._cache[d]
                del logdata
                os.remove(wavfile)

    def synthreal(self, data, samplerate, character):
        pass
        
    def readdata(self, chunk):
        if self._fp is None:
            return None
        try:
            data = self._fp.readframes(chunk)
        except ValueError:
            self._fp.close()
            self._fp = None
            return None
        if data == '':
            self._fp.close()
            self._fp = None
            return None
        return data
    
    def terminate(self):
        pass

class DataListener(OpenRTM_aist.ConnectorDataListenerT):
    def __init__(self, name, obj):
        self._name = name
        self._obj = obj
    
    def __call__(self, info, cdrdata):
        data = OpenRTM_aist.ConnectorDataListenerT.__call__(self, info, cdrdata, RTC.TimedString(RTC.Time(0,0),""))
        self._obj.onData(self._name, data)

class VoiceSynthComponentBase(OpenRTM_aist.DataFlowComponentBase):
    def __init__(self, manager):
        OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)
        self._wrap = None

    def onInitialize(self):
        OpenRTM_aist.DataFlowComponentBase.onInitialize(self)
        self._logger = OpenRTM_aist.Manager.instance().getLogbuf(self._properties.getProperty("instance_name"))
        self._logger.RTC_INFO(self._properties.getProperty("type_name") + " version " + self._properties.getProperty("version"))
        self._logger.RTC_INFO("Copyright (C) 2010-2011 Yosuke Matsusaka")
        self._prevtime = time.clock()
        # configuration parameters
        self._samplerate = [16000,]
        self.bindParameter("rate", self._samplerate, 16000)
        self._character = ["male",]
        self.bindParameter("character", self._character, "male")
        # create inport
        self._indata = RTC.TimedString(RTC.Time(0,0), "")
        self._inport = OpenRTM_aist.InPort("text", self._indata)
        self._inport.appendProperty('description', _('Text to be synthesized.').encode('UTF-8'))
        self._inport.addConnectorDataListener(OpenRTM_aist.ConnectorDataListenerType.ON_BUFFER_WRITE,
                                              DataListener("ON_BUFFER_WRITE", self))
        self.registerInPort(self._inport._name, self._inport)
        # create outport for wave data
        self._outdata = RTC.TimedOctetSeq(RTC.Time(0,0), None)
        self._outport = OpenRTM_aist.OutPort("result", self._outdata)
        self._outport.appendProperty('description', _('Synthesized audio data.').encode('UTF-8'))
        self.registerOutPort(self._outport._name, self._outport)
        # create outport for status
        self._statusdata = RTC.TimedString(RTC.Time(0,0), "")
        self._statusport = OpenRTM_aist.OutPort("status", self._statusdata)
        self._statusport.appendProperty('description', _('Status of audio output (one of "started", "finished").').encode('UTF-8'))
        self.registerOutPort(self._statusport._name, self._statusport)
        # create outport for duration data
        self._durdata = RTC.TimedString(RTC.Time(0,0), "")
        self._durport = OpenRTM_aist.OutPort("duration", self._durdata)
        self._durport.appendProperty('description', _('Time aliment information of each phonemes (to be used to lip-sync).').encode('UTF-8'))
        self.registerOutPort(self._durport._name, self._durport)
        self._is_active = False
        return RTC.RTC_OK

    def onActivated(self, ec_id):
        OpenRTM_aist.DataFlowComponentBase.onActivated(self, ec_id)
        self._is_active = True
        return RTC.RTC_OK

    def onDeactivate(self, ec_id):
        OpenRTM_aist.DataFlowComponentBase.onDeactivate(self, ec_id)
        self._is_active = False
        return RTC.RTC_OK

    def onData(self, name, data):
        try:
            if self._is_active == True:
                udata = data.data.decode("utf-8")
                self._logger.RTC_INFO(udata + " " + str(self._samplerate[0]) + " " + self._character[0])
                if self._wrap is not None:
                    self._wrap.synth(udata, self._samplerate[0], self._character[0])
        except:
            self._logger.RTC_ERROR(traceback.format_exc())

    def onExecute(self, ec_id):
        OpenRTM_aist.DataFlowComponentBase.onExecute(self, ec_id)
        try:
            # send stream
            if platform.system() == 'Windows':
                now = time.clock()
            else:
                now = time.time()
            chunk = int(self._samplerate[0] * (now - self._prevtime))
            data = None
            if chunk > 0:
                self._prevtime = now
                data = self._wrap.readdata(chunk)
                if data is not None:
                    if self._statusdata.data != "started":
                        self._logger.RTC_INFO("stream started")
                        self._statusdata.data = "started"
                        self._statusport.write(self._statusdata)
                        self._durdata.data = self._wrap._durationdata
                        self._durport.write(self._durdata)
                        data2 = self._wrap.readdata(int(self._samplerate[0] * 1.0))
                        if data2 is not None:
                            data += data2
                    self._outdata.data = data
                    self._outport.write(self._outdata)
                else:
                    if self._statusdata.data != "finished":
                        self._logger.RTC_INFO("stream finished")
                        self._statusdata.data = "finished"
                        self._statusport.write(self._statusdata)
        except:
            self._logger.RTC_ERROR(traceback.format_exc())
        return RTC.RTC_OK

    def onFinalize(self):
        OpenRTM_aist.DataFlowComponentBase.onFinalize(self)
        self._wrap.terminate()
        return RTC.RTC_OK

