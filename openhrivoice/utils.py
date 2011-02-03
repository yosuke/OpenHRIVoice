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

def askopenfilename(title=''):
    if platform.system() == 'Windows':
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
    if platform.system() == 'Windows':
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
            sel = root.tk.splitlist(sel)
        return sel
    return None

def addmanageropts(parser):
    parser.add_option('-a', '--manager-service', dest='managerservice', action='store_true',
                      default=False,
                      help='enable manager to be controlled as corba servant')
    parser.add_option('-f', '--config-file', dest='configfile', action='store',
                      default=None,
                      help='specify custom configuration file')
    parser.add_option('-o', '--option', dest='option', action='append',
                      default=None,
                      help='specify custom configuration parameter')
    parser.add_option('-p', '--port', dest='port', action='store',
                      default=None,
                      help='specify custom corba endpoint')
    parser.add_option('-d', '--master-mode', dest='mastermode', action='store_true',
                      default=False,
                      help='configure manager to be master')

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

