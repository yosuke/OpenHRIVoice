#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Utility script to generate W3C SRGS grammar from W3C PLS lexicon

Copyright (C) 2010
    Yosuke Matsusaka
    Intelligent Systems Research Institute,
    National Institute of Advanced Industrial Science and Technology (AIST),
    Japan
    All rights reserved.
Licensed under the Eclipse Public License -v 1.0 (EPL)
http://www.opensource.org/licenses/eclipse-1.0.txt
'''

import sys, os, codecs
from parsesrgs import PLS

def usage():
    print "usage: %s [lexiconfile]" % (os.path.basename(sys.argv[0]),)

def main():
    sys.stdin = codecs.getreader('utf-8')(sys.stdin)
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
    if len(sys.argv) != 2:
        usage()
        sys.exit()
    lex = PLS().parse([sys.argv[1],])
    print '''<?xml version="1.0" encoding="UTF-8" ?>
<grammar xmlns="http://www.w3.org/2001/06/grammar"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://www.w3.org/2001/06/grammar
                             http://www.w3.org/TR/speech-grammar/grammar.xsd"
         xml:lang="jp"
         version="1.0" mode="voice" root="command">
'''
    print '  <lexicon uri="%s"/>' % (sys.argv[1],)
    print '''
  <rule id="command">
    <one-of>'''
    for w in lex._dict.keys():
        print '      <item>%s</item>' % (w,)
    print '''    </one-of>
  </rule>
</grammar>
'''

if __name__ == '__main__':
    main()
    
