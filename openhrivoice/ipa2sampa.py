#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''ipa to sampa converter

Copyright (C) 2010
    Yosuke Matsusaka
    Intelligent Systems Research Institute,
    National Institute of Advanced Industrial Science and Technology (AIST),
    Japan
    All rights reserved.
Licensed under the Eclipse Public License -v 1.0 (EPL)
http://www.opensource.org/licenses/eclipse-1.0.txt
'''

# Mappings between ipa to sampa are referred from following web page:
# http://www.phon.ucl.ac.uk/home/sampa/index.html


import re

class ipa2sampa:
    def __init__(self):
        self._dict = {
            u'ɑ': 'A',
            u'æ': '{',
            u'ɐ': '6',
            u'ɒ': 'Q',
            u'ɛ': 'E',
            u'ə': '@',
            u'ɜ': '3',
            u'ɪ': 'I',
            u'ɔ': 'O',
            u'ø': '2',
            u'œ': '9',
            u'ɶ': '&',
            u'ʊ': 'U',
            u'ʉ': '}',
            u'ʌ': 'V',
            u'ʏ': 'Y',
            u'β': 'B',
            u'ç': 'C',
            u'ð': 'D',
            u'ɣ': 'G',
            u'ʎ': 'L',
            u'ɲ': 'J',
            u'ŋ': 'N',
            u'ʁ': 'R',
            u'ʃ': 'S',
            u'θ': 'T',
            u'ɥ': 'H',
            u'ʒ': 'Z',
            u'ʔ': '?',
            u'ː': ':',
            u'ˈ': '"',
            u'ˌ': '%',
            u'̩': '=n',
            u'̃': 'O~'
            }
        self._regex = None

    def extend(self, ipa, sampa):
        self._dict[ipa] = sampa
        self._regex = None

    def convert(self, text):
        if self._regex is None:
            self._regex = re.compile(u"(%s)" % u"|".join(map(re.escape, self._dict.keys())))
        ret = ' '.join(text)
        ret = self._regex.sub(lambda m: self._dict[m.string[m.start():m.end()]], ret) 
        ## clear all non alphabets
        #ret = re.sub(r'[^a-zA-Z :]', r'', ret)
        return ret.strip(" ")

def main():
    import sys, codecs, parsesrgs
    sys.stdin = codecs.getreader('utf-8')(sys.stdin)
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
    i2s = ipa2sampa()
    pls = parsesrgs.PLS()
    pls.parse([sys.argv[1],])
    for i, s in pls._alphabet.iteritems():
        i2s.extend(i, s)
    for k in pls._dict.keys():
        for p in pls._dict[k]:
            print k + ": " + i2s.convert(p)

if __name__ == '__main__':
    main()
