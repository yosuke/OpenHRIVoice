#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''MARY speech synthesis component

Copyright (C) 2010
    Yosuke Matsusaka
    Intelligent Systems Research Institute,
    National Institute of Advanced Industrial Science and Technology (AIST),
    Japan
    All rights reserved.
Licensed under the Eclipse Public License -v 1.0 (EPL)
http://www.opensource.org/licenses/eclipse-1.0.txt
'''

import os, sys, time, urllib, tempfile, traceback, codecs, locale
import wave
import OpenRTM_aist
import RTC

class MARYTalkWrap:
    def __init__(self):
        self._durations = ""
        self._samplerate = 16000
        self._baseurl = "http://localhost:59125/"
        self._input_type = "TEXT"
        self._output_type = "AUDIO"
        self._audio = "WAVE"
        self._characters = {}
        self._defaultcharacter = None
        self._voice = None
        self._locale = None
        self._gender = None
        self._voice_type = None
        voiceinfo = urllib.urlopen(self._baseurl + 'voices').readlines()
        for v in voiceinfo:
            (id, lang, gender, type) = v.strip().split()
            idstr = "%s-%s-%s" % (gender, lang, id)
            if not self._defaultcharacter:
                self._defaultcharacter = idstr
            self._characters[idstr] = (id, lang, gender, type)
            
    def setcharacter(self, idstr):
        (self._voice, self._locale, self._gender, self._voice_type) = self._characters[idstr]

    def gettempname(self):
        # get temp file name
        fn = tempfile.mkstemp()
        os.close(fn[0])
        return fn[1]

    def getaudio(self, data):
        if not self._voice:
            return None
        query = [
                 ('INPUT_TYPE', self._input_type),
                 ('OUTPUT_TYPE', 'AUDIO'),
                 ('AUDIO', self._audio),
                 ('LOCALE', self._locale),
                 ('VOICE', self._voice),
                 ('INPUT_TEXT', data),
                 ]
        maryurl = self._baseurl + 'process?' + urllib.urlencode(query)
        wavfile = self.gettempname()
        urllib.urlretrieve(maryurl, wavfile)
        return wavfile

    def getdurations(self, data):
        if not self._voice:
            return None
        query = [
                 ('INPUT_TYPE', self._input_type),
                 ('OUTPUT_TYPE', 'REALISED_DURATIONS'),
                 ('AUDIO', self._audio),
                 ('LOCALE', self._locale),
                 ('VOICE', self._voice),
                 ('INPUT_TEXT', data),
                 ]
        maryurl = self._baseurl + 'process?' + urllib.urlencode(query)
        f = urllib.urlopen(maryurl)
        d = f.read()
        f.close()
        #lasttime = float(d.split('\n')[-2].split(' ')[0])
        #d = '#\n0.001 125 sil\n' + '\n'.join(d.split('\n')[1:]) + ('%f 125 sil\n' % (lasttime + 0.001,))
        return d

    def write(self, data, pobj, chunk):
        print data
        print data
        if self._wf is not None:
            self._wf.close()
            self._wf = None
            os.remove(self._wavfile)
        self._wavfile = self.getaudio(data)
        self._durations = self.getdurations(data)
        print self._durations
        # read audio data
        self._wf = wave.open(self._wavfile, 'rb')
        #pobj._outdata.channels = wf.getnchannels()
        #pobj._outdata.samplebytes = wf.getsampwidth()
        self._samplerate = self._wf.getframerate()

    def readdata(self, chunk):
        if self._wf is None:
            return None
        data = self._wf.readframes(chunk)
        if data != '':
            return data
        self._wf.close()
        self._wf = None
        os.remove(self._wavfile)
        return None
    
MARYRTC_spec = ["implementation_id", "MARYRTC",
                "type_name",         "MARYRTC",
                "description",       "MARY speech synthesis component (python implementation)",
                "version",           "1.0.0",
                "vendor",            "AIST",
                "category",          "communication",
                "activity_type",     "DataFlowComponent",
                "max_instance",      "10",
                "language",          "Python",
                "lang_type",         "script",
                "conf.default.format", "int16"
                "conf.default.rate", "16000"
                "conf.default.character", ""
                "conf.__widget__.format", "radio",
                "conf.__constraints__.format", "int16",
                "conf.__widget__.rate", "spin",
                "conf.__constraints__.rate", "16000",
                "conf.__widget__.character", "radio",
                "conf.__constraints__.character", "",
                ""]

class DataListener(OpenRTM_aist.ConnectorDataListenerT):
    def __init__(self, name, obj):
        self._name = name
        self._obj = obj
    
    def __call__(self, info, cdrdata):
        data = OpenRTM_aist.ConnectorDataListenerT.__call__(self, info, cdrdata, RTC.TimedString(RTC.Time(0,0),""))
        self._obj.onData(self._name, data)

class MARYRTC(OpenRTM_aist.DataFlowComponentBase):
    def __init__(self, manager):
        OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

    def onInitialize(self):
        try:
            self._j = MARYTalkWrap()
            # bind configuration parameters
            self.bindParameter("character", self._character, self._j._defaultcharacter)
            # create inport
            self._indata = RTC.TimedString(RTC.Time(0,0), u"")
            self._inport = OpenRTM_aist.InPort("text", self._indata)
            self.registerInPort("text", self._inport)
            # create outport
            self._outdata = RTC.TimedOctetSeq(RTC.Time(0,0), None)
            self._outport = OpenRTM_aist.OutPort("result", self._outdata)
            self.registerOutPort("result", self._outport)
            # create outport for duration
            self._durationdata = RTC.TimedString(RTC.Time(0,0), "")
            self._durationport = OpenRTM_aist.OutPort("duration", self._durationdata)
            self.registerOutPort("duration", self._durationport)
        except:
            print traceback.format_exc()
        return RTC.RTC_OK

    def onData(self, name, data):
        try:
            self._j.setcharacter(self._character)
            udata = data.data.decode("utf-8")
            self._j.write(udata, self, 160)
        except:
            print traceback.format_exc()

    def onExecute(self, ec_id):
        try:
            # send stream
            now = time.time()
            chunk = int(self._j._samplerate * (now - self._prevtime))
            self._prevtime = now
            if chunk > 0:
                data = self._j.readdata(chunk)
                if data is not None:
                    self._outdata.tm = self._durationdata.tm
                    self._outdata.data = data
                    self._outport.write(self._outdata)
                    if self._statusdata.data != "started":
                        print "start"
                        self._statusdata.data = "started"
                        self._statusport.write(self._statusdata)
                        self._durationdata.data = self._j._durations
                        OpenRTM_aist.setTimestamp(self._durationdata)
                        self._durationport.write(self._durationdata)
                else:
                    if self._statusdata.data != "finished":
                        print "finished"
                        self._statusdata.data = "finished"
                        self._statusport.write(self._statusdata)
        except:
            print traceback.format_exc()
        return RTC.RTC_OK

class MARYRTCManager:
    def __init__(self):
        self._comp = None
        self._manager = OpenRTM_aist.Manager.init(sys.argv)
        self._manager.setModuleInitProc(self.moduleInit)
        self._manager.activateManager()

    def start(self):
        self._manager.runManager(False)

    def moduleInit(self, manager):
        profile=OpenRTM_aist.Properties(defaults_str=MARYRTC_spec)
        manager.registerFactory(profile, MARYRTC, OpenRTM_aist.Delete)
        self._comp = manager.createComponent("MARYRTC")

def main():
    locale.setlocale(locale.LC_CTYPE, "")
    encoding = locale.getlocale()[1]
    if not encoding:
        encoding = "us-ascii"
    sys.stdout = codecs.getwriter(encoding)(sys.stdout, errors = "replace")
    sys.stderr = codecs.getwriter(encoding)(sys.stderr, errors = "replace")
    manager = pyMARYRTCManager()
    manager.start()

if __name__=='__main__':
    main()
