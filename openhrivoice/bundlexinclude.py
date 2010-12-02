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

import os
import sys
import codecs
from lxml import etree

def usage():
    print "usage: %s [grammarfile]" % (os.path.basename(sys.argv[0]),)

def main():
    sys.stdin = codecs.getreader('utf-8')(sys.stdin)
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
    if len(sys.argv) != 2:
        usage()
        return 1
    doc = etree.parse(sys.argv[1])
    doc.xinclude()
    print etree.tounicode(doc, pretty_print=True)
    return 0

if __name__ == '__main__':
    sys.exit(main())
