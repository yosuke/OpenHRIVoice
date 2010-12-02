#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''OpenJTalk log file parser

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

class parseopenjtalk:
    def __init__(self):
        self._durations = []

    def parse(self, fname):
        f = open(fname, 'r')
        f_duration = False
        for l in f:
            l = l.strip(' \n')
            if l == '[Output label]':
                f_duration = True
                continue
            elif l == '':
                f_duration = False
                continue
            if f_duration:
                try:
                    (btime, etime, v) = l.split(' ')
                    vv = v.split(':')[0].split('-')[1].split('+')[0]
                    self._durations.append((int(btime), int(etime), vv))
                except:
                    pass

    def parse2(self, v):
        for l in v.split('\n'):
            try:
                (btime, etime, v) = l.split(' ')
                vv = v.split(':')[0].split('-')[1].split('+')[0]
                self._durations.append((int(btime), int(etime), vv))
            except:
                pass

    def toseg(self):
        s = u'#\n'
        for d in self._durations:
            t = float(d[1]-d[0])/1000000
            s += u'%f 125 %s\n' % (t, d[2])
        return s

def main():
    d = parseopenjtalk()
    d.parse(sys.argv[1])
    print d.toseg()

if __name__=='__main__':
    main()
