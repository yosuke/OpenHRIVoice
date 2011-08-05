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
from StringIO import StringIO
import tempfile
import xdot
from openhrivoice.parsesrgs import *
from openhrivoice.juliustographviz import juliustographviz
from openhrivoice.__init__ import __version__

__title__ = 'OpenHRI W3C-SRGS Editor'

if hasattr(sys, "frozen"):
    basedir = os.path.dirname(unicode(sys.executable, sys.getfilesystemencoding()))
else:
    basedir = os.path.dirname(__file__)

class AboutDialog(gtk.AboutDialog):

    def __init__(self, parent):
        Gtk.AboutDialog.__init__(self)
        self.set_name(__title__ + ' version ' + __version__)
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
        srgs = SRGS(StringIO(xmlstr))
        dotcode = juliustographviz(srgs.toJulius().split('\n'))
        self._parent_window._xdot.set_dotcode(dotcode)

class MainWindow(gtk.Window):
    def __init__(self, *args, **kwargs):
        # initialize main window
        gtk.Window.__init__(self, *args, **kwargs)
        self._xdot = xdot.DotWindow()
        self._filename = None

        self.add_accel_group(gtk.AccelGroup())
        self.connect('delete_event', self.quit)

        # intialize XML code view
        self._sourcebuf = gtksourceview2.Buffer(language=gtksourceview2.language_manager_get_default().get_language('xml'))
        self._sourceview = gtksourceview2.View(self._sourcebuf)
        self._sourceview.connect('key-press-event', self.keypressevent)
        self._sourceview.connect('key-release-event', self.keyreleaseevent)
        self._sourceview.set_show_line_numbers(True)
        self._sourceview.set_show_line_marks(True)
        self._sourceview.set_auto_indent(True)
        self._sourceview.set_indent_on_tab(True)
        self._sourceview.set_insert_spaces_instead_of_tabs(True)
        self._sourceview.set_tab_width(2)
        
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

        self._validationthread = ValidationThread()
        self._validationthread.set_parent_window(self)
        self._validationthread.start()

        self.update_title()

    def update_title(self):
        titlestr = 'OpenHRI W3C-SRGS Editor - '
        if self._sourcebuf.get_modified() == True:
            titlestr += '*'
        if self._filename is None:
            titlestr += '[new]'
        else:
            titlestr += self._filename
        self.props.title = titlestr

    def quit(self, widget, event):
        print "quiting"
        self._validationthread.exit()
        gtk.main_quit()

    def keypressevent (self, widget, event):
        if event.state & gtk.gdk.CONTROL_MASK:
            if event.keyval == gtk.keysyms.o:
                self.open_file()
                return True
            elif event.keyval == gtk.keysyms.s:
                self.save_file()
                return True
            elif event.keyval == gtk.keysyms.w:
                self.save_file_as()
                return True
            elif event.keyval == gtk.keysyms.f:
                self.format_data()
                return True
        return False

    def keyreleaseevent (self, widget, event):
        if self._sourcebuf.get_modified():
            self._data = self._sourcebuf.props.text
            self.validate()
        self.update_title()
        return False

    def set_data(self, data, undoable = True):
        if self._sourcebuf.props.text != data:
            if undoable == False:
                self._sourcebuf.begin_not_undoable_action()
            self._sourcebuf.props.text = data
            self._data = data
            if undoable == False:
                self._sourcebuf.end_not_undoable_action()
                self._sourcebuf.set_modified(False)
            self.validate()
        self.update_title()

    def validate(self):
        self._validationthread.set_data(self._data)

    def set_info(self, infostr):
        self._infolabel.set_text(infostr)

    def format_data(self):
        doc = None
        try:
            parser = etree.XMLParser(recover = True)
            doc = etree.parse(StringIO(self._sourcebuf.props.text), parser)
        except:
            pass
        if doc is not None:
            self.set_data(etree.tounicode(doc, pretty_print = True))

    def open_file(self):
        chooser = gtk.FileChooserDialog(
            __title__, self, gtk.FILE_CHOOSER_ACTION_OPEN,
            buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                     gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        chooser.set_default_response(gtk.RESPONSE_OK)
        res = chooser.run()
        if res == gtk.RESPONSE_OK:
            self._filename = chooser.get_filename()
            try:
                self.set_data(open(self._filename, 'r').read(), False)
                self.update_title()
            except:
                self.set_info('Unable to open ' + self._filename)
                self._filename = None
        chooser.destroy()
        
    def save_file(self):
        if self._filename is not None:
            f = open (self._filename, 'w')
            f.write(self._sourcebuf.props.text)
            f.close()
            self._sourcebuf.set_modified(False)
            self.update_title()
        else:
            self.save_file_as()
            
    def save_file_as (self):
        chooser = gtk.FileChooserDialog(
            __title__, self, gtk.FILE_CHOOSER_ACTION_SAVE,
            buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                     gtk.STOCK_SAVE, gtk.RESPONSE_OK))
        chooser.set_default_response(gtk.RESPONSE_OK)
        if self._filename is not None:
            chooser.set_filename(self._filename)
        res = chooser.run()
        if res == gtk.RESPONSE_OK:
            self._filename = chooser.get_filename()
            self.save_file()
        chooser.destroy()


initialdata = '''<?xml version="1.0" encoding="UTF-8" ?>
<grammar xmlns="http://www.w3.org/2001/06/grammar"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://www.w3.org/2001/06/grammar
                             http://www.w3.org/TR/speech-grammar/grammar.xsd"
         xml:lang="en"
         version="1.0" mode="voice" root="command">
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
        win._filename = sys.argv[1]
    else:
        win.set_data(initialdata, False)
    gtk.main()

if __name__ == '__main__':
    main()
