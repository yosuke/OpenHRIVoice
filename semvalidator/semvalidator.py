#!/usr/bin/env python
# -*- coding: utf-8 -*-

# semantic validation tool
#           copyright 2010 Yosuke Matsusaka, AIST.

import os.path
import sys
from lxml import etree
from rtsprofile.rts_profile import RtsProfile
#from logilab import constraint
from traceback import print_exc

SEM_NS = "{http://openhri.net/RTCSemantics}"

class semanticrule:
    def __init__(self):
        self._scope = None
        self._property = None
        self._value = None
    def parse(self, doc):
        self._scope = doc.get(SEM_NS + "scope")
        self._property = doc.get(SEM_NS + "property")
        self._value = doc.text
        return self
    def eval(self, comp):
        if self._property == "id":
            return comp.id == self._value
        if self._property.startswith("configuration."):
            cname = self._property.split(".")[1]
            for c in comp.get_configuration_set_by_id(comp.active_configuration_set).configuration_data:
                if c.name == cname and c.data == self._value:
                    return True
            return False
    def __str__(self):
        return "rule<scope=%s,property=%s,value=%s>" % (self._scope, self._property, self._value)
        
class semanticitem:
    def __init__(self):
        self._name = None
        self._restrictions = []
        self._requirements = []
    def parse(self, doc):
        self._name = doc.get(SEM_NS + "name")
        req = doc.find(SEM_NS + "requirement")
        if req is not None:
            self._requirements = [semanticrule().parse(d) for d in req.findall(SEM_NS + "rule")]
        res = doc.find(SEM_NS + "restriction")
        if res is not None:
            self._restrictions = [semanticrule().parse(d) for d in res.findall(SEM_NS + "rule")]
        return self

class semantics:
    def __init__(self):
        self._items = []
    def parse(self, uri):
        doc = etree.parse(uri)
        sem = doc.find(SEM_NS + "semantics")
        self._items = [semanticitem().parse(d) for d in sem.findall(SEM_NS + "item")]
        return self

def listvalidate(list, rule):
    for c in list:
        if rule.eval(c) == True:
            return True
        try:
            if listvalidate(list[c], rule) == True:
                return True
        except KeyError:
            pass
    return False

def main(argv):
    input_name = argv[1]
    type = os.path.splitext(input_name)[1][1:]
    f = open(input_name)
    if type == 'xml':
        prof = RtsProfile(xml_spec=f)
    elif type == 'yaml':
        prof = RtsProfile(yaml_spec=f)
    else:
        print >>sys.stderr, 'Unknown input type: {0}'.format(type)
        return 1
    f.close()

    compdict = {}
    for comp in prof.components:
        sem = semantics().parse(comp.path_uri)
        compdict[comp.instance_name] = (comp, sem)
    
    upstreamlist = {}
    downstreamlist = {}
    for con in prof.data_port_connectors:
        src = compdict[con.source_data_port.instance_name][0]
        tgt = compdict[con.target_data_port.instance_name][0]
        try:
            upstreamlist[tgt].append(src)
        except KeyError:
            upstreamlist[tgt] = (src,)
        try:
            downstreamlist[src].append(tgt)
        except KeyError:
            downstreamlist[src] = (tgt,)

    systemvalid = True
    for (comp, sem) in compdict.values():
        print "validation for component %s" % (comp.instance_name,)
        compvalid = False
        for i in sem._items:
            resvalid = False
            if i._restrictions:
                for r in i._restrictions:
                    rulevalid = False
                    if r._scope == "this":
                        if r.eval(comp) == True:
                            rulevalid = True
                    elif r._scope.endswith(".allupstream"):
                        try:
                            if listvalidate(upstreamlist[comp], r) == True:
                                rulevalid = True
                        except KeyError:
                            rulevalid = False
                    elif r._scope.endswith(".alldownstream"):
                        try:
                            if listvalidate(downstreamlist[comp], r) == True:
                                rulevalid = True
                        except KeyError:
                            rulevalid = False
                    if rulevalid == True:
                        resvalid = True
            else:
                resvalid = False
            reqvalid = True
            if i._requirements:
                for r in i._requirements:
                    rulevalid = False
                    if r._scope == "this":
                        if r.eval(comp) == True:
                            rulevalid = True
                    elif r._scope.endswith(".allupstream"):
                        try:
                            if listvalidate(upstreamlist[comp], r) == True:
                                rulevalid = True
                        except KeyError:
                            rulevalid = False
                    elif r._scope.endswith(".alldownstream"):
                        try:
                            if listvalidate(downstreamlist[comp], r) == True:
                                rulevalid = True
                        except KeyError:
                            rulevalid = False
                    if rulevalid == False:
                        reqvalid = False
            else:
                reqvalid = True
            if resvalid == False and reqvalid == True:
                compvalid = True
                print "component is valid in semantics {%s}" % (i._name,)
        if compvalid == False:
            print "no valid semantics"
        if compvalid == False:
            systemvalid = False
    if systemvalid == True:
        print "system is valid"
    else:
        print "system is invalid"

if __name__ == '__main__':
    #sys.exit(main([None,"rtsystem-invalid.xml"]))
    #sys.exit(main([None,"rtsystem.xml"]))
    sys.exit(main(sys.argv))
