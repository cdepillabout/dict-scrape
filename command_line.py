#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

# Copyright (C) 2012  Dennis Gosnell
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import re
import sys
import urllib


from dictscrape import DaijisenDictionary, DaijirinDictionary, \
        NewCenturyDictionary, ProgressiveDictionary

def main(word_kanji, word_kana):
    check_daijirin(word_kanji, word_kana)
    print
    check_daijisen(word_kanji, word_kana)
    print
    check_new_century(word_kanji, word_kana)
    print
    check_progressive(word_kanji, word_kana)

if __name__ == '__main__':

    daijirin_dic = DaijirinDictionary()
    daijisen_dic = DaijisenDictionary()
    new_century_dic = NewCenturyDictionary()
    progressive_dic = ProgressiveDictionary()

    if len(sys.argv) == 3:
        kanji = sys.argv[1].decode("utf8")
        kana = sys.argv[2].decode("utf8")
        for d in [daijirin_dic, daijisen_dic, new_century_dic, progressive_dic]:
            if d:
                print("\t\t\t\t%s\n%s\n\n" % (d.short_name, d.lookup(kanji, kana)))
        sys.exit(1)


    words = [
            (u'強迫', u'きょうはく'),
            (u'面白い', u'おもしろい'),
            (u'赤し', u'あかし'),
            (u'うっとり', u''),
            (u'バリカン', u''),
            (u'コンピエーニュ', u''),
            (u'蜥蜴', u'とかげ'),
            (u'らくだ', u'駱駝'),
            (u'成り済ます', u'なりすます'),
            #(u'行く', u'いく'),
            (u'が', u''),
            (u'遊ぶ', u'あそぶ'),
            #(u'遊ぶ', u'あすぶ'),        # this fails in the daijirin
            #(u'唸る', u'うなる'),         # this doesn't parse right in the progressive dict
            ]

    """
    for one, two in words:
        main(one, two)
        print
        """

    """
    one = words[0]
    result = NewCenturyDictionary().lookup(one[0], one[1])
    print(result)
    """


    one = words[0]
    for d in [daijirin_dic, daijisen_dic, new_century_dic, progressive_dic]:
        print(d.lookup(one[0], one[1]))
        print

    """
    for word in words:
        for d in [daijirin_dic, daijisen_dic, new_century_dic, progressive_dic]:
            print(d.lookup(word[0], word[1]).to_jsonable())
            print
        print
        """

    """
    daijirin_dic = DaijirinDictionary()
    daijisen_dic = DaijisenDictionary()
    new_century_dic = NewCenturyDictionary()
    progressive_dic = ProgressiveDictionary()
    """

    """
    def print_all_defs(defs):
        for i in range(len(defs)):
            d = ""
            if defs[i].definition:
                definition = defs[i].definition
            else:
                definition = "NO DEFINITION AVAILABLE"
            print("(%2d) %s" % (i, definition))
            for e in defs[i].example_sentences:
                print("    - %s" % e.jap_sentence)
                if e.eng_trans:
                    print("      %s" % e.eng_trans)


    for word in words:
        for d in [daijirin_dic, daijisen_dic, new_century_dic, progressive_dic]:
            print ("FROM %s" % d.dic_name)
            result = d.lookup(word[0], word[1])
            if not result:
                print("NO RESULT FOUND!!!!!")
                print
                continue

            print ("%s (%s) %s:" % (result.kanji, result.kana, result.accent))
            print_all_defs(result.defs)
            print
            """

