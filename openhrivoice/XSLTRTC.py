#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''XSLT component

Copyright (C) 2010
    Yosuke Matsusaka
    Intelligent Systems Research Institute,
    National Institute of Advanced Industrial Science and Technology (AIST),
    Japan
    All rights reserved.
Licensed under the Eclipse Public License -v 1.0 (EPL)
http://www.opensource.org/licenses/eclipse-1.0.txt
'''

import os, sys, time, traceback, getopt, codecs, locale
from lxml import etree
from StringIO import StringIO
import OpenRTM_aist
import RTC

XSLTRTC_spec = ["implementation_id", "XSLTRTC",
                "type_name",         "XSLTRTC",
                "description",       "XSLT component (python implementation)",
                "version",           "1.0.0",
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
        data = OpenRTM_aist.ConnectorDataListenerT.__call__(self, info, cdrdata, RTC.TimedString(RTC.Time(0,0),""))
        self._obj.onData(self._name, data)

class XSLTRTC(OpenRTM_aist.DataFlowComponentBase):
    def __init__(self, manager):
        try:
            OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)
        except:
            print traceback.format_exc()

    def onInitialize(self):
        try:
            self._transform = None
            # create inport
            self._indata = RTC.TimedString(RTC.Time(0,0), "")
            self._inport = OpenRTM_aist.InPort("text", self._indata)
            self._inport.addConnectorDataListener(OpenRTM_aist.ConnectorDataListenerType.ON_BUFFER_WRITE,
                                                  DataListener("ON_BUFFER_WRITE", self))
            self.registerInPort("text", self._inport)
            # create outport for audio stream
            self._outdata = RTC.TimedString(RTC.Time(0,0), "")
            self._outport = OpenRTM_aist.OutPort("result", self._outdata)
            self.registerOutPort("result", self._outport)
        except:
            print traceback.format_exc()
        return RTC.RTC_OK
    
    def onData(self, name, data):
        try:
            #udata = data.data.decode("utf-8")
            udoc = etree.parse(StringIO(data.data))
            self._outdata.data = unicode(self._transform(udoc)).encode("utf-8")
            self._outport.write(self._outdata)
            print self._outdata.data.decode("utf-8")
        except:
            print traceback.format_exc()

    def onExecute(self, ec_id):
        time.sleep(1)
        return RTC.RTC_OK

class XSLTRTCManager:
    def __init__(self):
        try:
            opts, args = getopt.getopt(sys.argv[1:], "adlf:o:p:hg", ["help", "gui"])
        except getopt.GetoptError:
            usage()
            sys.exit()
        managerargs = [sys.argv[0]]
        for o, a in opts:
            if o in ("-a", "-d", "-l"):
                managerargs.append(o)
            if o in ("-f", "-o", "-p"):
                managerargs.append(o, a)
            if o in ("-h", "--help"):
                usage()
                sys.exit()
            if o in ("-g", "--gui"):
                import Tkinter, tkFileDialog
                root = Tkinter.Tk()
                root.withdraw()
                sel = tkFileDialog.askopenfilenames(title="select XSLT files")
                if isinstance(sel, unicode):
                    sel = root.tk.splitlist(sel)
                args.extend(sel)
        if len(args) < 1:
            usage()
            sys.exit()
        self._files = args
        self._comp = {}
        self._manager = OpenRTM_aist.Manager.init(managerargs)
        self._manager.setModuleInitProc(self.moduleInit)
        self._manager.activateManager()

    def start(self):
        self._manager.runManager(False)

    def moduleInit(self, manager):
        profile = OpenRTM_aist.Properties(defaults_str=XSLTRTC_spec)
        manager.registerFactory(profile, XSLTRTC, OpenRTM_aist.Delete)
        for a in self._files:
            self._comp[a] = manager.createComponent("XSLTRTC?exec_cxt.periodic.rate=1")
            xslt_doc = etree.parse(a)
            self._comp[a]._transform = etree.XSLT(xslt_doc)

def usage():
    print "usage: %s [-f rtc.conf] [--help] [--gui] [xsltfile]" % (os.path.basename(sys.argv[0]),)

def main():
    locale.setlocale(locale.LC_CTYPE, "")
    encoding = locale.getlocale()[1]
    if not encoding:
        encoding = "us-ascii"
    sys.stdout = codecs.getwriter(encoding)(sys.stdout, errors = "replace")
    sys.stderr = codecs.getwriter(encoding)(sys.stderr, errors = "replace")
    manager = XSLTRTCManager()
    manager.start()

if __name__=='__main__':
    main()
