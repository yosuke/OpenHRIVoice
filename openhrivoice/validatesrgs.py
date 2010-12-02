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

import sys, os, getopt, codecs, locale
from lxml import etree
from parsesrgs import *

def usage():
    print "usage: %s [--help] [--gui] [grammarfile]" % (os.path.basename(sys.argv[0]),)
        
def main():
    global guimode
    
    locale.setlocale(locale.LC_CTYPE, "")
    encoding = locale.getlocale()[1]
    if not encoding:
        encoding = "us-ascii"
    sys.stdout = codecs.getwriter(encoding)(sys.stdout, errors = "replace")
    sys.stderr = codecs.getwriter(encoding)(sys.stderr, errors = "replace")

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hg", ["help", "gui"])
    except getopt.GetoptError:
        usage()
        sys.exit()
    guimode = False
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        if o in ("-g", "--gui"):
            import Tkinter, tkFileDialog
            root = Tkinter.Tk()
            root.withdraw()
            args.append(tkFileDialog.askopenfilename(title="select W3C-SRGS grammar file"))
            guimode = True
    if len(args) != 1:
        usage()
        sys.exit()
    if hasattr(sys, "frozen"):
        basedir = os.path.dirname(unicode(sys.executable, sys.getfilesystemencoding()))
    else:
        basedir = os.path.dirname(__file__)
        
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
    except IOError:
        print "[error] Cannot open PLS file: %s" % (",".join(srgs._lex),)
        myexit()
    try:
        xmlschema2.assert_(doc4)
        print "PLS file is valid."
    except AssertionError, b:
        print "[error] Invalid PLS file."
        print b
        myexit()
    myexit()

def myexit():
    global guimode
    if guimode == True:
        raw_input("Press Enter to Exit")
    sys.exit()

if __name__ == '__main__':
    main()
