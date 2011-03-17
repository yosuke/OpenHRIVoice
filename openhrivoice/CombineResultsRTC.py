#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''CombineResultsRTC (combine results from speech recognizers)

Copyright (C) 2010
    Yosuke Matsusaka
    Intelligent Systems Research Institute,
    National Institute of Advanced Industrial Science and Technology (AIST),
    Japan
    All rights reserved.
Licensed under the Eclipse Public License -v 1.0 (EPL)
http://www.opensource.org/licenses/eclipse-1.0.txt
'''

import sys
import codecs
import time
import signal
import re
import traceback
import socket
import threading
import optparse
import OpenRTM_aist
import RTC
from xml.dom import minidom
from openhrivoice import utils
from openhrivoice.__init__ import __version__

__doc__ = 'Combine results from speech recognizers component.'

CombineResultsRTC_spec = ["implementation_id", "CombineResultsRTC",
                          "type_name",         "CombineResultsRTC",
                          "description",       "Combine Results from Speech Recognizers",
                          "version",           __version__,
                          "vendor",            "Yosuke Matsusaka, AIST",
                          "category",          "Speech",
                          "activity_type",     "DataFlowComponent",
                          "max_instance",      "1",
                          "language",          "Python",
                          "lang_type",         "script",
                          ""]

class DataListener(OpenRTM_aist.ConnectorDataListenerT):
    def __init__(self, name, obj):
        self._name = name
        self._obj = obj
    
    def __call__(self, info, cdrdata):
        data = OpenRTM_aist.ConnectorDataListenerT.__call__(self, info, cdrdata, RTC.TimedString(RTC.Time(0,0),""))
        self._obj.onData(self._name, data)

class CombineResultsRTC(OpenRTM_aist.DataFlowComponentBase):
    def __init__(self, manager):
        OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)
        self._data = {}
        self._port = {}
        self._statusports = ('status1', 'status2')
        self._resultports = ('result1', 'result2')
        self._results = {}
        self._maxprob = {}
        self._listening = 0

    def onInitialize(self):
        OpenRTM_aist.DataFlowComponentBase.onInitialize(self)
        self._logger = OpenRTM_aist.Manager.instance().getLogbuf(self._properties.getProperty("instance_name"))
        self._logger.RTC_INFO("CombineResultsRTC version " + __version__)
        self._logger.RTC_INFO("Copyright (C) 2010-2011 Yosuke Matsusaka")
        self.createInPort('status1', RTC.TimedString)
        self._port['status1'].appendProperty('description', 'Status of recognizer 1.')
        self.createInPort('result1', RTC.TimedString)
        self._port['result1'].appendProperty('description', 'Recognition result of recognizer 1.')
        self.createInPort('status2', RTC.TimedString)
        self._port['status2'].appendProperty('description', 'Status of recognizer 2.')
        self.createInPort('result2', RTC.TimedString)
        self._port['result2'].appendProperty('description', 'Recognition result of recognizer 2.')
        self.createOutPort('statusout', RTC.TimedString)
        self._port['statusout'].appendProperty('description', 'Status of both combined.')
        self.createOutPort('resultout', RTC.TimedString)
        self._port['resultout'].appendProperty('description', 'Recognition result of both combined.')
        return RTC.RTC_OK
    
    def createInPort(self, name, type=RTC.TimedString):
        self._logger.RTC_INFO("create inport: " + name)
        self._data[name] = type(RTC.Time(0,0), None)
        self._port[name] = OpenRTM_aist.InPort(name, self._data[name])
        self.registerInPort(name, self._port[name])
        self._port[name].addConnectorDataListener(OpenRTM_aist.ConnectorDataListenerType.ON_BUFFER_WRITE,
                                                  DataListener(name, self))
        self._results[name] = ''
        self._maxprob[name] = -float("inf")

    def createOutPort(self, name, type=RTC.TimedString):
        self._logger.RTC_INFO("create outport: " + name)
        self._data[name] = type(RTC.Time(0,0), None)
        self._port[name] = OpenRTM_aist.OutPort(name, self._data[name], OpenRTM_aist.RingBuffer(8))
        self.registerOutPort(name, self._port[name])

    def onData(self, name, data):
        try:
            self.processResult(name, data.data)
        except:
            self._logger.RTC_ERROR(traceback.format_exc())

    def onExecute(self, ec_id):
        OpenRTM_aist.DataFlowComponentBase.onExecute(self, ec_id)
        return RTC.RTC_OK

    def processResult(self, host, s):
        self._logger.RTC_INFO("got input %s (%s)" % (s, host))
        self._results[host] = s
        if host[:-1] == 'result':
            hearing = False
            for p in self._statusports:
                if self._results[p] == 'STARTREC':
                    hearing = True
            if hearing == False:
                results = list()
                for p in self._resultports:
                    if self._results[p] != '':
                        doc = minidom.parseString(self._results[p])
                        for s in doc.getElementsByTagName('data'):
                            prob = float(s.getAttribute('likelihood'))
                            if prob > self._maxprob[p]:
                                self._maxprob[p] = prob
                            results.append((prob/self._maxprob[p], s))
                results.sort(key = lambda x:x[0])
                doc = minidom.Document()
                listentext = doc.createElement("listenText")
                doc.appendChild(listentext)
                rank = 1
                for r in results:
                    listentext.appendChild(r[1])
                    r[1].setAttribute("rank", str(rank))
                    rank += 1
                retstr = doc.toxml(encoding="utf-8")
                self._logger.RTC_INFO(retstr)
                self._data['resultout'].data = retstr
                self._port['resultout'].write(self._data['resultout'])

class CombineResultsRTCManager:
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
        profile=OpenRTM_aist.Properties(defaults_str=CombineResultsRTC_spec)
        manager.registerFactory(profile, CombineResultsRTC, OpenRTM_aist.Delete)
        self._comp = manager.createComponent("CombineResultsRTC?exec_cxt.periodic.rate=1")

def main():
    manager = CombineResultsRTCManager()
    manager.start()

if __name__=='__main__':
    main()

