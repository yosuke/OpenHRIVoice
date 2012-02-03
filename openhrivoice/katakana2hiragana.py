#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Katakana to hiragana converter

Copyright (C) 2010
    Yosuke Matsusaka
    Intelligent Systems Research Institute,
    National Institute of Advanced Industrial Science and Technology (AIST),
    Japan
    All rights reserved.
Licensed under the Eclipse Public License -v 1.0 (EPL)
http://www.opensource.org/licenses/eclipse-1.0.txt
'''

import re

class katakana2hiragana:
    def __init__(self):
        self._dict = {
            u'ア':u'あ',
            u'イ':u'い',
            u'ウ':u'う',
            u'エ':u'え',
            u'オ':u'お',
            u'カ':u'か',
            u'キ':u'き',
            u'ク':u'く',
            u'ケ':u'け',
            u'コ':u'こ',
            u'サ':u'さ',
            u'シ':u'し',
            u'ス':u'す',
            u'セ':u'せ',
            u'ソ':u'そ',
            u'タ':u'た',
            u'チ':u'ち',
            u'ツ':u'つ',
            u'テ':u'て',
            u'ト':u'と',
            u'ナ':u'な',
            u'ニ':u'に',
            u'ヌ':u'ぬ',
            u'ネ':u'ね',
            u'ノ':u'の',
            u'ハ':u'は',
            u'ヒ':u'ひ',
            u'フ':u'ふ',
            u'ヘ':u'へ',
            u'ホ':u'ほ',
            u'マ':u'ま',
            u'ミ':u'み',
            u'ム':u'む',
            u'メ':u'め',
            u'モ':u'も',
            u'ヤ':u'や',
            u'ユ':u'ゆ',
            u'ヨ':u'よ',
            u'ラ':u'ら',
            u'リ':u'り',
            u'ル':u'る',
            u'レ':u'れ',
            u'ロ':u'ろ',
            u'ワ':u'わ',
            u'ヲ':u'を',
            u'ン':u'ん',
            u'ガ':u'が',
            u'ギ':u'ぎ',
            u'グ':u'ぐ',
            u'ゲ':u'げ',
            u'ゴ':u'ご',
            u'ザ':u'ざ',
            u'ジ':u'じ',
            u'ズ':u'ず',
            u'ゼ':u'ぜ',
            u'ゾ':u'ぞ',
            u'ダ':u'だ',
            u'ヂ':u'ぢ',
            u'ヅ':u'づ',
            u'デ':u'で',
            u'ド':u'ど',
            u'バ':u'ば',
            u'ビ':u'び',
            u'ブ':u'ぶ',
            u'ベ':u'べ',
            u'ボ':u'ぼ',
            u'パ':u'ぱ',
            u'ピ':u'ぴ',
            u'プ':u'ぷ',
            u'ペ':u'ぺ',
            u'ポ':u'ぽ',
            u'ァ':u'ぁ',
            u'ィ':u'ぃ',
            u'ゥ':u'ぅ',
            u'ェ':u'ぇ',
            u'ォ':u'ぉ',
            u'ッ':u'っ',
            u'ャ':u'ゃ',
            u'ュ':u'ゅ',
            u'ョ':u'ょ'
            }
        self._regex = re.compile("|".join(map(re.escape, self._dict.keys())))

    def convert(self, text):
        return self._regex.sub(lambda m: self._dict[m.string[m.start():m.end()]], text) 

def main():
    import sys, codecs
    sys.stdin = codecs.getreader('utf-8')(sys.stdin)
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
    h = katakana2hiragana()
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
        print h.convert(u'ヒラガナの変換のテストでーす')

if __name__ == '__main__':
    main()
