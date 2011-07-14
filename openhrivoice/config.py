#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''configuration manager for OpenHRIVoice

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
import socket
import platform
import time
import struct
import traceback
import locale
import codecs
import tempfile
import optparse
from glob import glob
from openhrivoice.__init__ import __version__
from openhrivoice import utils

class config():
    def __init__(self):
        self._platform = platform.system()
        if hasattr(sys, "frozen"):
            self._basedir = os.path.dirname(unicode(sys.executable, sys.getfilesystemencoding()))
        else:
            self._basedir = os.path.dirname(__file__)
        self._homedir = os.path.expanduser('~')
        self._configdir = os.path.join(self._homedir, '.openhri')
        if os.path.exists(self._configdir) == False:
            os.makedirs(self._configdir)

        self._lexicondb = os.path.join(self._configdir, 'lexcon.db')

        if self._platform == "Windows":
            self._julius_runkitdir = os.path.join(self._basedir, "3rdparty", "dictation-kit-v4.0-win")
            self._julius_voxforgedir = os.path.join(self._basedir, "3rdparty", "julius-voxforge-build726")
            self._julius_bin = os.path.join(self._julius_runkitdir, "bin", "julius.exe")
            self._julius_hmm_en = os.path.join(self._julius_voxforgedir, "hmmdefs")
            self._julius_hlist_en = os.path.join(self._julius_voxforgedir, "tiedlist")
            self._julius_dict_en = os.path.join(self._julius_voxforgedir, "dict")
        else:
            self._julius_runkitdir = "/usr/share/julius-runkit"
            self._julius_voxforgedir = "/usr/share/julius-voxforge"
            self._julius_voxforgedir_de = "/usr/share/julius-voxforge-de"
            self._julius_bin = "/usr/bin/julius"
            self._julius_hmm_en = os.path.join(self._julius_voxforgedir, "acoustic", "hmmdefs")
            self._julius_hlist_en = os.path.join(self._julius_voxforgedir, "acoustic", "tiedlist")
            self._julius_dict_en = "/usr/share/doc/julius-voxforge/dict.gz"
            self._julius_hmm_de = os.path.join(self._julius_voxforgedir_de, "acoustic", "hmmdefs")
            self._julius_hlist_de = os.path.join(self._julius_voxforgedir_de, "acoustic", "tiedlist")
        self._julius_hmm_ja = os.path.join(self._julius_runkitdir, "model", "phone_m", "hmmdefs_ptm_gid.binhmm")
        self._julius_hlist_ja = os.path.join(self._julius_runkitdir, "model", "phone_m", "logicalTri")
        self._julius_ngram_ja = os.path.join(self._julius_runkitdir, "model", "lang_m", "web.60k.8-8.bingramv4.gz")
        self._julius_dict_ja = os.path.join(self._julius_runkitdir, "model", "lang_m", "web.60k.htkdic")

        if self._platform == "Windows":
            self._openjtalk_bin = os.path.join(self._basedir, "open_jtalk.exe")
            self._openjtalk_phonemodel_male_ja =  os.path.join(self._basedir, "3rdparty", "hts_voice_nitech_jp_atr503_m001-1.01")
            self._openjtalk_phonemodel_female_ja =  os.path.join(self._basedir, "3rdparty", "MMDAgent-Example/Voice/mei_normal")
            self._openjtalk_dicfile_ja = os.path.join(self._basedir, "3rdparty", "open_jtalk_dic_utf_8-1.00")
        else:
            self._openjtalk_bin = "open_jtalk"
            self._openjtalk_phonemodel_male_ja = "/usr/lib/hts-voice/nitech-jp-atr503-m001"
            self._openjtalk_phonemodel_female_ja = "/usr/lib/mmdagent/voice/mei_normal"
            self._openjtalk_dicfile_ja = "/usr/lib/open_jtalk/dic/utf-8"

        if self._platform == "Windows":
            self._festivaldir = os.path.join(self._basedir, "3rdparty", "festival-1.96.03-win", "festival")
            self._festival_bin = os.path.join(self._festivaldir, "festival.exe")
            self._festival_opt = ["--libdir", os.path.join(self._festivaldir, "lib")]
        else:
            self._festival_bin = "festival"
            self._festival_opt = []
