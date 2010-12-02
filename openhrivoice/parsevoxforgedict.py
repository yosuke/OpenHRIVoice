#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Voxforge dict file parser

Copyright (C) 2010
    Yosuke Matsusaka
    Intelligent Systems Research Institute,
    National Institute of Advanced Industrial Science and Technology (AIST),
    Japan
    All rights reserved.
Licensed under the Eclipse Public License -v 1.0 (EPL)
http://www.opensource.org/licenses/eclipse-1.0.txt
'''

import re
import gzip

class VoxforgeDict:
    """ Utility class to parse Voxforge Pronunciation Dictionaly."""

    def __init__(self, fname):
        self._fname = fname
        self._dict = {}
        self.parse(self._fname)

    def parse(self, fname):
        if fname[-3:] == '.gz':
            f = gzip.open(fname, 'rb')
        else:
            f = open(fname, 'r')
        for l in f:
            t = re.split(r"\s+", l.strip(), 2)
            st = ' '.join(t[2].split(' ')[:-1])
            st = st.lower()
            try:
                self._dict[t[0]].append(st)
            except KeyError:
                self._dict[t[0]] = [st,]

    def lookup(self, w):
        try:
            return self._dict[w.upper()]
        except KeyError:
            return []

if __name__ == '__main__':
    doc = VoxforgeDict('/usr/share/doc/julius-voxforge/dict.gz')
    print doc.lookup('hello')
    
