#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''sampa to simon converter

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

class sampa2simon:
    def __init__(self):
        self._phonemes = [
            'Enas:',
            'a:',
            'b',
            '@',
            'n',
            'ts',
            'R',
            'a',
            'x',
            'X',
            't',
            'l',
            's',
            'm',
            'p',
            'f',
            'N',
            'S',
            'e:',
            'v',
            'O',
            'r',
            'aU',
            'E',
            'C',
            'g',
            'I',
            'k',
            'd',
            'dZ',
            'aI',
            'u:',
            'o:',
            'U',
            'h',
            'i:',
            'z',
            'Y',
            'OY',
            'O',
            'i',
            'y:',
            'o',
            'e',
            'oeh:',
            'pf',
            'j',
            'E:',
            'oeh',
            'oe',
            'oe:',
            'U:',
            'u',
            'ah',
            'y',
            'O:',
            'Z',
            'N=',
            'n=',
            'A:',
            'm=',
            'l=',
            'A',
            'OI',
            '&',
            'EI',
            'w',
            's:',
            'h:',
            'Y:',
            'I:',
            'Q',
            'gls',
            'Onas',
            'Enas',
            'Anas',
            'enas',
            'onas',
            'Onsb',
            'Ensb',
            'Ansb',
            'ensb',
            'onsb',
            'Onas:',
            'Enas:',
            'Anas:',
            'enas:',
            'onas:',
            'Onsb:',
            'Ensb:',
            'Ansb:',
            'ensb:',
            'onsb:',
            'H',
            'B',
            'dz',
            'tS',
            'tK',
            'kp',
            'gb',
            'Nm',]
        self._dict = {}
        for i in self._phonemes:
            self._dict[i] = i

    def convert(self, text):
        text = text.replace('6', 'ah');
        text = text.replace('2', 'oeh');
        text = text.replace('~', 'nas');
        text = text.replace('<', 'nsb');
        text = text.replace('_', '');
        text = text.replace('^', '');
        text = text.replace('?', 'gls');
        text = text.replace('9', 'oe');
        ret = ''
        for i in text.split(' '):
            try:
                ret = ret + ' ' + self._dict[i]
            except KeyError:
                pass
        return ret.strip(' ')

def main():
    import sys, codecs, parsesrgs, ipa2sampa
    sys.stdin = codecs.getreader('utf-8')(sys.stdin)
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
    i2s = ipa2sampa.ipa2sampa()
    s2s = sampa2simon()
    pls = parsesrgs.PLS()
    pls.parse([sys.argv[1],])
    for i, s in pls._alphabet.iteritems():
        i2s.extend(i, s)
    for k in pls._dict.keys():
        for p in pls._dict[k]:
            print k.lower() + ": " + p + " -> " + s2s.convert(i2s.convert(p))

if __name__ == '__main__':
    main()
