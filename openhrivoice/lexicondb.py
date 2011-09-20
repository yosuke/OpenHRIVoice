#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Pronouciation dictionary manager

Copyright (C) 2010-2011
    Yosuke Matsusaka
    Intelligent Systems Research Institute,
    National Institute of Advanced Industrial Science and Technology (AIST),
    Japan
    All rights reserved.
Licensed under the Eclipse Public License -v 1.0 (EPL)
http://www.opensource.org/licenses/eclipse-1.0.txt
'''

import sqlite3
from openhrivoice.__init__ import __version__
from openhrivoice.config import config
from openhrivoice.parsejuliusdict import *
from openhrivoice.parsevoxforgedict import *

class LexiconDB:
    ''' Utility class to store pronunciation dictionary to database'''
    
    def __init__(self, fname, version):
        self._config = config()
        self._db = sqlite3.connect(fname)
        createtable = False

        if not self.tableexist('version'):
            # create version table if not
            self.createversiontable(version)
            createtable = True
        elif len(self._db.execute(u"select text from version where text = '%s';" % (version,)).fetchall()) == 0:
            # check version
            self._db.execute(u'drop table version;')
            self.createversiontable(version)
            createtable = True

        if createtable == True:
            if self.tableexist('data'):
                self._db.execute(u'drop table data;')
            self.createdatatable()

            dic = VoxforgeDict(self._config._julius_dict_en)
            for t, vs in dic._dict.iteritems():
                for v in vs:
                    self.register(t.lower(), v, 'ARPAbet')
            del dic

            dic = JuliusDict(self._config._julius_dict_ja)
            for t, vs in dic._dict.iteritems():
                for v in vs:
                    self.register(t, v, 'KANA')
            del dic
            self._db.commit()

    def tableexist(self, name):
        tbls = self._db.execute("select * from sqlite_master where type = 'table' and name = '%s';" % (name,))
        return (len(tbls.fetchall()) != 0)

    def createversiontable(self, version):
        sql = u"""
create table version (
  text varchar(10)
);
"""
        self._db.execute(sql)
        self._db.execute(u'insert into version values (?);', (version,))

    def createdatatable(self):
        sql = u"""
create table data (
  text varchar(10),
  pronounce varchar(200),
  alphabet varchar(10)
);
"""
        self._db.execute(sql)
        self._db.execute('create index text_index on data(text);')
        self._db.execute('create index alphabet_index on data(alphabet);')

    def register(self, text, pronounce, alphabet):
        sql = u'insert into data values (?,?,?);'
        self._db.execute(sql, (text, pronounce, alphabet))

    def lookup(self, text):
        return list(set([p[0] for p in self._db.execute(u"select pronounce from data where text = '%s';" % (text.lower(),)).fetchall()]))

    def substringlookup(self, text):
        p = self.lookup(text)
        if len(p) == 0:
            for i in range(1, len(text)):
                substr = text[:-i]
                reststr = text[len(text)-i:]
                #print substr + "|" + reststr
                pp1 = self.lookup(substr)
                if len(pp1) > 0:
                    #print substr + ':' + ','.join(pp1)
                    pp2 = self.substringlookup(reststr)
                    for p1 in pp1:
                        for p2 in pp2:
                            p.append(p1 + p2)
                    break
        return list(set(p))
        
if __name__ == '__main__':
    import sys
    import locale
    import codecs
    encoding = locale.getpreferredencoding()
    sys.stdout = codecs.getwriter(encoding)(sys.stdout, errors = "replace")
    sys.stderr = codecs.getwriter(encoding)(sys.stderr, errors = "replace")
    db = LexiconDB('test.db', __version__)
    print ','.join(db.lookup('look'))
    print ','.join(db.lookup('pizza'))
    print ','.join(db.lookup(u'見'))
    print ','.join(db.substringlookup(u'隣の客はよく柿食う客だ'))
    
