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
            u'a': 'a',
            u'b': 'b',
            u'ɓ': 'b_<',
            u'c': 'c',
            u'd': 'd',
            u'ɖ': 'd`',
            u'ɗ': 'd_<',
            u'e': 'e',
            u'f': 'f',
            u'ɡ': 'g',
            u'ɠ': 'g_<',
            u'h': 'h',
            u'ɦ': 'h\\',
            u'i': 'i',
            u'j': 'j',
            u'ʝ': 'j\\',
            u'k': 'k',
            u'l': 'l',
            u'ɭ': 'l`',
            u'ɺ': 'l\\',
            u'm': 'm',
            u'n': 'n',
            u'ɳ': 'n`',
            u'o': 'o',
            u'p': 'p',
            u'ɸ': 'p\\',
            u'q': 'q',
            u'r': 'r',
            u'ɽ': 'r`',
            u'ɹ': 'r\\',
            u'ɻ': 'r\`',
            u's': 's',
            u'ʂ': 's`',
            u'ɕ': 's\\',
            u't': 't',
            u'ʈ': 't`',
            u'u': 'u',
            u'v': 'v',
            u'ʋ': 'v\\',
            u'w': 'w',
            u'x': 'x',
            u'ɧ': 'x\\',
            u'y': 'y',
            u'z': 'z',
            u'ʐ': 'z`',
            u'ʑ': 'z\\',
            u'ɑ': 'A',
            u'β': 'B',
            u'ʙ': 'B\\',
            u'ç': 'C',
            u'ð': 'D',
            u'ɛ': 'E',
            u'ɱ': 'F',
            u'ɣ': 'G',
            u'ɢ': 'G\\',
            u'ʛ': 'G\_<',
            u'ɥ': 'H',
            u'ʜ': 'H\\',
            u'ɪ': 'I',
            u'ᵻ': 'I\\',
            u'ɲ': 'J',
            u'ɟ': 'J\\',
            u'ʄ': 'J\_<',
            u'ɬ': 'K',
            u'ɮ': 'K\\',
            u'ʎ': 'L',
            u'ʟ': 'L\\',
            u'ɯ': 'M',
            u'ɰ': 'M\\',
            u'ŋ': 'N',
            u'ɴ': 'N\\',
            u'ɔ': 'O',
            u'ʘ': 'O\\',
            u'ʋ': 'P',
            u'ɒ': 'Q',
            u'ʁ': 'R',
            u'ʀ': 'R\\',
            u'ʃ': 'S',
            u'θ': 'T',
            u'ʊ': 'U',
            u'ᵿ': 'U\\',
            u'ʌ': 'V',
            u'ʍ': 'W',
            u'χ': 'X',
            u'ħ': 'X\\',
            u'ʏ': 'Y',
            u'ʒ': 'Z',
            u'.': '.',
            u'ˈ': '"',
            u'ˌ': '%',
            u'ʲ': "'",
            u'ː': ': ',
            u'ˑ': ': \\',
            u'ə': '@',
            u'ɘ': '@\\',
            u'æ': '{',
            u'ʉ': '}',
            u'ɨ': '1',
            u'ø': '2',
            u'ɜ': '3',
            u'ɞ': '3\\',
            u'ɾ': '4',
            u'ɫ': '5',
            u'ɐ': '6',
            u'ɤ': '7',
            u'ɵ': '8',
            u'œ': '9',
            u'ɶ': '&',
            u'ʔ': '?',
            u'ʕ': '?\\',
            u'ʢ': '<\\',
            u'ʡ': '>\\',
            u'ǃ': '!\\',
            u'|': '|',
            u'ǀ': '|\\',
            u'‖': '||',
            u'ǁ': '|\\|\\',
            u'ǂ': '=\\',
            u'‿': '-\\'
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
