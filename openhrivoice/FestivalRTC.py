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
from openhrivoice.__init__ import __version__
from openhrivoice import utils
from openhrivoice.VoiceSynthComponentBase import *
try:
    import gettext
    _ = gettext.translation(domain='openhrivoice', localedir=os.path.dirname(__file__)+'/../share/locale').ugettext
except:
    _ = lambda s: s

__doc__ = _('English speech synthesis component.')

class FestivalWrap(VoiceSynthBase):
    def __init__(self):
        VoiceSynthBase.__init__(self)
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
        
    def synth(self, data):
        if self._fp is not None:
            self._fp.close()
            self._fp = None
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
        self._fp = wave.open(self._wavfile, 'rb')
        #self._channels = self._fp.getnchannels()
        #self._samplebytes = self._fp.getsampwidth()
        self._samplerate = self._fp.getframerate()
        df = open(self._durfile, 'r')
        self._durationdata = df.read().encode("utf-8")
        df.close()
        os.remove(self._durfile)
        
FestivalRTC_spec = ["implementation_id", "FestivalRTC",
                    "type_name",         "FestivalRTC",
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

class FestivalRTC(VoiceSynthComponentBase):
    def __init__(self, manager):
        VoiceSynthComponentBase.__init__(self, manager)

    def onInitialize(self):
        VoiceSynthComponentBase.onInitialize(self)
        self._wrap = FestivalWrap()
        return RTC.RTC_OK


class FestivalRTCManager:
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
        profile=OpenRTM_aist.Properties(defaults_str=FestivalRTC_spec)
        manager.registerFactory(profile, FestivalRTC, OpenRTM_aist.Delete)
        self._comp = manager.createComponent("FestivalRTC")

def main():
    manager = FestivalRTCManager()
    manager.start()

if __name__=='__main__':
    main()
