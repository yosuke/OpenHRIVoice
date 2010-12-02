#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Hiragana to phoneme converter

Copyright (C) 2010
    Yosuke Matsusaka
    Intelligent Systems Research Institute,
    National Institute of Advanced Industrial Science and Technology (AIST),
    Japan
    All rights reserved.
Licensed under the Eclipse Public License -v 1.0 (EPL)
http://www.opensource.org/licenses/eclipse-1.0.txt
'''

# Mappings between hiragana to phoneme are referred from yomi2voca code written
# by Julius development team:
# http://sourceforge.jp/cvs/view/julius/julius4/gramtools/yomi2voca/

import re

class hiragana2phoneme:
    def __init__(self):
        self._dict1 = {
            u'でぃ': ' d i',
            u'てぃ': ' t i',
            u'すぃ': ' s i',
            u'ずぃ': ' z i',
            u'きゃ': ' ky a',
            u'きゅ': ' ky u',
            u'きょ': ' ky o',
            u'しゃ': ' sh a',
            u'しゅ': ' sh u',
            u'しぇ': ' sh e',
            u'しょ': ' sh o',
            u'ちゃ': ' ch a',
            u'ちゅ': ' ch u',
            u'ちぇ': ' ch e',
            u'ちょ': ' ch o',
            u'にゃ': ' ny a',
            u'にゅ': ' ny u',
            u'にょ': ' ny o',
            u'ひゃ': ' hy a',
            u'ひゅ': ' hy u',
            u'ひょ': ' hy o',
            u'みゃ': ' my a',
            u'みゅ': ' my u',
            u'みょ': ' my o',
            u'りゃ': ' ry a',
            u'りゅ': ' ry u',
            u'りょ': ' ry o',
            u'ぎゃ': ' gy a',
            u'ぎゅ': ' gy u',
            u'ぎょ': ' gy o',
            u'じゃ': ' j a',
            u'ぢゃ': ' j a',
            u'じゅ': ' j u',
            u'じぇ': ' j e',
            u'じょ': ' j o',
            u'びゃ': ' by a',
            u'びゅ': ' by u',
            u'びょ': ' by o',
            u'ぴゃ': ' py a',
            u'ぴゅ': ' py u',
            u'ぴょ': ' py o',
            u'うぃ': ' w i',
            u'うぇ': ' w e',
            u'うぉ': ' w o',
            u'ふぁ': ' f a',
            u'ふぃ': ' f i',
            u'ふぇ': ' f e',
            u'ふぉ': ' f o'
        }
        self._dict2 = {
            u'あ': ' a',
            u'い': ' i',
            u'う': ' u',
            u'え': ' e',
            u'お': ' o',
            u'か': ' k a',
            u'き': ' k i',
            u'く': ' k u',
            u'け': ' k e',
            u'こ': ' k o',
            u'さ': ' s a',
            u'し': ' sh i',
            u'す': ' s u',
            u'せ': ' s e',
            u'そ': ' s o',
            u'た': ' t a',
            u'ち': ' ch i',
            u'つ': ' ts u',
            u'て': ' t e',
            u'と': ' t o',
            u'な': ' n a',
            u'に': ' n i',
            u'ぬ': ' n u',
            u'ね': ' n e',
            u'の': ' n o',
            u'は': ' h a',
            u'ひ': ' h i',
            u'ふ': ' f u',
            u'へ': ' h e',
            u'ほ': ' h o',
            u'ま': ' m a',
            u'み': ' m i',
            u'む': ' m u',
            u'め': ' m e',
            u'も': ' m o',
            u'ら': ' r a',
            u'り': ' r i',
            u'る': ' r u',
            u'れ': ' r e',
            u'ろ': ' r o',
            u'が': ' g a',
            u'ぎ': ' g i',
            u'ぐ': ' g u',
            u'げ': ' g e',
            u'ご': ' g o',
            u'ざ': ' z a',
            u'じ': ' j i',
            u'ず': ' z u',
            u'ぜ': ' z e',
            u'ぞ': ' z o',
            u'だ': ' d a',
            u'ぢ': ' j i',
            u'づ': ' z u',
            u'で': ' d e',
            u'ど': ' d o',
            u'ば': ' b a',
            u'び': ' b i',
            u'ぶ': ' b u',
            u'べ': ' b e',
            u'ぼ': ' b o',
            u'ぱ': ' p a',
            u'ぴ': ' p i',
            u'ぷ': ' p u',
            u'ぺ': ' p e',
            u'ぽ': ' p o',
            u'や': ' y a',
            u'ゆ': ' y u',
            u'よ': ' y o',
            u'わ': ' w a',
            u'ん': ' N',
            u'っ': ' q',
            u'ー': ':',
            u'を': ' o',
            u'、': ' sp'
        }
        self._regex1 = re.compile(u"(%s)" % u"|".join(map(re.escape, self._dict1.keys())))
        self._regex2 = re.compile(u"(%s)" % u"|".join(map(re.escape, self._dict2.keys())))

    def convert(self, text):
        ret = text
        ret = self._regex1.sub(lambda m: self._dict1[m.string[m.start():m.end()]], ret) 
        ret = self._regex2.sub(lambda m: self._dict2[m.string[m.start():m.end()]], ret) 
        # clear all non alphabets
        ret = re.sub(r'[^a-zA-Z :]', r'', ret)
        return ret.strip(" ")

def main():
    import sys, codecs
    sys.stdin = codecs.getreader('utf-8')(sys.stdin)
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
    h = hiragana2phoneme()
    if len(sys.argv) == 2:
        f = open(sys.argv[1])
        for l in f:
            for w in l.decode("utf-8").strip("\n").split(" "):
                if w == "<s>":
                    print "<s>\t[]\tsilB"
                elif w == "</s>":
                    print "</s>\t[]\tsilE"
                else:
                    print "%s\t[%s]\t%s" % (w, w, h.convert(w))
    else:
        print h.convert(u'おんそえのへんかんのてすとでーす')

if __name__ == '__main__':
    main()
