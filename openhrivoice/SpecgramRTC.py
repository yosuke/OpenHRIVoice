#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Spectrogram visualization component

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
import codecs
import locale
import optparse
import numpy
import matplotlib
if sys.platform == "win32":
    matplotlib.use('tkagg')
import matplotlib.pyplot
import OpenRTM_aist
import RTC
from openhrivoice.__init__ import __version__
from openhrivoice import utils
try:
    import gettext
    _ = gettext.translation(domain='openhrivoice', localedir=os.path.dirname(__file__)+'/../share/locale').ugettext
except:
    _ = lambda s: s

__doc__ = _('Spectrogram visualization component.')

SpecgramRTC_spec = ["implementation_id", "SpecgramRTC",
                    "type_name",         "SpecgramRTC",
                    "description",       __doc__.encode('UTF-8'),
                    "version",           __version__,
                    "vendor",            "AIST",
                    "category",          "communication",
                    "activity_type",     "DataFlowComponent",
                    "max_instance",      "10",
                    "language",          "Python",
                    "lang_type",         "script",
                    ""]

class DataListener(OpenRTM_aist.ConnectorDataListenerT):
    def __init__(self, name, obj):
        self._name = name
        self._obj = obj
    
    def __call__(self, info, cdrdata):
        data = OpenRTM_aist.ConnectorDataListenerT.__call__(self, info, cdrdata, RTC.TimedOctetSeq(RTC.Time(0,0),None))
        self._obj.onData(self._name, data)

class SpecgramRTC(OpenRTM_aist.DataFlowComponentBase):
    def __init__(self, manager):
        try:
            OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)
            self._NFFT = 256
            self._Fs = 16000
            self._noverlap = 128
            self._recordlen = int(self._Fs * 5.0)
            self._x = numpy.ones(self._recordlen)
        except:
            self._logger.RTC_ERROR(traceback.format_exc())

    def onInitialize(self):
        try:
            OpenRTM_aist.DataFlowComponentBase.onInitialize(self)
            self._logger = OpenRTM_aist.Manager.instance().getLogbuf(self._properties.getProperty("instance_name"))
            self._logger.RTC_INFO(self._properties.getProperty("type_name") + " version " + self._properties.getProperty("version"))
            self._logger.RTC_INFO("Copyright (C) 2010-2011 Yosuke Matsusaka")
            # create inport
            self._indata = RTC.TimedOctetSeq(RTC.Time(0,0), None)
            self._inport = OpenRTM_aist.InPort("data", self._indata)
            self._inport.appendProperty('description', _('Audio data input.').encode('UTF-8'))
            self._inport.addConnectorDataListener(OpenRTM_aist.ConnectorDataListenerType.ON_BUFFER_WRITE,
                                                  DataListener("ON_BUFFER_WRITE", self))
            self.addInPort(self._inport._name, self._inport)
        except:
            self._logger.RTC_ERROR(traceback.format_exc())
        return RTC.RTC_OK
    
    def onData(self, name, data):
        try:
            self._x = numpy.concatenate((self._x, numpy.fromstring(data.data, numpy.int16)))
            self._x = self._x[-self._recordlen:]
        except:
            self._logger.RTC_ERROR(traceback.format_exc())

    def onExecute(self, ec_id):
        try:
            OpenRTM_aist.DataFlowComponentBase.onExecute(self, ec_id)
            matplotlib.pyplot.specgram(numpy.asarray(self._x), NFFT=self._NFFT, Fs=self._Fs, noverlap=self._noverlap)
        except:
            self._logger.RTC_ERROR(traceback.format_exc())
        return RTC.RTC_OK

class SpecgramRTCManager:
    def __init__(self):
        encoding = locale.getpreferredencoding()
        sys.stdout = codecs.getwriter(encoding)(sys.stdout, errors = "replace")
        sys.stderr = codecs.getwriter(encoding)(sys.stderr, errors = "replace")

        parser = utils.MyParser(version=__version__, usage="%prog",
                                description=__doc__)
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
        profile = OpenRTM_aist.Properties(defaults_str=SpecgramRTC_spec)
        manager.registerFactory(profile, SpecgramRTC, OpenRTM_aist.Delete)
        self._comp = manager.createComponent("SpecgramRTC")
        matplotlib.pyplot.subplot('111')
        matplotlib.pyplot.show()

def main():
    manager = SpecgramRTCManager()
    manager.start()

if __name__=='__main__':
    main()
