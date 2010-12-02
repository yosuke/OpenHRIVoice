#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Utility script to generate graphviz dot file from Julius grammar

Copyright (C) 2010
    Yosuke Matsusaka
    Intelligent Systems Research Institute,
    National Institute of Advanced Industrial Science and Technology (AIST),
    Japan
    All rights reserved.
Licensed under the Eclipse Public License -v 1.0 (EPL)
http://www.opensource.org/licenses/eclipse-1.0.txt
'''

import sys, codecs

def main():
    sys.stdin = codecs.getreader('utf-8')(sys.stdin)
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
    
    fdfa = True
    fsa = list()
    dic = {}
    for line in sys.stdin:
        line = line.rstrip()
        if line == "DFAEND":
            fdfa = False
            continue
        elif line == "DICEND":
            break
        if fdfa:
            v = line.split(' ')
            fsa.append((int(v[2]), int(v[1]), int(v[0])))
        else:
            v = line.split('\t')
            dic[int(v[0])] = v[1].strip('[]')
    print u"digraph finite_state_machine {"
    print u"  rankdir=LR;"
    for v in fsa:
        if v[0] < 0:
            break
        print u'  S%i -> S%i [label = "%s"];' % (v[0], v[2], dic[v[1]])
    print u"}"

if __name__ == '__main__':
    main()
