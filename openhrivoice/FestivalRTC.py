#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Festival speech synthesis component

Copyright (C) 2010
    Yosuke Matsusaka
    Intelligent Systems Research Institute,
    National Institute of Advanced Industrial Science and Technology (AIST),
    Japan
    All rights reserved.
Licensed under the Eclipse Public License -v 1.0 (EPL)
http://www.opensource.org/licenses/eclipse-1.0.txt
'''

import os, sys, time, subprocess, signal, tempfile, traceback, platform, codecs
import wave
import OpenRTM_aist
import RTC

class FestivalWrap:
    def __init__(self):
        self._wf = None
        self._samplerate = 16000
        self._durationdata = ""
        self._platform = platform.system()
        if hasattr(sys, "frozen"):
            self._basedir = os.path.dirname(unicode(sys.executable, sys.getfilesystemencoding()))
        else:
            self._basedir = os.path.dirname(__file__)
        if self._platform == "Windows":
            self._binfile = os.path.join(self._basedir, "3rdparty", "festival-1.96.03-win\\festival\\festival.exe")
            self._opt =  ["--libdir", os.path.join(self._basedir, "3rdparty", "festival-1.96.03-win\\festival\\lib")]
        else:
            self._binfile = "festival"
            self._opt = []
        self._cmdline =[self._binfile, '--pipe']
        self._cmdline.extend(self._opt)
        print ' '.join(self._cmdline)
        
    def gettempname(self):
        # get temp file name
        fn = tempfile.mkstemp()
        os.close(fn[0])
        return fn[1]

    def write(self, data):
        print data
        if self._wf is not None:
            self._wf.close()
            self._wf = None
            os.remove(self._wavfile)
        self._durfile = self.gettempname().replace("\\", "\\\\")
        self._wavfile = self.gettempname().replace("\\", "\\\\")
        # run Festival
        self._p = subprocess.Popen(self._cmdline, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        self._p.stdin.write('(set! u (Utterance Text "' + data + '"))')
        self._p.stdin.write('(utt.synth u)')
        self._p.stdin.write('(utt.save.segs u "' + self._durfile + '")')
        self._p.stdin.write('(utt.save.wave u "' + self._wavfile + '")')
        self._p.communicate()

        # read data
        self._wf = wave.open(self._wavfile, 'rb')
        #pobj._outdata.channels = wf.getnchannels()
        #pobj._outdata.samplebytes = wf.getsampwidth()
        self._samplerate = self._wf.getframerate()
        df = open(self._durfile, 'r')
        self._durationdata = df.read().encode("utf-8")
        print self._durationdata.decode("utf-8")
        df.close()
        os.remove(self._durfile)
        
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
    
    def terminate(self):
        print 'FestivalWrap: terminate'
        #self._p.terminate()
        return 0

FestivalRTC_spec = ["implementation_id", "FestivalRTC",
                    "type_name",         "FestivalRTC",
                    "description",       "Festival speech synthesis component (python implementation)",
                    "version",           "1.0.0",
                    "vendor",            "AIST",
                    "category",          "communication",
                    "activity_type",     "DataFlowComponent",
                    "max_instance",      "1",
                    "language",          "Python",
                    "lang_type",         "script",
                    "conf.__widget__.format", "radio",
                    "conf.__constraints__.format", "int16",
                    "conf.__widget__.rate", "spin",
                    "conf.__constraints__.rate", "16000",
                    "conf.__widget__.character", "radio",
                    "conf.__constraints__.character", "male",
                    ""]

class DataListener(OpenRTM_aist.ConnectorDataListenerT):
    def __init__(self, name, obj):
        self._name = name
        self._obj = obj
    
    def __call__(self, info, cdrdata):
        data = OpenRTM_aist.ConnectorDataListenerT.__call__(self, info, cdrdata, RTC.TimedString(RTC.Time(0,0),""))
        self._obj.onData(self._name, data)

class FestivalRTC(OpenRTM_aist.DataFlowComponentBase):
    def __init__(self, manager):
        try:
            OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)
            #self._rate = 16000
        except:
            print traceback.format_exc()

    def onInitialize(self):
        try:
            self._j = FestivalWrap()
            self._prevtime = time.time()
            # create inport
            self._indata = RTC.TimedString(RTC.Time(0,0), "")
            self._inport = OpenRTM_aist.InPort("text", self._indata)
            self._inport.addConnectorDataListener(OpenRTM_aist.ConnectorDataListenerType.ON_BUFFER_WRITE,
                                                  DataListener("ON_BUFFER_WRITE", self))
            self.registerInPort("text", self._inport)
            # create outport for wave data
            self._outdata = RTC.TimedOctetSeq(RTC.Time(0,0), None)
            self._outport = OpenRTM_aist.OutPort("result", self._outdata)
            self.registerOutPort("result", self._outport)
            # create outport for status
            self._statusdata = RTC.TimedString(RTC.Time(0,0), "")
            self._statusport = OpenRTM_aist.OutPort("status", self._statusdata)
            self.registerOutPort("status", self._statusport)
            # create outport for duration data
            self._durdata = RTC.TimedString(RTC.Time(0,0), "")
            self._durport = OpenRTM_aist.OutPort("duration", self._durdata)
            self.registerOutPort("duration", self._durport)
        except:
            print traceback.format_exc()
        return RTC.RTC_OK

    def onData(self, name, data):
        try:
            udata = data.data.decode("utf-8")
            self._j.write(udata)
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
                    self._outdata.data = data
                    self._outport.write(self._outdata)
                    if self._statusdata.data != "started":
                        print "start"
                        self._statusdata.data = "started"
                        self._statusport.write(self._statusdata)
                        self._durdata.data = self._j._durationdata
                        self._durport.write(self._durdata)
                else:
                    if self._statusdata.data != "finished":
                        print "finished"
                        self._statusdata.data = "finished"
                        self._statusport.write(self._statusdata)
        except:
            print traceback.format_exc()
        return RTC.RTC_OK

    def onFinalize(self):
        self._j.terminate()
        return RTC.RTC_OK

class FestivalRTCManager:
    def __init__(self):
        self._comp = None
        self._manager = OpenRTM_aist.Manager.init(sys.argv)
        self._manager.setModuleInitProc(self.moduleInit)
        self._manager.activateManager()

    def start(self):
        self._manager.runManager(False)

    def moduleInit(self, manager):
        profile=OpenRTM_aist.Properties(defaults_str=FestivalRTC_spec)
        manager.registerFactory(profile, pyFestival, OpenRTM_aist.Delete)
        self._comp = manager.createComponent("FestivalRTC")

def main():
    manager = FestivalRTCManager()
    manager.start()

if __name__=='__main__':
    main()
