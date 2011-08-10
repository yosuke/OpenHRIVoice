#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Manager for OpenHRIVoice components

Copyright (C) 2011
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
import time
import traceback
import platform
import codecs
import locale
import optparse
import OpenRTM_aist
import RTC
from openhrivoice.__init__ import __version__
from openhrivoice import utils
from openhrivoice.config import config
try:
    import gettext
    _ = gettext.translation(domain='openhrivoice', localedir=os.path.dirname(__file__)+'/../share/locale').ugettext
except:
    _ = lambda s: s

__doc__ = _('Manager for OpenHRIVoice components.')

def main():
    encoding = locale.getpreferredencoding()
    sys.stdout = codecs.getwriter(encoding)(sys.stdout, errors = "replace")
    sys.stderr = codecs.getwriter(encoding)(sys.stderr, errors = "replace")
    
    parser = utils.MyParser(version=__version__, description=__doc__)
    utils.addmanageropts(parser)
    try:
        opts, args = parser.parse_args()
    except optparse.OptionError, e:
        print >>sys.stderr, 'OptionError:', e
        sys.exit(1)
    manager = OpenRTM_aist.Manager.init(utils.genmanagerargs(opts))
    manager.activateManager()
    for c in ('JuliusRTC', 'OpenJTalkRTC', 'FestivalRTC', 'MARYRTC', 'XSLTRTC', 'CombineResultsRTC'):
        print 'loading... %s' % (c,)
        exec('from openhrivoice import %s' % (c,))
        profile=OpenRTM_aist.Properties(defaults_str=eval('%s.%s_spec' % (c, c)))
        manager.registerFactory(profile, eval('%s.%s' % (c, c)), OpenRTM_aist.Delete)
    manager.runManager(False)

if __name__=='__main__':
    main()
