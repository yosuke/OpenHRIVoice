#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''CMU dict file parser

Copyright (C) 2010
    Yosuke Matsusaka
    Intelligent Systems Research Institute,
    National Institute of Advanced Industrial Science and Technology (AIST),
    Japan
    All rights reserved.
Licensed under the Eclipse Public License -v 1.0 (EPL)
http://www.opensource.org/licenses/eclipse-1.0.txt
'''

class CMUDict:
    """ Utility class to parse CMU Pronunciation Dictionaly."""

    def __init__(self, fname):
        self._fname = fname
        self._dict = {}
        self.parse(self._fname)

    def parse(self, fname):
        f = open(fname, 'r')
        f.readline()
        for l in f:
            t = l.strip().split(' ', 2)
            w = t[0].strip('()"')
            v = t[2].replace('(', '').replace(')', '').replace(' 0', '').replace(' 1', '')
            try:
                self._dict[w].append(v)
            except KeyError:
                self._dict[w] = [v,]

    def lookup(self, w):
        try:
            return self._dict[w]
        except KeyError:
            return []

if __name__ == '__main__':
    doc = CMUDict('/usr/share/festival/dicts/cmu/cmudict-0.4.out')
    print doc.lookup('hello')
    
