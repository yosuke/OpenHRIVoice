#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Utility script to generate W3C-PLS from W3C-SRGS

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
import re
import platform
import getopt
import ctypes
import codecs

from parsesrgs import *
#from parsecmudict import *
from parsevoxforgedict import *
from parsejuliusdict import *

def usage():
    print "usage: %s [--help] [--gui] [grammarfile]" % (os.path.basename(sys.argv[0]),)
        
def main():
    outfile = sys.stdout
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hg", ["help", "gui"])
    except getopt.GetoptError:
        usage()
        sys.exit()
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        if o in ("-g", "--gui"):
            import Tkinter, tkFileDialog
            root = Tkinter.Tk()
            root.withdraw()
            args.append(tkFileDialog.askopenfilename(title="select W3C-SRGS grammar file"))
            outfile = tkFileDialog.asksaveasfile()
    outfile = codecs.getwriter('utf-8')(outfile)
    if len(args) != 1:
        usage()
        sys.exit()
    srgs = SRGS(args[0])
    if hasattr(sys, "frozen"):
        basedir = os.path.dirname(unicode(sys.executable, sys.getfilesystemencoding()))
    else:
        basedir = os.path.dirname(__file__)
    if srgs._lang == "jp":
        alphabet = "X-KANA"        
        if platform.system() == "Windows":
            dic = JuliusDict(os.path.join(basedir, 'dictation-kit-v4.0-win\model\lang_m\web.60k.htkdic'))
        else:
            dic = JuliusDict('/usr/share/julius-runkit/model/lang_m/web.60k.htkdic')
    else:
        alphabet = "X-ARPAbet"
        if platform.system() == "Windows":
            dic = VoxforgeDict(os.path.join(basedir, 'julius-voxforge-build726\dict'))
        else:
            dic = VoxforgeDict('/usr/share/doc/julius-voxforge/dict.gz')
    print >> outfile, '''<?xml version="1.0" encoding="UTF-8"?>
<lexicon version="1.0"
     xmlns="http://www.w3.org/2005/01/pronunciation-lexicon"
     xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
     xsi:schemaLocation="http://www.w3.org/2005/01/pronunciation-lexicon
                         http://www.w3.org/TR/2007/CR-pronunciation-lexicon-20071212/pls.xsd"
     alphabet="'''+alphabet+'''" xml:lang="'''+srgs._lang+'''">'''
    for w in set(srgs.wordlist()):
        print >> outfile, '  <lexeme>'
        print >> outfile, '    <grapheme>'+w+'</grapheme>'
        for r in dic.lookup(w):
            print >> outfile, '    <phoneme>{{' + alphabet + '|' + r + '}}</phoneme>'
        print >> outfile, '  </lexeme>'
    print >> outfile, '</lexicon>'
    outfile.close()

if __name__ == '__main__':
    main()
