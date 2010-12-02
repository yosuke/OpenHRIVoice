#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Utility script to convert W3C SRGS to Julius

Copyright (C) 2010
    Yosuke Matsusaka
    Intelligent Systems Research Institute,
    National Institute of Advanced Industrial Science and Technology (AIST),
    Japan
    All rights reserved.
Licensed under the Eclipse Public License -v 1.0 (EPL)
http://www.opensource.org/licenses/eclipse-1.0.txt
'''

import sys, os, re, codecs, getopt
from parsesrgs import *

def usage():
    print "usage: %s [grammarfile]" % (os.path.basename(sys.argv[0]),)

def main():
    sys.stdin = codecs.getreader('utf-8')(sys.stdin)
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
    opts, args = getopt.getopt(sys.argv[1:], 'r:')
    if len(args) != 1:
        usage()
        sys.exit()
    targetrule = None
    for o, a in opts:
        if o == "-r":
            targetrule = a
    srgs = SRGS(args[0])
    print srgs.toJulius(targetrule)

if __name__ == '__main__':
    main()
