#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Wave file player component

Copyright (C) 2010-2011
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
try:
    import gettext
    _ = gettext.translation(domain='openhrivoice', localedir=os.path.dirname(__file__)+'/../share/locale').ugettext
except:
    _ = lambda s: s

__doc__ = _('Wave file player component.')

WavePlayerRTC_spec = ["implementation_id", "WavePlayerRTC",
                      "type_name",         "WavePlayerRTC",
                      "description",       __doc__.encode('UTF-8'),
                      "version",           __version__,
                      "vendor",            "AIST",
                      "category",          "communication",
                      "activity_type",     "DataFlowComponent",
                      "max_instance",      "10",
                      "language",          "Python",
                      "lang_type",         "script",
                      "conf.default.file", "",
                      "conf.__description__.file", _("Wave file.").encode('UTF-8'),
                      "conf.default.repeat", "1",
                      "conf.__widget__.repeat", "radio",
                      "conf.__constraints__.repeat", "(0, 1)",
                      "conf.__description__.repeat", _("Loop play mode.").encode('UTF-8'),
                      ""]

class WavePlayerRTC(OpenRTM_aist.DataFlowComponentBase):
    def __init__(self, manager):
        OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)
        self._repeat = [1,]
        self._file = ['',]
        self._prevtime = 0.0

    def onInitialize(self):
        OpenRTM_aist.DataFlowComponentBase.onInitialize(self)
        self._logger = OpenRTM_aist.Manager.instance().getLogbuf(self._properties.getProperty("instance_name"))
        self._logger.RTC_INFO(self._properties.getProperty("type_name") + " version " + self._properties.getProperty("version"))
        self._logger.RTC_INFO("Copyright (C) 2010-2011 Yosuke Matsusaka")
        #self.bindParameter("file", self._file, self._file)
        self.bindParameter("repeat", self._repeat, self._repeat[0])
        self._data = RTC.TimedOctetSeq(RTC.Time(0,0), None)
        self._port = OpenRTM_aist.OutPort("data", self._data)
        self._port.appendProperty('description', _('Audio data.').encode('UTF-8'))
        self.addOutPort(self._port._name, self._port)
        return RTC.RTC_OK

    def onActivated(self, ec_id):
        OpenRTM_aist.DataFlowComponentBase.onActivated(self, ec_id)
        try:
            self._stream = wave.open(self._file[0], 'rb')
        except IOError:
            return RTC.RTC_ERROR
        self._prevtime = time.clock() - 1.0
        return RTC.RTC_OK

    def onExecute(self, ec_id):
        OpenRTM_aist.DataFlowComponentBase.onExecute(self, ec_id)
        now = time.clock()
        chunk = int(self._stream.getframerate() * (now - self._prevtime))
        if chunk > 0:
            self._prevtime = now
            self._data.data = self._stream.readframes(chunk)
            if (self._repeat[0] != 0 and self._data.data == ''):
                self._stream.rewind()
                self._data.data = self._stream.readframes(chunk)
            self._port.write(self._data)
        return RTC.RTC_OK

class WavePlayerRTCManager:
    def __init__(self):
        encoding = locale.getpreferredencoding()
        sys.stdout = codecs.getwriter(encoding)(sys.stdout, errors = "replace")
        sys.stderr = codecs.getwriter(encoding)(sys.stderr, errors = "replace")

        parser = utils.MyParser(version=__version__, description=__doc__)
        utils.addmanageropts(parser)
        parser.add_option('-g', '--gui', dest='guimode', action="store_true",
                          default=False,
                          help=_('show file open dialog in GUI'))
        try:
            opts, args = parser.parse_args()
        except optparse.OptionError, e:
            print >>sys.stderr, 'OptionError:', e
            sys.exit(1)

        if opts.guimode == True:
            sel = utils.askopenfilename(title="select wave file")
            if sel is not None:
                args.append(sel)
    
        if len(args) != 1:
            parser.error("wrong number of arguments")
            sys.exit(1)

        self._file = args[0]
        self._comp = None
        self._manager = OpenRTM_aist.Manager.init(utils.genmanagerargs(opts))
        self._manager.setModuleInitProc(self.moduleInit)
        self._manager.activateManager()

    def start(self):
        self._manager.runManager(False)

    def moduleInit(self, manager):
        profile=OpenRTM_aist.Properties(defaults_str=WavePlayerRTC_spec)
        manager.registerFactory(profile, WavePlayerRTC, OpenRTM_aist.Delete)
        self._comp = manager.createComponent("WavePlayerRTC")
        self._comp._file[0] = self._file

def main():
    manager = WavePlayerRTCManager()
    manager.start()

if __name__=='__main__':
    main()
