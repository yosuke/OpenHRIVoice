#!/usr/bin/env python

from setuptools import setup, find_packages
import sys, os

version = '1.04'

try:
    import py2exe
    sys.path.append("openhrivoice")
except ImportError:
    pass


if sys.platform == "win32":
    # py2exe options
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
                    "openhrivoice/XSLTRTC.py",
                    "openhrivoice/CombineResultsRTC.py"
                    ],
        "options": {
            "py2exe": {
                "includes": "xml.etree.ElementTree, lxml._elementpath, OpenRTM_aist, RTC",
                "dll_excludes": ["ierutil.dll", "powrprof.dll", "msimg32.dll", "mpr.dll", "urlmon.dll", "dnsapi.dll"],
            }
        }
    }
else:
    extra = {}

setup(name='openhrivoice',
    version=version,
    description="Voice components for OpenRTM (part of OpenHRI softwares)",
    long_description="""Voice components for OpenRTM (part of OpenHRI softwares).""",
    classifiers=[],
    keywords='',
    author='Yosuke Matsusaka',
    author_email='yosuke.matsusaka@aist.go.jp',
    url='http://openhri.net/',
    license='EPL',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    package_data={'openhrivoice': ['*.dfa', '*.dict', '*.xsd']},
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
    """,
    **extra
    )
