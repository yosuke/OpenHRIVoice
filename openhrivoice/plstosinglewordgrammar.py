#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Utility script to generate W3C SRGS grammar from W3C PLS lexicon

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
import locale
from openhrivoice.parsesrgs import PLS
from openhrivoice.__init__ import __version__
from openhrivoice import utils
try:
    import gettext
    _ = gettext.translation(domain='openhrivoice', localedir=os.path.dirname(__file__)+'/../share/locale').ugettext
except:
    _ = lambda s: s

__doc__ = _('Generate W3C-SRGS grammar from the W3C-PLS pronounciation dictionary.')

__examples__ = '''
Examples:

- '''+_('Generate single words SRGS grammar from the PLS lexicon.')+'''

  ::
  
  $ plstosinglewordgrammar sample-lex.xml > sample.grxml
'''

def main():
    encoding = locale.getpreferredencoding()
    sys.stdout = codecs.getwriter(encoding)(sys.stdout, errors = "replace")
    sys.stderr = codecs.getwriter(encoding)(sys.stderr, errors = "replace")

    parser = utils.MyParser(version=__version__, usage="%prog [lexiconfile]",
                            description=__doc__, epilog=__examples__)
    parser.add_option('-v', '--verbose', dest='verbose', action='store_true',
                      default=False,
                      help=_('output verbose information'))
    try:
        opts, args = parser.parse_args()
    except optparse.OptionError, e:
        print >>sys.stderr, 'OptionError:', e
        sys.exit(1)

    if len(args) == 0:
        parser.error("wrong number of arguments")
        sys.exit(1)

    lex = PLS().parse([args[0],])

    sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
    print '''<?xml version="1.0" encoding="UTF-8" ?>
<grammar xmlns="http://www.w3.org/2001/06/grammar"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://www.w3.org/2001/06/grammar
                             http://www.w3.org/TR/speech-grammar/grammar.xsd"
         xml:lang="jp"
         version="1.0" mode="voice" root="command">
'''
    print '  <lexicon uri="%s"/>' % (args[0],)
    print '''
  <rule id="command">
    <one-of>'''
    for w in lex._dict.keys():
        print '      <item>%s</item>' % (w,)
    print '''    </one-of>
  </rule>
</grammar>
'''

if __name__ == '__main__':
    main()
    
