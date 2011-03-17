#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Utility functions

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
import platform
import optparse
try:
    import gettext
    _ = gettext.translation(domain='openhrivoice', localedir=os.path.dirname(__file__)+'/../share/locale').ugettext
except:
    _ = lambda s: s

class MyParser(optparse.OptionParser):
    def _add_help_option (self):
        self.add_option("-h", "--help",
                        action="help",
                        help=_("show this help message and exit"))

    def _add_version_option (self):
        self.add_option("--version",
                        action="version",
                        help=_("show program's version number and exit"))

    def format_epilog(self, formatter):
        if self.epilog is not None:
            return self.epilog
        else:
            return ''

    def exit(self, status=0, msg=None):
        if msg is not None:
            sys.stderr.write(msg)
        sys.exit(status)

    def print_usage(self, file=None):
        if file == None :
            file = sys.stdout
        file.write(self.get_usage() + '\n')

    def print_help(self, file=None):
        if file == None :
            file = sys.stdout
        file.write(self.format_help() + '\n')

    def print_version(self, file=None):
        if file == None :
            file = sys.stdout
        file.write(self.get_version() + '\n')

def askopenfilename(title=''):
    #if platform.system() == 'Windows':
    if 0:
        import win32ui
        import win32con 
        openFlags = win32con.OFN_FILEMUSTEXIST|win32con.OFN_EXPLORER
        fspec = "*.*||"
        dlg = win32ui.CreateFileDialog(1, None, None, openFlags, fspec) 
        if dlg.DoModal() == win32con.IDOK: 
            return dlg.GetPathName()
    else:
        import Tkinter
        import tkFileDialog
        rt = Tkinter.Tk()
        rt.withdraw()
        return tkFileDialog.askopenfilename(title=title)
    return None

def askopenfilenames(title=''):
    #if platform.system() == 'Windows':
    if 0:
        import win32ui
        import win32con 
        openFlags = win32con.OFN_FILEMUSTEXIST|win32con.OFN_EXPLORER|win32con.OFN_ALLOWMULTISELECT
        fspec = "all|*.*||"
        dlg = win32ui.CreateFileDialog(1, None, None, openFlags, fspec) 
        if dlg.DoModal() == win32con.IDOK: 
            return dlg.GetPathNames()
    else:
        import Tkinter
        import tkFileDialog
        rt = Tkinter.Tk()
        rt.withdraw()
        sel = tkFileDialog.askopenfilenames(title=title)
        if isinstance(sel, unicode):
            sel = [unicode(s, 'utf-8') for s in rt.tk.splitlist(sel)]
        return sel
    return None

def asksaveasfile():
    if platform.system() == 'Windows':
        import win32ui
        import win32con 
        openFlags = win32con.OFN_OVERWRITEPROMPT|win32con.OFN_EXPLORER
        fspec = "*.*||"
        dlg = win32ui.CreateFileDialog(0, None, None, openFlags, fspec) 
        if dlg.DoModal() == win32con.IDOK: 
            return dlg.GetPathName()
    else:
        import Tkinter
        import tkFileDialog
        rt = Tkinter.Tk()
        rt.withdraw()
        return tkFileDialog.asksaveasfile()
    return None

def addmanageropts(parser):
    parser.add_option('-a', '--manager-service', dest='managerservice', action='store_true',
                      default=False,
                      help=_('enable manager to be controlled as corba servant'))
    parser.add_option('-f', '--config-file', dest='configfile', action='store',
                      default=None,
                      help=_('specify custom configuration file'))
    parser.add_option('-o', '--option', dest='option', action='append',
                      default=None,
                      help=_('specify custom configuration parameter'))
    parser.add_option('-p', '--port', dest='port', action='store',
                      default=None,
                      help=_('specify custom corba endpoint'))
    parser.add_option('-d', '--master-mode', dest='mastermode', action='store_true',
                      default=False,
                      help=_('configure manager to be master'))

def genmanagerargs(opt):
    args = [sys.argv[0],]
    if opt.managerservice == True:
        args.append('-a')
    if opt.configfile is not None:
        args.append('-f')
        args.append(opt.configfile)
    if opt.option is not None:
        for o in opt.option:
            args.append('-o')
            args.append(o)
    if opt.port is not None:
        args.append('-p')
        args.append(port)
    if opt.mastermode == True:
        args.append('-d')

