#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
import OpenRTM_aist
import RTC
 
consolein_spec = ["implementation_id", "ConsoleIn",
                  "type_name",         "ConsoleIn",
                  "description",       "Console input component",
                  "version",           "1.0",
                  "vendor",            "sample",
                  "category",          "example",
                  "activity_type",     "DataFlowComponent",
                  "max_instance",      "10",
                  "language",          "Python",
                  "lang_type",         "script",
                  ""]
 
class ConsoleIn(OpenRTM_aist.DataFlowComponentBase):
    def __init__(self, manager):
        OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)
        self._data = RTC.TimedString(RTC.Time(0,0),"")
        self._outport = OpenRTM_aist.OutPort("out", self._data)
 
    def onInitialize(self):
        self.registerOutPort("out", self._outport)
        return RTC.RTC_OK
 
    def onExecute(self, ec_id):
        self._data.data = "テストです"
        OpenRTM_aist.setTimestamp(self._data)
        self._outport.write()
        time.sleep(5)
        return RTC.RTC_OK
 
def MyModuleInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=consolein_spec)
    manager.registerFactory(profile,
                            ConsoleIn,
                            OpenRTM_aist.Delete)
    comp = manager.createComponent("ConsoleIn")
 
def main():
    mgr = OpenRTM_aist.Manager.init(sys.argv)
    mgr.setModuleInitProc(MyModuleInit)
    mgr.activateManager()
    mgr.runManager()
 
if __name__ == "__main__":
    main()