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

import sys
import codecs
import optparse
from parsesrgs import *
from __init__ import __version__

def main():
    sys.stdin = codecs.getreader('utf-8')(sys.stdin)
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
    
    parser = optparse.OptionParser(version=__version__, usage="%prog [grammarfile]")
    parser.add_option('-v', '--verbose', dest='verbose', action='store_true',
                      default=False,
                      help='output verbose information')
    parser.add_option('-r', '--target-rule', dest='targetrule', action="store",
                      type="string",
                      help='specify target rule id')
    try:
        opts, args = parser.parse_args()
    except optparse.OptionError, e:
        print >>sys.stderr, 'OptionError:', e
        sys.exit(1)

    if len(args) == 0:
        parser.error("wrong number of arguments")
        sys.exit(1)

    srgs = SRGS(args[0])
    print srgs.toJulius(opts.targetrule)

if __name__ == '__main__':
    main()
