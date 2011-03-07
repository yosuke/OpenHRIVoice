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
import os
import codecs
import optparse
from openhrivoice.__init__ import __version__
from lxml import etree
import locale
from openhrivoice import utils
try:
    import gettext
    _ = gettext.translation(domain='openhrivoice', localedir=os.path.dirname(__file__)+'/../share/locale').ugettext
except:
    _ = lambda s: s

__doc__ = _('Bundle multiple xincuded XML files to one file.')

def main():
    encoding = locale.getpreferredencoding()
    sys.stdout = codecs.getwriter(encoding)(sys.stdout, errors = "replace")
    sys.stderr = codecs.getwriter(encoding)(sys.stderr, errors = "replace")

    parser = utils.MyParser(version=__version__, usage="%prog [grammarfile]",
                            description=__doc__)
    parser.add_option('-v', '--verbose', dest='verbose', action='store_true',
                      default=False,
                      help=_('output verbose information'))
    try:
        opts, args = parser.parse_args()
    except optparse.OptionError, e:
        print >>sys.stderr, 'OptionError:', e
        return 1
        
    if len(args) == 0:
        parser.error("wrong number of arguments")
        return 1

    doc = etree.parse(args[0])
    doc.xinclude()
    print etree.tounicode(doc, pretty_print=True)
    return 0

if __name__ == '__main__':
    sys.exit(main())
