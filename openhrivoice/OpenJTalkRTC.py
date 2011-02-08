#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''OpenJTalk speech synthesis component

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
import optparse
import wave
import socket
import OpenRTM_aist
import RTC
from __init__ import __version__
import utils
from parseopenjtalk import parseopenjtalk

__doc__ = 'Japanese speech synthesis component.'

class mysocket(socket.socket):
    def getline(self):
        s = ""
        buf = self.recv(1)
        while buf and buf[0] != "\n":
            s += buf[0]
            buf = self.recv(1)
            if not buf:
                break
        return s

class OpenJTalkWrap:
    def __init__(self):
        self._args = (("td", "tree-dur.inf"),
                      ("tf", "tree-lf0.inf"),
                      ("tm", "tree-mgc.inf"),
                      ("md", "dur.pdf"),
                      ("mf", "lf0.pdf"),
                      ("mm", "mgc.pdf"),
                      ("df", "lf0.win1"),
                      ("df", "lf0.win2"),
                      ("df", "lf0.win3"),
                      ("dm", "mgc.win1"),
                      ("dm", "mgc.win2"),
                      ("dm", "mgc.win3"),
                      ("ef", "tree-gv-lf0.inf"),
                      ("em", "tree-gv-mgc.inf"),
                      ("cf", "gv-lf0.pdf"),
                      ("cm", "gv-mgc.pdf"),
                      ("k", "gv-switch.inf"))
        self._wf = None
        self._samplerate = 16000
        self._durationdata = ""
        self._platform = platform.system()
        if hasattr(sys, "frozen"):
            self._basedir = os.path.dirname(unicode(sys.executable, sys.getfilesystemencoding()))
        else:
            self._basedir = os.path.dirname(__file__)
        if self._platform == "Windows":
            self._binfile = os.path.join(self._basedir, "open_jtalk.exe")
            self._phonemodel =  os.path.join(self._basedir, "3rdparty", "hts_voice_nitech_jp_atr503_m001-1.01")
            self._dicfile = os.path.join(self._basedir, "3rdparty", "open_jtalk_dic_utf_8-1.00")
        else:
            self._binfile = "open_jtalk"
            self._phonemodel = "/usr/lib/hts-voice/nitech-jp-atr503-m001"
            self._dicfile = "/usr/lib/open_jtalk/dic/utf-8"

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
        self._textfile = self.gettempname()
        self._wavfile = self.gettempname()
        self._logfile = self.gettempname()
        # text file which specifies synthesized string
        fp = codecs.open(self._textfile, 'w', 'utf-8')
        fp.write(u"%s\n" % (data,))
        fp.close()
        # command line for OpenJTalk
        self._cmdarg = []
        self._cmdarg.append(self._binfile)
        for o, v in self._args:
            self._cmdarg.append("-"+o)
            self._cmdarg.append(os.path.join(self._phonemodel, v))
        self._cmdarg.append("-x")
        self._cmdarg.append(self._dicfile)
        self._cmdarg.append("-ow")
        self._cmdarg.append(self._wavfile)
        self._cmdarg.append("-ot")
        self._cmdarg.append(self._logfile)
        self._cmdarg.append(self._textfile)
        # run OpenJTalk
        #print " ".join(self._cmdarg)
        self._p = subprocess.Popen(self._cmdarg)
        self._p.wait()
        # read duration data
        d = parseopenjtalk()
        d.parse(self._logfile)
        self._durationdata = d.toseg().encode("utf-8")
        print self._durationdata.decode("utf-8")
        # read data
        self._wf = wave.open(self._wavfile, 'rb')
        #pobj._outdata.channels = wf.getnchannels()
        #pobj._outdata.samplebytes = wf.getsampwidth()
        self._samplerate = self._wf.getframerate()
        os.remove(self._textfile)
        os.remove(self._logfile)
    
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
        pass

class OpenJTalkWrap2:
    def __init__(self):
        self._args = (("td", "tree-dur.inf"),
                      ("tf", "tree-lf0.inf"),
                      ("tm", "tree-mgc.inf"),
                      ("md", "dur.pdf"),
                      ("mf", "lf0.pdf"),
                      ("mm", "mgc.pdf"),
                      ("df", "lf0.win1"),
                      ("df", "lf0.win2"),
                      ("df", "lf0.win3"),
                      ("dm", "mgc.win1"),
                      ("dm", "mgc.win2"),
                      ("dm", "mgc.win3"),
                      ("ef", "tree-gv-lf0.inf"),
                      ("em", "tree-gv-mgc.inf"),
                      ("cf", "gv-lf0.pdf"),
                      ("cm", "gv-mgc.pdf"),
                      ("k", "gv-switch.inf"))
        self._samplerate = 16000
        self._platform = platform.system()
        if hasattr(sys, "frozen"):
            self._basedir = os.path.dirname(unicode(sys.executable, sys.getfilesystemencoding()))
        else:
            self._basedir = os.path.dirname(__file__)
        if self._platform == "Windows":
            self._binfile = os.path.join(self._basedir, "open_jtalk.exe")
            self._phonemodel =  os.path.join(self._basedir, "3rdparty", "hts_voice_nitech_jp_atr503_m001-1.01")
            self._dicfile = os.path.join(self._basedir, "3rdparty", "open_jtalk_dic_utf_8-1.00")
        else:
            self._binfile = "open_jtalk"
            self._phonemodel = "/usr/lib/hts-voice/nitech-jp-atr503-m001"
            self._dicfile = "/usr/lib/open_jtalk/dic/utf-8"
        # command line for OpenJTalk
        self._moduleport = self.getunusedport()
        self._cmdarg = []
        self._cmdarg.append(self._binfile)
        for o, v in self._args:
            self._cmdarg.append("-"+o)
            self._cmdarg.append(os.path.join(self._phonemodel, v))
        self._cmdarg.append("-x")
        self._cmdarg.append(self._dicfile)
        self._cmdarg.append("-w")
        self._cmdarg.append(str(self._moduleport))
        # run OpenJTalk
        #print " ".join(self._cmdarg)
        self._p = subprocess.Popen(self._cmdarg)
        self._modulesocket = mysocket(socket.AF_INET, socket.SOCK_STREAM)
        self._modulesocket.settimeout(5)
        print "connecting to ports"
        for retry in range(0, 10):
            try:
                self._modulesocket.connect(("localhost", self._moduleport))
            except socket.error:
                time.sleep(1)
                continue
            break

    def getunusedport(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('localhost', 0))
        addr, port = s.getsockname()
        s.close()
        return port

    def write(self, data):
        print data
        self._modulesocket.sendall(data.encode("utf-8")+"\n")
        # read duration data
        d = ""
        l = self._modulesocket.getline()
        while l != "" and l != "LABELEND":
            d += l + "\n"
            l = self._modulesocket.getline()
        dd = parseopenjtalk(d)
        self._durationdata = dd.toseg().encode("utf-8")
        print self._durationdata
        # read data
        self._dlen = int(self._modulesocket.getline())
        self._rlen = 0
            
    def readdata(self, chunk):
        if self._rlen < self._dlen:
            rdata = self._modulesocket.recv(chunk)
            self._rlen += len(rdata)
            return rdata
        return None
    
    def terminate(self):
        self._modulesocket.close()
        self._p.terminate()

OpenJTalkRTC_spec = ["implementation_id", "OpenJTalkRTC",
                     "type_name",         "OpenJTalkRTC",
                     "description",       __doc__,
                     "version",           __version__,
                     "vendor",            "AIST",
                     "category",          "communication",
                     "activity_type",     "DataFlowComponent",
                     "max_instance",      "1",
                     "language",          "Python",
                     "lang_type",         "script",
                     "conf.default.format", "int16",
                     "conf.__widget__.format", "radio",
                     "conf.__constraints__.format", "int16",
                     "conf.__description__.format", "Format of output audio (fixed to 16bit).",
                     "conf.default.rate", "16000",
                     "conf.__widget__.rate", "spin",
                     "conf.__constraints__.rate", "16000",
                     "conf.__description__.rate", "Sampling frequency of output audio (fixed to 16kHz).",
                     "conf.default.character", "male",
                     "conf.__widget__.character", "radio",
                     "conf.__constraints__.character", "male",
                     "conf.__description__.character", "Character of voice (fixed to male).",
                     ""]

class DataListener(OpenRTM_aist.ConnectorDataListenerT):
    def __init__(self, name, obj):
        self._name = name
        self._obj = obj
    
    def __call__(self, info, cdrdata):
        data = OpenRTM_aist.ConnectorDataListenerT.__call__(self, info, cdrdata, RTC.TimedString(RTC.Time(0,0),""))
        self._obj.onData(self._name, data)

class OpenJTalkRTC(OpenRTM_aist.DataFlowComponentBase):
    def __init__(self, manager):
        OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)
        self._logger = OpenRTM_aist.Manager.instance().getLogbuf("OpenJTalkRTC")
        self._logger.RTC_INFO("OpenJTalkRTC version " + __version__)
        self._logger.RTC_INFO("Copyright (C) 2010-2011 Yosuke Matsusaka")

    def onInitialize(self):
        OpenRTM_aist.DataFlowComponentBase.onInitialize(self)
        self._j = OpenJTalkWrap()
        self._prevtime = time.time()
        # bind configuration parameters
        #self.bindParameter("rate", self._rate, self._rate)
        # create inport
        self._indata = RTC.TimedString(RTC.Time(0,0), "")
        self._inport = OpenRTM_aist.InPort("text", self._indata)
        self._inport.appendProperty('description', 'Text to be synthesized.')
        self._inport.addConnectorDataListener(OpenRTM_aist.ConnectorDataListenerType.ON_BUFFER_WRITE,
                                              DataListener("ON_BUFFER_WRITE", self))
        self.registerInPort(self._inport._name, self._inport)
        # create outport for audio stream
        self._outdata = RTC.TimedOctetSeq(RTC.Time(0,0), None)
        self._outport = OpenRTM_aist.OutPort("result", self._outdata)
        self._outport.appendProperty('description', 'Synthesized audio data.')
        self.registerOutPort(self._outport._name, self._outport)
        # create outport for status
        self._statusdata = RTC.TimedString(RTC.Time(0,0), "")
        self._statusport = OpenRTM_aist.OutPort("status", self._statusdata)
        self._statusport.appendProperty('description', 'Status of audio output (one of "started", "finished").')
        self.registerOutPort(self._statusport._name, self._statusport)
        # create outport for duration
        self._durationdata = RTC.TimedString(RTC.Time(0,0), "")
        self._durationport = OpenRTM_aist.OutPort("duration", self._durationdata)
        self._durationport.appendProperty('description', 'Time aliment information of each phonemes (to be used to lip-sync).')
        self.registerOutPort(self._durationport._name, self._durationport)
        return RTC.RTC_OK
    
    def onData(self, name, data):
        udata = data.data.decode("utf-8")
        self._j.write(udata)

    def onExecute(self, ec_id):
        OpenRTM_aist.DataFlowComponentBase.onExecute(self, ec_id)
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
                    self._logger.RTC_INFO("streaming start")
                    self._statusdata.data = "started"
                    self._statusport.write(self._statusdata)
                    self._durationdata.data = self._j._durationdata
                    self._durationport.write(self._durationdata)
            else:
                if self._statusdata.data != "finished":
                    self._logger.RTC_INFO("streaming finished")
                    self._statusdata.data = "finished"
                    self._statusport.write(self._statusdata)
        return RTC.RTC_OK

    def onFinalize(self):
        self._j.terminate()
        return RTC.RTC_OK

class OpenJTalkRTCManager:
    def __init__(self):
        parser = optparse.OptionParser(version=__version__, description=__doc__)
        utils.addmanageropts(parser)
        try:
            opts, args = parser.parse_args()
        except optparse.OptionError, e:
            print >>sys.stderr, 'OptionError:', e
            sys.exit(1)
        self._comp = None
        self._manager = OpenRTM_aist.Manager.init(utils.genmanagerargs(opts))
        self._manager.setModuleInitProc(self.moduleInit)
        self._manager.activateManager()

    def start(self):
        self._manager.runManager(False)

    def moduleInit(self, manager):
        profile=OpenRTM_aist.Properties(defaults_str=OpenJTalkRTC_spec)
        manager.registerFactory(profile, OpenJTalkRTC, OpenRTM_aist.Delete)
        self._comp = manager.createComponent("OpenJTalkRTC")

def main():
    locale.setlocale(locale.LC_CTYPE, "")
    encoding = locale.getlocale()[1]
    if not encoding:
        encoding = "us-ascii"
    sys.stdout = codecs.getwriter(encoding)(sys.stdout, errors = "replace")
    sys.stderr = codecs.getwriter(encoding)(sys.stderr, errors = "replace")
    manager = OpenJTalkRTCManager()
    manager.start()

if __name__=='__main__':
    main()
