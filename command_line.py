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

"""
This is a small example program that uses the dictscrape library.
You can pass KANJI and KANA on the command line and this program
will look up that word and print it out.

$ ./command_line.py 強迫 きょうはく
.....
$

Another possibility is to just run this program without any arguments.
It will print out some example searches.

$ ./command_line.py
.....
$
"""

import re
import sys
import urllib


from dictscrape import DaijisenDictionary, DaijirinDictionary, \
        NewCenturyDictionary, ProgressiveDictionary, KenkyuushaDictionary

daijirin_dic = DaijirinDictionary()
daijisen_dic = DaijisenDictionary()
new_century_dic = NewCenturyDictionary()
progressive_dic = ProgressiveDictionary()
kenkyuusha_dic = KenkyuushaDictionary()

def main():
    """
    This shows some uses of the the dictscrape library.
    """
    kenkyuusha_dic.lookup(u'秀逸', u'しゅういつ')
    sys.exit(0)


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

    print("\t\t\tLOOK UP ONE WORD IN ONE DICTIONARY:")
    print("\t\t\t-----------------------------------")
    kanji = words[0][0]
    kana = words[0][1]
    result = new_century_dic.lookup(kanji, kana)
    print(result)

    print("\n\t\t\tLOOK UP ONE WORD IN ALL DICTIONARIES:")
    print("\t\t\t-------------------------------------")
    kanji = words[3][0]
    kana = words[3][1]
    for d in [daijirin_dic, daijisen_dic, new_century_dic, progressive_dic]:
        print(d.lookup(kanji, kana))
        print

    print("\n\t\t\tLOOK UP ACCENT FOR ALL WORDS:")
    print("\t\t\t-----------------------------")
    for kanji, kana in words:
        result = daijirin_dic.lookup(kanji, kana)
        accent = "NO ACCENT AVAILABLE"
        if len(result.accent):
            accent = result.accent
        print("%s (%s): %s" % (kanji, kana, accent))


if __name__ == '__main__':
    # If the user passes kanji and kana on the command line, then we
    # look up that word and print the results.
    if len(sys.argv) == 3:
        kanji = sys.argv[1].decode("utf8")
        kana = sys.argv[2].decode("utf8")
        for d in [daijirin_dic, daijisen_dic, new_century_dic, progressive_dic]:
            if d:
                print("\t\t\t\t%s\n%s\n\n" % (d.short_name, d.lookup(kanji, kana)))
        sys.exit(1)

    main()


