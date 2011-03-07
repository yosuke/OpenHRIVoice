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
import optparse
import ctypes
import codecs
import locale
from openhrivoice.parsesrgs import *
#from openhrivoice.parsecmudict import *
from openhrivoice.parsevoxforgedict import *
from openhrivoice.parsejuliusdict import *
from openhrivoice.__init__ import __version__
from openhrivoice import utils
try:
    import gettext
    _ = gettext.translation(domain='openhrivoice', localedir=os.path.dirname(__file__)+'/../share/locale').ugettext
except:
    _ = lambda s: s

__doc__ = _('Generate W3C-PLS lexcon from the W3C-SRGS grammar.')

__examples__ = '''
Examples:

- '''+_('Generate W3C-PLS lexcon from the W3C-SRGS grammar.')+'''

  ::
  
  $ srgstopls sample.grxml > sample-lex.xml
'''

def main():
    outfile = sys.stdout

    encoding = locale.getpreferredencoding()
    sys.stdout = codecs.getwriter(encoding)(sys.stdout, errors = "replace")
    sys.stderr = codecs.getwriter(encoding)(sys.stderr, errors = "replace")

    parser = utils.MyParser(version=__version__, usage="%prog [grammarfile]",
                            description=__doc__, epilog=__examples__)
    parser.add_option('-v', '--verbose', dest='verbose', action='store_true',
                      default=False,
                      help=_('output verbose information'))
    parser.add_option('-r', '--target-rule', dest='targetrule', action="store",
                      type="string",
                      help=_('specify target rule id'))
    parser.add_option('-g', '--gui', dest='guimode', action="store_true",
                      default=False,
                      help=_('show file open dialog in GUI'))
    try:
        opts, args = parser.parse_args()
    except optparse.OptionError, e:
        print >>sys.stderr, 'OptionError:', e
        sys.exit(1)

    if opts.guimode == True:
        sel = utils.askopenfilename(title="select W3C-SRGS grammar file")
        if sel is not None:
            args.append(sel)
        outname = utils.asksaveasfile()
        outfile = open(outname, 'w')
    
    if len(args) == 0:
        parser.error("wrong number of arguments")
        sys.exit(1)

    outfile = codecs.getwriter('utf-8')(outfile)

    srgs = SRGS(args[0])
    if hasattr(sys, "frozen"):
        basedir = os.path.dirname(unicode(sys.executable, sys.getfilesystemencoding()))
    else:
        basedir = os.path.dirname(__file__)
    if srgs._lang in ("jp", "ja"):
        alphabet = "x-KANA"
        meca = None
        if platform.system() == "Windows":
            dic = JuliusDict(os.path.join(basedir, 'dictation-kit-v4.0-win\model\lang_m\web.60k.htkdic'))
        else:
            try:
                import MeCab
                meca = MeCab.Tagger('-Oyomi')
            except:
                pass
            dic = JuliusDict('/usr/share/julius-runkit/model/lang_m/web.60k.htkdic')
    else:
        alphabet = "x-ARPAbet"
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
        prons = dic.lookup(w)
        if len(prons) == 0 and srgs._lang == "jp":
            if meca is not None:
                yomi = dic.katakana2hiragana(unicode(meca.parse(w.encode('euc-jp')), 'euc-jp').strip())
                prons.append(yomi.replace(u'う',u'ー').replace(u'ーー',u'ーう'))
        for r in prons:
            print >> outfile, '    <phoneme>{{' + alphabet + '|' + r + '}}</phoneme>'
        print >> outfile, '  </lexeme>'
    print >> outfile, '</lexicon>'
    outfile.close()

if __name__ == '__main__':
    main()
