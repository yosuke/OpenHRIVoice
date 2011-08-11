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

import os
import sys
import time
import urllib
import tempfile
import traceback
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

__doc__ = _('German speech synthesis component using MARY.')

class MARYTalkWrap(VoiceSynthBase):
    def __init__(self):
        VoiceSynthBase.__init__(self)
        self._baseurl = "http://localhost:59125/"
        self._voice_type = {}
        voiceinfo = urllib.urlopen(self._baseurl + 'voices').readlines()
        for v in voiceinfo:
            (id, lang, gender, type) = v.strip().split(' ', 3)
            if lang == 'de':
                self._voice_type[gender] = id
            
    def getaudio(self, data, character):
        query = [
                 ('INPUT_TYPE', 'TEXT'),
                 ('OUTPUT_TYPE', 'AUDIO'),
                 ('AUDIO', 'WAVE'),
                 ('LOCALE', 'de'),
                 ('VOICE', self._voice_type[character]),
                 ('INPUT_TEXT', data.encode('utf-8')),
                 ]
        maryurl = self._baseurl + 'process?' + urllib.urlencode(query)
        wavfile = self.gettempname()
        urllib.urlretrieve(maryurl, wavfile)
        return wavfile

    def getdurations(self, data, character):
        query = [
                 ('INPUT_TYPE', 'TEXT'),
                 ('OUTPUT_TYPE', 'REALISED_DURATIONS'),
                 ('AUDIO', 'WAVE'),
                 ('LOCALE', 'de'),
                 ('VOICE', self._voice_type[character]),
                 ('INPUT_TEXT', data.encode('utf-8')),
                 ]
        maryurl = self._baseurl + 'process?' + urllib.urlencode(query)
        f = urllib.urlopen(maryurl)
        d = f.read()
        f.close()
        #lasttime = float(d.split('\n')[-2].split(' ')[0])
        #d = '#\n0.001 125 sil\n' + '\n'.join(d.split('\n')[1:]) + ('%f 125 sil\n' % (lasttime + 0.001,))
        return d

    def synthreal(self, data, samplerate, character):
        wavfile = self.getaudio(data, character)
        durations = self.getdurations(data, character)
        return (durations, wavfile)

MARYRTC_spec = ["implementation_id", "MARYRTC",
                "type_name",         "MARYRTC",
                "description",       __doc__,
                "version",           __version__,
                "vendor",            "AIST",
                "category",          "communication",
                "activity_type",     "DataFlowComponent",
                "max_instance",      "5",
                "language",          "Python",
                "lang_type",         "script",
                "conf.default.format", "int16",
                "conf.default.rate", "16000",
                "conf.default.character", "male",
                "conf.__widget__.format", "radio",
                "conf.__constraints__.format", "(int16)",
                "conf.__description__.format", "Format of output audio (fixed to 16bit).",
                "conf.__widget__.rate", "spin",
                "conf.__constraints__.rate", "x == 16000",
                "conf.__description__.rate", "Sampling frequency of output audio (fixed to 16kHz).",
                "conf.__widget__.character", "radio",
                "conf.__constraints__.character", "(male, female)",
                "conf.__description__.character", "Character of the voice.",
                ""]

class MARYRTC(VoiceSynthComponentBase):
    def __init__(self, manager):
        VoiceSynthComponentBase.__init__(self, manager)

    def onInitialize(self):
        VoiceSynthComponentBase.onInitialize(self)
        try:
            self._wrap = MARYTalkWrap()
        except:
            self._logger.RTC_ERROR(traceback.format_exc())
            return RTC.RTC_ERROR
        return RTC.RTC_OK

class MARYRTCManager:
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
    manager = MARYRTCManager()
    manager.start()

if __name__=='__main__':
    main()
