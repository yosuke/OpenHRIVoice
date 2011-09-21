#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''W3C SRGS validator

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
import locale
import optparse
from openhrivoice.__init__ import __version__
from lxml import etree
from openhrivoice.parsesrgs import *
from openhrivoice import utils
try:
    import gettext
    _ = gettext.translation(domain='openhrivoice', localedir=os.path.dirname(__file__)+'/../share/locale').ugettext
except:
    _ = lambda s: s

__doc__ = _('Validate format of the SRGS grammar file.')

__examples__ = '''
Examples:

- '''+_('Validate format of the SRGS grammar.')+'''

  ::
  
  $ validatesrgs sample.grxml
'''

def main():
    global opts
    
    encoding = locale.getpreferredencoding()
    sys.stdout = codecs.getwriter(encoding)(sys.stdout, errors = "replace")
    sys.stderr = codecs.getwriter(encoding)(sys.stderr, errors = "replace")

    if hasattr(sys, "frozen"):
        basedir = os.path.dirname(unicode(sys.executable, sys.getfilesystemencoding()))
    else:
        basedir = os.path.dirname(__file__)

    parser = utils.MyParser(version=__version__, usage="%prog [grammarfile]",
                            description=__doc__, epilog=__examples__)
    parser.add_option('-v', '--verbose', dest='verbose', action='store_true',
                      default=False,
                      help=_('output verbose information'))
    parser.add_option('-g', '--gui', dest='guimode', action="store_true",
                      default=False,
                      help=_('show file open dialog in GUI'))
    try:
        opts, args = parser.parse_args()
    except optparse.OptionError, e:
        print >>sys.stderr, 'OptionError:', e
        sys.exit(1)

    if opts.guimode == True:
        args.append(utils.askopenfilename(title="select W3C-SRGS grammar file"))

    if len(args) == 0:
        parser.error("wrong number of arguments")
        sys.exit(1)

    parser = etree.XMLParser(dtd_validation = True)
    xmlschema_doc = etree.parse(os.path.join(basedir, 'grammar.xsd'))
    xmlschema = etree.XMLSchema(xmlschema_doc)
    print "Validating SRGS file %s..." % (args[0],)
    try:
        doc2 = etree.parse(args[0])
        doc2.xinclude()
    except etree.XMLSyntaxError, e:
        print "[error] invalid xml syntax"
        print e
        myexit()
    except IOError, e:
        print "[error] IO error: unable to open file ", args[0]
        print e
        myexit()
    try:
        xmlschema.assert_(doc2)
        print "SRGS file is valid."
    except AssertionError, b:
        print "[error] Invalid SRGS file."
        print b
        myexit()

    xmlschema2_doc = etree.parse(os.path.join(basedir, 'pls.xsd'))
    xmlschema2 = etree.XMLSchema(xmlschema2_doc)
    srgs = SRGS(args[0])
    try:
        for l in srgs._lex:
            print "Validating PLS file %s..." % (l,)
            doc4 = etree.parse(l)
            try:
                xmlschema2.assert_(doc4)
                print "PLS file is valid."
            except AssertionError, b:
                print "[error] Invalid PLS file."
                print b
                myexit()
    except IOError:
        print "[error] Cannot open PLS file: %s" % (",".join(srgs._lex),)
        myexit()
    myexit()

def myexit():
    global opts
    if opts.guimode == True:
        raw_input("Press Enter to Exit")
    sys.exit()

if __name__ == '__main__':
    main()
