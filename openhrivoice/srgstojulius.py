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

__doc__ = 'Generate Julius grammar from the W3C-SRGS grammar.'

__examples__ = '''
Examples:

- Generate Julius grammar fron the W3C-SRGS grammar.

  ::
  
  $ srgstojulius sample.grxml > sample.julius
'''

def main():
    sys.stdin = codecs.getreader('utf-8')(sys.stdin)
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
    
    class MyParser(optparse.OptionParser):
        def format_epilog(self, formatter):
            return self.epilog

    parser = MyParser(version=__version__, usage="%prog [grammarfile]",
                      description=__doc__, epilog=__examples__)
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
