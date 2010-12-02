#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Julius dict file parser

Copyright (C) 2010
    Yosuke Matsusaka
    Intelligent Systems Research Institute,
    National Institute of Advanced Industrial Science and Technology (AIST),
    Japan
    All rights reserved.
Licensed under the Eclipse Public License -v 1.0 (EPL)
http://www.opensource.org/licenses/eclipse-1.0.txt
'''

from string import maketrans

class JuliusDict:
    """ Utility class to parse Julius Pronunciation Dictionaly."""

    hira = u'がぎぐげござじずぜぞだぢづでどばびぶべぼぱぴぷぺぽ' + \
           u'あいうえおかきくけこさしすせそたちつてと' + \
           u'なにぬねのはひふへほまみむめもやゆよらりるれろ' + \
           u'わをんぁぃぅぇぉゃゅょっ'
    kata = u'ガギグゲゴザジズゼゾダヂヅデドバビブベボパピプペポ' + \
           u'アイウエオカキクケコサシスセソタチツテト' + \
           u'ナニヌネノハヒフヘホマミムメモヤユヨラリルレロ' + \
           u'ワヲンァィゥェォャュョッ'

    def __init__(self, fname):
        self._fname = fname
        self._dict = {}
        self.kanamap = {}
        for i in range(0, len(self.hira)):
            self.kanamap[ord(self.kata[i])] = self.hira[i]
        self.parse(self._fname)
        
    def katakana2hiragana(self, str):
        return str.translate(self.kanamap)

    def parse(self, fname):
        f = open(fname, 'r')
        for l in f:
            t = l.decode('euc-jp', 'ignore').split(':', 2)
            if len(t) > 2:
                st = self.katakana2hiragana(t[1]).replace('{','').replace('}','').split('/')
                try:
                    self._dict[t[0]].extend(st)
                except KeyError:
                    self._dict[t[0]] = st

    def lookup(self, w):
        try:
            return list(set(self._dict[w]))
        except KeyError:
            return []

if __name__ == '__main__':
    doc = JuliusDict('/usr/share/julius-runkit/model/lang_m/web.60k.htkdic')
    print doc.lookup(u'こんにちは')
    
