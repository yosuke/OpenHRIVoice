#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Utility script to generate hiragana n-gram from ipadic

Copyright (C) 2010
    Yosuke Matsusaka
    Intelligent Systems Research Institute,
    National Institute of Advanced Industrial Science and Technology (AIST),
    Japan
    All rights reserved.
Licensed under the Eclipse Public License -v 1.0 (EPL)
http://www.opensource.org/licenses/eclipse-1.0.txt
'''

'''Usage:
python ipadictohiraganangram.py > hiraganangram.txt
text2wfreq < hiraganangram.txt > hiraganangram.wfreq
wfreq2vocab < hiraganangram.wfreq > hiraganangram.vocab
text2idngram -n 2 -vocab hiraganangram.vocab < hiraganangram.txt > hiraganangram.id2gram
text2idngram -n 3 -vocab hiraganangram.vocab < hiraganangram.txt > hiraganangram.id3gram
reverseidngram hiraganangram.id3gram hiraganangram.revid3gram
idngram2lm -vocab_type 0 -n 3 -idngram hiraganangram.revid3gram -vocab hiraganangram.vocab -arpa hiraganangram.rev3gram.arpa
idngram2lm -vocab_type 0 -n 2 -idngram hiraganangram.id2gram -vocab hiraganangram.vocab -arpa hiraganangram.2gram.arpa
mkbingram -nlr hiraganangram.2gram.arpa -nrl hiraganangram.rev3gram.arpa hiraganangram.bingram
python hiragana2phoneme.py hiraganangram.vocab > hiraganangram.htkdic
'''

import sys
import os
import re
import getopt
import codecs
import unicodedata
from xml.dom import minidom

from parsejuliusdict import *

def usage():
    print "usage: %s [--help]" % (os.path.basename(sys.argv[0]),)
        
def main():
    sys.stdin = codecs.getreader('utf-8')(sys.stdin)
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", ["help",])
    except getopt.GetoptError:
        usage()
        sys.exit()
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
    if len(args) >= 1:
        usage()
        sys.exit()
    dic = JuliusDict('/usr/share/julius-runkit/model/lang_m/web.60k.htkdic')
    f = open('/usr/share/mecab/dic/ipadic/Noun.name.csv', 'r')
    flag = {}
    for l in f:
        v = l.decode('euc-jp').split(',')
        if v[7] == u'姓': # and not flag.has_key(v[0]):
            flag[v[0]] = True
            try:
                for w in dic.lookup(v[0]):
                    out = "<s>"
                    for c in w:
                        if c not in u"ぁぃぅぇぉゃゅょー":
                            out = out + " "
                        out = out + c
                    out = out + " </s>"
                    print out
            except KeyError:
                pass

if __name__ == '__main__':
    main()
