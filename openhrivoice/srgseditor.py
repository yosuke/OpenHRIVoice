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
import locale
from lxml import etree
from lxml.html import soupparser
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
from openhrivoice.config import config

__title__ = 'OpenHRI W3C-SRGS Editor'

if hasattr(sys, "frozen"):
    basedir = os.path.dirname(unicode(sys.executable, sys.getfilesystemencoding()))
else:
    basedir = os.path.dirname(__file__)

class MyDotWindow(xdot.DotWindow):

    ui = '''
    <ui>
        <toolbar name="ToolBar">
            <toolitem action="Reload"/>
            <separator/>
            <toolitem action="ZoomIn"/>
            <toolitem action="ZoomOut"/>
            <toolitem action="ZoomFit"/>
            <toolitem action="Zoom100"/>
        </toolbar>
    </ui>
    '''

    def __init__(self):
        gtk.Window.__init__(self)
        self.set_title('Dot Viewer')
        self.set_default_size(512, 512)
        vbox = gtk.VBox()
        self.add(vbox)

        self.graph = xdot.Graph()
        self.widget = xdot.DotWidget()
        self.uimanager = gtk.UIManager()

        accelgroup = self.uimanager.get_accel_group()
        self.add_accel_group(accelgroup)

        actiongroup = gtk.ActionGroup('Actions')
        actiongroup.add_actions((
            ('Reload', gtk.STOCK_REFRESH, None, None, None, self.on_reload),
            ('ZoomIn', gtk.STOCK_ZOOM_IN, None, None, None, self.widget.on_zoom_in),
            ('ZoomOut', gtk.STOCK_ZOOM_OUT, None, None, None, self.widget.on_zoom_out),
            ('ZoomFit', gtk.STOCK_ZOOM_FIT, None, None, None, self.widget.on_zoom_fit),
            ('Zoom100', gtk.STOCK_ZOOM_100, None, None, None, self.widget.on_zoom_100),
        ))
        self.uimanager.insert_action_group(actiongroup, 0)

        self.uimanager.add_ui_from_string(self.ui)
        toolbar = self.uimanager.get_widget('/ToolBar')
        vbox.pack_start(toolbar, False)
        vbox.pack_start(self.widget)
        self.set_focus(self.widget)
        self.show_all()

class AboutDialog(gtk.AboutDialog):

    def __init__(self, parent):
        Gtk.AboutDialog.__init__(self)
        self.set_name(__title__ + ' version ' + __version__)
        self.set_copyright('Copyright (c) 2011 Yosuke Matsusaka')
        self.set_website_label('http://openhri.net/')
        self.set_authors(['Yosuke Matsusaka',])
        self.set_transient_for(parent)
        self.connect("response", lambda d, r: d.destroy())

class MainWindow(gtk.Window):
    ui = '''
    <ui>
        <toolbar name="ToolBar">
            <toolitem action="Open"/>
            <toolitem action="Save"/>
            <toolitem action="SaveAs"/>
            <separator/>
            <toolitem action="Format"/>
        </toolbar>
    </ui>
    '''

    def __init__(self, *args, **kwargs):
        self._config = config()
        # initialize main window
        gtk.Window.__init__(self, *args, **kwargs)
        self._filename = None
        self._data = None

        self._uimanager = gtk.UIManager()

        actiongroup = gtk.ActionGroup('Actions')
        actiongroup.add_actions((
            ('Open', gtk.STOCK_OPEN, None, None, None, self.open_file),
            ('Save', gtk.STOCK_SAVE, None, None, None, self.save_file),
            ('SaveAs', gtk.STOCK_SAVE_AS, None, None, None, self.save_file_as),
            ('Format', gtk.STOCK_INDENT, None, None, None, self.format_data),
        ))
        self._uimanager.insert_action_group(actiongroup, 0)

        self._uimanager.add_ui_from_string(self.ui)
        self._toolbar = self._uimanager.get_widget('/ToolBar')

        accelgroup = self._uimanager.get_accel_group()
        self.add_accel_group(accelgroup)
        self.connect('delete_event', self.quit)
        self.connect('destroy', self.quit)

        self._xdot = MyDotWindow()
        self._xdot.connect('delete_event', self.quit)

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
        self._sourceview.modify_font(pango.FontDescription('Monospace 10'))
        
        self._sw = gtk.ScrolledWindow()
        self._sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self._sw.add(self._sourceview)

        # initialize information view
        self._infolabel = gtk.Label()
        self._infolabel.set_line_wrap(True)

        # layout main window
        self._vbox = gtk.VBox()
        self._vbox.pack_start(self._toolbar, False)
        self._vbox.pack_start(self._sw)
        self._vbox.pack_start(self._infolabel, False, False)
        self.add(self._vbox)
        self.set_size_request(400, 400)
        self.resize(600, 520)

        schemafile = os.path.join(basedir, 'grammar.xsd')
        xmlschema_doc = etree.parse(schemafile)
        self._xmlschema = etree.XMLSchema(xmlschema_doc)

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

    def quit(self, *args):
        print "quiting"
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
        if self._data != self._sourcebuf.props.text:
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

    def validate(self, *args):
        self.set_info("validating")
        try:
            doc = etree.fromstring(self._data)
            if hasattr(doc, "xinclude"):
                doc.xinclude()
            self._xmlschema.assert_(doc)
            self.set_info("valid")
            srgs = SRGS(StringIO(self._data))
            dotcode = juliustographviz(srgs.toJulius().split('\n'))
            self._xdot.set_dotcode(dotcode)
        except etree.XMLSyntaxError, e:
            self.set_info("[error] " + str(e))
        except AssertionError, e:
            self.set_info("[error] " + str(e))
        except KeyError, e:
            self.set_info("[error] " + str(e))

    def set_info(self, infostr):
        self._infolabel.set_text(infostr)
        print infostr

    def format_data(self, *args):
        doc = None
        try:
            parser = etree.XMLParser(recover = True)
            doc = etree.parse(StringIO(self._sourcebuf.props.text), parser)
        except:
            pass
        if doc is not None:
            self.set_data(etree.tounicode(doc, pretty_print = True))

    def format_data2(self):
        doc = soupparser.fromstring(self._sourcebuf.props.text)
        self.set_data(etree.tounicode(doc, pretty_print = True))
        #doc = BeautifulSoup(self._sourcebuf.props.text)
        #self.set_data(doc.prettify())

    def open_file(self, *args):
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
        
    def save_file(self, *args):
        if self._filename is not None:
            try:
                f = open (self._filename, 'w')
                f.write(self._sourcebuf.props.text)
                f.close()
                self._sourcebuf.set_modified(False)
                self.update_title()
            except IOError, e:
                self.set_info(str(e))
                md = gtk.MessageDialog(self, 
                                       gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR,
                                       gtk.BUTTONS_CLOSE, str(e))
                md.run()
                md.destroy()
        else:
            self.save_file_as()
            
    def save_file_as (self, *args):
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
      <item>hello</item>
      <item>bye</item>
    </one-of>
  </rule>
</grammar>
'''

initialdata_ja = '''<?xml version="1.0" encoding="UTF-8" ?>
<grammar xmlns="http://www.w3.org/2001/06/grammar"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://www.w3.org/2001/06/grammar
                             http://www.w3.org/TR/speech-grammar/grammar.xsd"
         xml:lang="ja"
         version="1.0" mode="voice" root="command">
  <rule id="command">
    <one-of>
      <item>こんにちは</item>
      <item>さようなら</item>
    </one-of>
  </rule>
</grammar>
'''

def main():
    gtk.gdk.threads_init()
    gtk.gdk.threads_enter()
    win = MainWindow()
    win.show_all()
    if len(sys.argv) >= 2:
        win.set_data(open(sys.argv[1], 'r').read(), False)
        win._filename = sys.argv[1]
    else:
        if locale.getdefaultlocale()[0] == 'ja_JP':
            win.set_data(initialdata_ja, False)
        else:
            win.set_data(initialdata, False)
    win.update_title()
    gtk.main()

if __name__ == '__main__':
    main()
