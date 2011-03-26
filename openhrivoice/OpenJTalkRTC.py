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
from openhrivoice.__init__ import __version__
from openhrivoice import utils
from openhrivoice.config import config
from openhrivoice.parseopenjtalk import parseopenjtalk
from openhrivoice.VoiceSynthComponentBase import *
try:
    import gettext
    _ = gettext.translation(domain='openhrivoice', localedir=os.path.dirname(__file__)+'/../share/locale').ugettext
except:
    _ = lambda s: s

__doc__ = _('Japanese speech synthesis component.')

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

class OpenJTalkWrap(VoiceSynthBase):
    def __init__(self):
        VoiceSynthBase.__init__(self)
        self._config = config()
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

    def synth(self, data):
        if self._fp is not None:
            self._fp.close()
            self._fp = None
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
        self._cmdarg.append(self._conf._openjtalk_bin)
        for o, v in self._args:
            self._cmdarg.append("-"+o)
            self._cmdarg.append(os.path.join(self._conf._openjtalk_phonemodel_ja, v))
        self._cmdarg.append("-x")
        self._cmdarg.append(self._conf._openjtalk_dicfile_ja)
        self._cmdarg.append("-ow")
        self._cmdarg.append(self._wavfile)
        self._cmdarg.append("-ot")
        self._cmdarg.append(self._logfile)
        self._cmdarg.append(self._textfile)
        # run OpenJTalk
        p = subprocess.Popen(self._cmdarg)
        p.wait()
        # read duration data
        d = parseopenjtalk()
        d.parse(self._logfile)
        self._durationdata = d.toseg().encode("utf-8")
        # read data
        self._fp = wave.open(self._wavfile, 'rb')
        #self._channels = wf.getnchannels()
        #self._samplebytes = wf.getsampwidth()
        self._samplerate = self._fp.getframerate()
        os.remove(self._textfile)
        os.remove(self._logfile)
    
    def terminate(self):
        pass

class OpenJTalkWrap2(VoiceSynthBase):
    def __init__(self):
        VoiceSynthBase.__init__(self)
        self._config = config()
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
        # command line for OpenJTalk
        self._moduleport = self.getunusedport()
        self._cmdarg = []
        self._cmdarg.append(self._conf._openjtalk_bin)
        for o, v in self._args:
            self._cmdarg.append("-"+o)
            self._cmdarg.append(os.path.join(self._conf._openjtalk_phonemodel_ja, v))
        self._cmdarg.append("-x")
        self._cmdarg.append(self._conf._openjtalk_dicfile_ja)
        self._cmdarg.append("-w")
        self._cmdarg.append(str(self._moduleport))
        # run OpenJTalk
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

    def synth(self, data):
        self._modulesocket.sendall(data.encode("utf-8")+"\n")
        # read duration data
        d = ""
        l = self._modulesocket.getline()
        while l != "" and l != "LABELEND":
            d += l + "\n"
            l = self._modulesocket.getline()
        dd = parseopenjtalk(d)
        self._durationdata = dd.toseg().encode("utf-8")
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
                     "description",       __doc__.encode('UTF-8'),
                     "version",           __version__,
                     "vendor",            "AIST",
                     "category",          "communication",
                     "activity_type",     "DataFlowComponent",
                     "max_instance",      "5",
                     "language",          "Python",
                     "lang_type",         "script",
                     "conf.default.format", "int16",
                     "conf.__widget__.format", "radio",
                     "conf.__constraints__.format", "int16",
                     "conf.__description__.format", _("Format of output audio (fixed to 16bit).").encode('UTF-8'),
                     "conf.default.rate", "16000",
                     "conf.__widget__.rate", "spin",
                     "conf.__constraints__.rate", "16000",
                     "conf.__description__.rate", _("Sampling frequency of output audio (fixed to 16kHz).").encode('UTF-8'),
                     "conf.default.character", "male",
                     "conf.__widget__.character", "radio",
                     "conf.__constraints__.character", "male",
                     "conf.__description__.character", _("Character of the voice (fixed to male).").encode('UTF-8'),
                     ""]

class OpenJTalkRTC(VoiceSynthComponentBase):
    def __init__(self, manager):
        VoiceSynthComponentBase.__init__(self, manager)

    def onInitialize(self):
        VoiceSynthComponentBase.onInitialize(self)
        self._wrap = OpenJTalkWrap()
        return RTC.RTC_OK
    
class OpenJTalkRTCManager:
    def __init__(self):
        encoding = locale.getpreferredencoding()
        sys.stdout = codecs.getwriter(encoding)(sys.stdout, errors = "replace")
        sys.stderr = codecs.getwriter(encoding)(sys.stderr, errors = "replace")

        parser = utils.MyParser(version=__version__, description=__doc__)
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
    manager = OpenJTalkRTCManager()
    manager.start()

if __name__=='__main__':
    main()
