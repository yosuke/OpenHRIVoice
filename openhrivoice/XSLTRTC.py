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

import os
import sys
import time
import traceback
import codecs
import locale
import optparse
from lxml import etree
from StringIO import StringIO
import OpenRTM_aist
import RTC
from openhrivoice.__init__ import __version__
from openhrivoice import utils
try:
    import gettext
    _ = gettext.translation(domain='openhrivoice', localedir=os.path.dirname(__file__)+'/../share/locale').ugettext
except:
    _ = lambda s: s

__doc__ = _('XML transformation component.')

XSLTRTC_spec = ["implementation_id", "XSLTRTC",
                "type_name",         "XSLTRTC",
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
        data = OpenRTM_aist.ConnectorDataListenerT.__call__(self, info, cdrdata, RTC.TimedString(RTC.Time(0,0),""))
        self._obj.onData(self._name, data)

class XSLTRTC(OpenRTM_aist.DataFlowComponentBase):
    def __init__(self, manager):
        OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)
        self._transform = None

    def onInitialize(self):
        OpenRTM_aist.DataFlowComponentBase.onInitialize(self)
        self._logger = OpenRTM_aist.Manager.instance().getLogbuf(self._properties.getProperty("instance_name"))
        self._logger.RTC_INFO("XSLTRTC version " + __version__)
        self._logger.RTC_INFO("Copyright (C) 2010-2011 Yosuke Matsusaka")
        # create inport
        self._indata = RTC.TimedString(RTC.Time(0,0), "")
        self._inport = OpenRTM_aist.InPort("text", self._indata)
        self._inport.appendProperty('description', _('Text data in XML format.').encode('UTF-8'))
        self._inport.addConnectorDataListener(OpenRTM_aist.ConnectorDataListenerType.ON_BUFFER_WRITE,
                                              DataListener("ON_BUFFER_WRITE", self))
        self.registerInPort(self._inport._name, self._inport)
        # create outport for audio stream
        self._outdata = RTC.TimedString(RTC.Time(0,0), "")
        self._outport = OpenRTM_aist.OutPort("result", self._outdata)
        self._outport.appendProperty('description', _('Text data in XML format (transformed).').encode('UTF-8'))
        self.registerOutPort(self._outport._name, self._outport)
        return RTC.RTC_OK
    
    def onData(self, name, data):
        try:
            #udata = data.data.decode("utf-8")
            udoc = etree.parse(StringIO(data.data))
            self._outdata.data = unicode(self._transform(udoc)).encode("utf-8")
            self._outport.write(self._outdata)
            self._logger.RTC_INFO(self._outdata.data.decode("utf-8"))
        except:
            self._logger.RTC_ERROR(traceback.format_exc())

    def onExecute(self, ec_id):
        OpenRTM_aist.DataFlowComponentBase.onExecute(ec_id)
        return RTC.RTC_OK

class XSLTRTCManager:
    def __init__(self):
        encoding = locale.getpreferredencoding()
        sys.stdout = codecs.getwriter(encoding)(sys.stdout, errors = "replace")
        sys.stderr = codecs.getwriter(encoding)(sys.stderr, errors = "replace")

        parser = utils.MyParser(version=__version__, usage="%prog [xsltfile]",
                                description=__doc__)
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
            sel = utils.askopenfilenames(title="select XSLT files")
            if sel is not None:
                args.extend(sel)
    
        if len(args) == 0:
            parser.error("wrong number of arguments")
            sys.exit(1)

        self._files = args
        self._comp = {}
        self._manager = OpenRTM_aist.Manager.init(utils.genmanagerargs(opts))
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

def main():
    manager = XSLTRTCManager()
    manager.start()

if __name__=='__main__':
    main()
