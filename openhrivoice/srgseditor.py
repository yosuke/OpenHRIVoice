#! /usr/bin/python
# -*- coding: utf-8 -*-

'''Visual Editing Environment for W3C-SRGS

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
import threading
from lxml import etree
import pango
import gtk
import gtksourceview2
from pprint import pprint
import tempfile
import xdot
from openhrivoice.parsesrgs import *
from openhrivoice.juliustographviz import juliustographviz
from openhrivoice.__init__ import __version__

if hasattr(sys, "frozen"):
    basedir = os.path.dirname(unicode(sys.executable, sys.getfilesystemencoding()))
else:
    basedir = os.path.dirname(__file__)

class AboutDialog(gtk.AboutDialog):

    def __init__(self, parent):
        Gtk.AboutDialog.__init__(self)
        self.set_name('OpenHRI W3C-SRGS Editor version ' + __version__)
        self.set_copyright('Copyright (c) 2011 Yosuke Matsusaka')
        self.set_website_label('http://openhri.net/')
        self.set_authors(['Yosuke Matsusaka',])
        self.set_transient_for(parent)
        self.connect("response", lambda d, r: d.destroy())

class ValidationThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self._loop = True
        self._parent_window = None
        self._updated = False
        self._data = ''

    def run(self):
        # load xml schema definition for validating SRGS format
        #schemafile = os.path.join(basedir, 'grammar.xsd')
        #self._parent_window.set_info("reading schema definition: " + schemafile)
        #xmlschema_doc = etree.parse(schemafile)
        #self._xmlschema = etree.XMLSchema(xmlschema_doc)
        #self._parent_window.set_info("end reading schema")
        while self._loop == True:
            time.sleep(0.1)
            if self._updated == True:
                text = self._data
                self._updated = False
                if self.validatesrgs(text) == True:
                    self.drawdot(text)

    def exit(self):
        self._loop = False

    def set_parent_window(self, win):
        self._parent_window = win

    def set_data(self, text):
        if self._data != text:
            self._updated = True
            self._data = text

    def validatesrgs(self, xmlstr):
        self._parent_window.set_info("validating")
        try:
            doc = etree.fromstring(xmlstr)
            if hasattr(doc, "xinclude"):
                doc.xinclude()
            #self._xmlschema.assert_(doc)
            self._parent_window.set_info("valid")
        except etree.XMLSyntaxError, e:
            self._parent_window.set_info("[error] " + str(e))
            return False
        except AssertionError, e:
            self._parent_window.set_info("[error] " + str(e))
            return False
        return True

    def drawdot(self, xmlstr):
        fn = tempfile.mkstemp()
        f = os.fdopen(fn[0], 'w')
        f.write(xmlstr)
        f.close()
        srgs = SRGS(fn[1])
        dotcode = juliustographviz(srgs.toJulius().split('\n'))
        os.remove(fn[1])
        self._parent_window._xdot.set_dotcode(dotcode)

class MainWindow(gtk.Window):
    def __init__(self, *args, **kwargs):
        # initialize main window
        gtk.Window.__init__(self, *args, **kwargs)
        self._xdot = xdot.DotWindow()
        self.add_accel_group(gtk.AccelGroup())
        self.connect('delete_event', self.quit)

        # intialize XML code view
        self._sourcebuf = gtksourceview2.Buffer(language=gtksourceview2.language_manager_get_default().get_language('xml'))
        self._sourceview = gtksourceview2.View(self._sourcebuf)
        self._sourceview.connect('key-release-event', self.keypressevent)
        self._sourceview.set_show_line_numbers(True)
        self._sourceview.set_show_line_marks(True)
        self._sourceview.set_auto_indent(True)
        self._sourceview.set_indent_on_tab(True)
        self._sourceview.set_insert_spaces_instead_of_tabs(True)
        
        self._sw = gtk.ScrolledWindow()
        self._sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self._sw.add(self._sourceview)

        # initialize information view
        self._infolabel = gtk.Label()

        # layout main window
        self._vbox = gtk.VBox()
        self._vbox.pack_start(self._sw)
        self._vbox.pack_start(self._infolabel, False, False)
        self.add(self._vbox)
        self.set_size_request(400, 400)
        self.resize(600, 520)
        self.props.title = 'OpenHRI W3C-SRGS Editor'

        self._validationthread = ValidationThread()
        self._validationthread.set_parent_window(self)
        self._validationthread.start()

    def quit(self, widget, event):
        print "quiting"
        self._validationthread.exit()
        gtk.main_quit()

    def keypressevent (self, widget, event):
        self.set_data(self._sourcebuf.props.text)
        return False

    def set_data(self, data, undoable = True):
        if undoable == False:
            self._sourcebuf.begin_not_undoable_action()
        if self._sourcebuf.props.text != data:
            self._sourcebuf.props.text = data
        if undoable == False:
            self._sourcebuf.end_not_undoable_action()
        self._validationthread.set_data(data)

    def set_info(self, infostr):
        self._infolabel.set_text(infostr)

initialdata = '''<?xml version="1.0" encoding="UTF-8" ?>
<grammar xmlns="http://www.w3.org/2001/06/grammar"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://www.w3.org/2001/06/grammar
                             http://www.w3.org/TR/speech-grammar/grammar.xsd"
         xml:lang="en"
         version="1.0" mode="voice" root="command">
 <rule id="command">
  <one-of>
   <item><ruleref uri="#greeting"/></item>
   <item><ruleref uri="#control"/></item>
  </one-of>
 </rule>
 <rule id="command">
  <one-of>
   <item>hi</item>
   <item>bye</item>
  </one-of>
 </rule>
</grammar>
'''

def main():
    gtk.gdk.threads_init()
    win = MainWindow()
    win.show_all()
    if len(sys.argv) >= 2:
        win.set_data(open(sys.argv[1], 'r').read(), False)
    else:
        win.set_data(initialdata, False)
    gtk.main()

if __name__ == '__main__':
    main()
