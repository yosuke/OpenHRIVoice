#!/usr/bin/env python
# -*- coding: utf-8 -*-

# An utility script to generate W3C-PLS from ipadic
#  copyright 2010 Yosuke Matsusaka, AIST

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
    alphabet = "X-KANA"
    dic = JuliusDict('/usr/share/julius-runkit/model/lang_m/web.60k.htkdic')
    f = open('/usr/share/mecab/dic/ipadic/Noun.name.csv', 'r')
    print '''<?xml version="1.0" encoding="UTF-8"?>
<lexicon version="1.0"
     xmlns="http://www.w3.org/2005/01/pronunciation-lexicon"
     xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
     xsi:schemaLocation="http://www.w3.org/2005/01/pronunciation-lexicon
                         http://www.w3.org/TR/2007/CR-pronunciation-lexicon-20071212/pls.xsd"
     alphabet="X-KANA" xml:lang="jp">'''
    flag = {}
    for l in f:
        v = l.decode('euc-jp').split(',')
        if v[7] == u'姓' and unicodedata.name(v[0][0])[0:4] == 'CJK ' and int(v[3]) < 7500 and not flag.has_key(v[0]) :
            flag[v[0]] = True
            print '  <lexeme>'
            print '    <grapheme>'+v[0]+'</grapheme>'
            try:
                for r in dic.lookup(v[0]):
                    print '    <phoneme>{{X-KANA|' + r + '}}</phoneme>'
            except KeyError:
                print '    <phoneme>{{X-KANA|' + dic.katakana2hiragana(v[11]) + '}}</phoneme>'
            print '  </lexeme>'
    print '</lexicon>'

if __name__ == '__main__':
    main()
