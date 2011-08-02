#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Utility script to generate graphviz dot file from Julius grammar

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
import locale
from openhrivoice import utils
try:
    import gettext
    _ = gettext.translation(domain='openhrivoice', localedir=os.path.dirname(__file__)+'/../share/locale').ugettext
except:
    _ = lambda s: s

__doc__ = _('Draw graph from Julius grammar.')

__examples__ = '''
Examples:

- '''+_('Draw graph of the SRGS grammar.')+'''

  ::
  
  $ srgstojulius sample.grxml | juliustographviz | dot -Txlib
'''

def juliustographviz(lines):
    ret = ''
    fdfa = True
    fsa = list()
    dic = {}
    for line in lines:
        line = line.rstrip('\n')
        if line == "DFAEND":
            fdfa = False
            continue
        elif line == "DICEND":
            break
        if fdfa:
            v = line.split(' ')
            fsa.append((int(v[2]), int(v[1]), int(v[0])))
        else:
            v = line.split('\t')
            dic[int(v[0])] = v[1].strip('[]')
    ret += u"digraph finite_state_machine {\n"
    ret += u"  rankdir=LR;\n"
    for v in fsa:
        if v[0] < 0:
            break
        ret += u'  S%i -> S%i [label = "%s"];\n' % (v[0], v[2], dic[v[1]])
    ret += u"}\n"
    return ret

def main():
    encoding = locale.getpreferredencoding()
    sys.stdin = codecs.getreader(encoding)(sys.stdin, errors = "replace")
    sys.stdout = codecs.getwriter(encoding)(sys.stdout, errors = "replace")
    sys.stderr = codecs.getwriter(encoding)(sys.stderr, errors = "replace")

    parser = utils.MyParser(version=__version__, usage="%prog < [julius grammar]",
                            description=__doc__, epilog=__examples__)
    parser.add_option('-v', '--verbose', dest='verbose', action='store_true',
                      default=False,
                      help=_('output verbose information'))
    try:
        opts, args = parser.parse_args()
    except optparse.OptionError, e:
        print >>sys.stderr, 'OptionError:', e
        sys.exit(1)

    print juliustographviz(sys.stdin)

if __name__ == '__main__':
    main()
