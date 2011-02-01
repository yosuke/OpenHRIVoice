#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Utility script to bundle xincluded xml files to one file

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
from __init__ import __version__
from lxml import etree

def main():
    sys.stdin = codecs.getreader('utf-8')(sys.stdin)
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

    parser = optparse.OptionParser(version=__version__, usage="%prog [grammarfile]")
    parser.add_option('-v', '--verbose', dest='verbose', action='store_true',
                      default=False,
                      help='output verbose information')
    try:
        opts, args = parser.parse_args()
    except optparse.OptionError, e:
        print >>sys.stderr, 'OptionError:', e
        sys.exit(1)
        
    if len(args) == 0:
        parser.error("wrong number of arguments")
        sys.exit(1)

    doc = etree.parse(args[0])
    doc.xinclude()
    print etree.tounicode(doc, pretty_print=True)
    return 0

if __name__ == '__main__':
    sys.exit(main())
