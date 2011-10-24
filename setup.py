#!/usr/bin/env python

from setuptools import setup, find_packages
from setuptools.command.build_ext import build_ext
import sys, os
from glob import glob
import matplotlib
from openhrivoice.__init__ import __version__

cmd_classes = {}
try:
    from DistUtilsExtra.command import *
    cmd_classes.update({"build": build_extra.build_extra,
                        "build_i18n" :  build_i18n.build_i18n})
except ImportError:
    pass

try:
    import py2exe
    sys.path.append("openhrivoice")
except ImportError:
    pass

data_files = []

if sys.platform == "win32":
    # py2exe options
    data_files = matplotlib.get_py2exe_datafiles()
    extra = {
        "console": [
                    "openhrivoice/JuliusRTC.py",
                    "openhrivoice/srgstopls.py",
                    "openhrivoice/srgstojulius.py",
                    "openhrivoice/validatesrgs.py",
                    "openhrivoice/bundlexinclude.py",
                    "openhrivoice/plstosinglewordgrammar.py",
                    "openhrivoice/OpenJTalkRTC.py",
                    "openhrivoice/FestivalRTC.py",
                    "openhrivoice/CombineResultsRTC.py",
                    "openhrivoice/XSLTRTC.py",
                    "openhrivoice/WavePlayerRTC.py",
                    "openhrivoice/SpecgramRTC.py",
                    "openhrivoice/srgseditor.py",
                    ],
        "options": {
            "py2exe": {
                "includes": ["xml.etree.ElementTree", "lxml._elementpath", "OpenRTM_aist", "RTC",
                             "matplotlib.backends",  "matplotlib.backends.backend_tkagg",
                             "matplotlib.figure","pylab", "numpy", "matplotlib.numerix.fft", "cairo", "pango", "pangocairo",
                             "atk", "gobject", "gio", "glib", "gtk", "gtksourceview2"],
                "excludes": ["_gtkagg", "_wxagg"],
                "dll_excludes": ["ierutil.dll", "powrprof.dll", "msimg32.dll", "mpr.dll", "urlmon.dll", "dnsapi.dll"],
            }
        }
    }
else:
    extra = {}

setup(name='openhrivoice',
      cmdclass=cmd_classes,
      version=__version__,
      description="Voice components for OpenRTM (part of OpenHRI softwares)",
      long_description="""Voice components for OpenRTM (part of OpenHRI softwares).""",
      classifiers=[],
      keywords='',
      author='Yosuke Matsusaka',
      author_email='yosuke.matsusaka@aist.go.jp',
      url='http://openhri.net/',
      license='EPL',
      packages=find_packages(exclude=['ez_setup', 'doc', 'examples', 'tests']),
      include_package_data=True,
      package_data={'openhrivoice': ['*.dfa', '*.dict', '*.xsd']},
      data_files=data_files,
      zip_safe=False,
      install_requires=[
        # -*- Extra requirements: -*-
        ],
      entry_points="""
      [console_scripts]
      openjtalkrtc = openhrivoice.OpenJTalkRTC:main
      juliusrtc = openhrivoice.JuliusRTC:main
      srgstopls = openhrivoice.srgstopls:main
      srgstojulius = openhrivoice.srgstojulius:main
      validatesrgs = openhrivoice.validatesrgs:main
      bundlexinclude = openhrivoice.bundlexinclude:main
      plstosinglewordgrammar = openhrivoice.plstosinglewordgrammar:main
      juliustographviz = openhrivoice.juliustographviz:main
      maryrtc = openhrivoice.MARYRTC:main
      festivalrtc = openhrivoice.FestivalRTC:main
      combineresultsrtc = openhrivoice.CombineResultsRTC:main
      xsltrtc = openhrivoice.XSLTRTC:main
      waveplayerrtc = openhrivoice.WavePlayerRTC:main
      specgramrtc = openhrivoice.SpecgramRTC:main
      openhrivoicemanager = openhrivoice.OpenHRIVoiceManager:main
      srgseditor = openhrivoice.srgseditor:main
      """,
      **extra
      )
