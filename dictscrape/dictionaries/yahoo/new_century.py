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

from lxml import etree

from ..dictionary import Dictionary
from .yahoo import YahooDictionary

from ...example_sentence import ExampleSentence
from ...definition import Definition

class NewCenturyDictionary(YahooDictionary):
    """
    New Century Dictionary from Yahoo.
    """

    long_dictionary_name = u"Yahoo's New Century Dictionary (ニューセンチュリー和英辞典)"
    short_dictionary_name = "New_Century"
    dictionary_type = Dictionary.YAHOO_NEW_CENTURY_TYPE
    dtype_search_param = '3'
    dname_search_param = '2ss'

    def __init__(self):
        pass

    def remove_parenthesis(self, string):
        # Remove parenthesis.  This is a little difficult because
        # we have to loop through the list multiple times until we
        # are certain there are no more parenthesis.  Just to be
        # on the safe side, we will raise an exception if we
        # loop through too many times.
        # In order to do this properly, we might need to use a
        # proper parsing library like pyparsing.
        count = 0
        while re.search(u'（.*?）', string):
            string = re.sub(u'（.[^（]*?）', u'', string)
            count += 1
            if count > 100:
                raise Exception(
                        "Looped thru string too many times looking for matching ().")

        return string


    def clean_def_string(self, def_string):
        """
        Cleans up a definition string and splits up the definition parts.
        Removed some html, a long with things in parenthesis.

        def_string (unicode): A definition string from an entry.

        Returns list of cleaned definition parts.
        """
        # remove things in brackets and parenthesis
        def_string = self.remove_parenthesis(def_string)
        def_string = re.sub(u'【.*?】', u'', def_string)
        def_string = re.sub(u'〈.*?〉', u'', def_string)

        # remove bold
        def_string = def_string.replace(u'<b>', u'')
        def_string = def_string.replace(u'</b>', u'')

        # remove stars
        def_string = def_string.replace(u'＊', u'')

        # replace big spaces with small spaces
        def_string = def_string.replace(u'  ', u' ')

        # deleting stars sometimes leaves extra spaces. remove these spaces
        def_string = def_string.replace(u'  ', u'')

        # the def string may start with a number like ［１］. delete this.
        def_string = re.sub(u'^［(１|２|３|４|５|６|７|８|９|０)+］', u'', def_string)

        # strip whitespace
        def_string = def_string.strip()

        # remove trailing period
        if len(def_string) > 0 and def_string[-1] == u'.':
            def_string = def_string[:-1]

        # strip whitespace again after deleting previous period
        def_string = def_string.strip()

        # split up the definition parts, breaking on ';'
        def_parts = self.split_def_parts(def_string, split_characters=[u';', u',', u'.'])
        return def_parts

    @property
    def gaiji(self):
        return [
                    (u'g111a', u'〈'),
                    (u'g111b', u'〉'),
                    (u'g111c', u'⁝'),
                    (u'g111d', u'＊'),
                    (u'g111e', u'（同）'),
                    (u'g111f', u'Æ'),
                    (u'g1138', u'[形]'),
                    (u'g1139', u'[助]'),
                    (u'g113b', u'[接]'),
                    (u'g113e', u'[前]'),
                    (u'g113f', u'[代]'),
                    (u'g1142', u'[動]'),
                    (u'g1144', u'[副]'),
                    (u'g1145', u'[名]'),
                    (u'g1147', u'⇔'),
                    (u'g11f7', u'a'),
                    (u'g11f8', u'a'),
                    (u'g11f9', u'a'),
                    (u'g11fa', u'a'),
                    (u'g11fb', u'a'),
                    (u'g11fc', u'a'),
                    (u'g11fd', u'a'),
                    (u'g11fe', u'a'),
                    (u'g11ff', u'a'),
                    (u'g11bd', u'〔'),
                    (u'g11be', u'〕'),
                    (u'g1202', u'c'),
                    (u'g1203', u'c'),
                    (u'g1204', u'c'),
                    (u'g1205', u'd'),
                    (u'g1206', u'e'),
                    (u'g1207', u'e'),
                    (u'g1208', u'e'),
                    (u'g1209', u'e'),
                    (u'g120a', u'e'),
                    (u'g120b', u'e'),
                    (u'g120c', u'e'),
                    (u'g120d', u'e'),
                    (u'g120e', u'f'),
                    (u'g120f', u'g'),
                    (u'g1210', u'g'),
                    (u'g1211', u'g'),
                    (u'g1212', u'h'),
                    (u'g1213', u'h'),
                    (u'g1214', u'h'),
                    (u'g1215', u'i'),
                    (u'g1216', u'i'),
                    (u'g1217', u'i'),
                    (u'g1218', u'i'),
                    (u'g1219', u'i'),
                    (u'g121a', u'j'),
                    (u'g121b', u'm'),
                    (u'g121c', u'm'),
                    (u'g121d', u'n'),
                    (u'g121e', u'n'),
                    (u'g121f', u'n'),
                    (u'g1220', u'o'),
                    (u'g1221', u'o'),
                    (u'g1222', u'o'),
                    (u'g1223', u'o'),
                    (u'g1224', u'o'),
                    (u'g1225', u'p'),
                    (u'g1226', u'P'),
                    (u'g1227', u'q'),
                    (u'g1228', u'r'),
                    (u'g1229', u'r'),
                    (u'g122a', u'r'),
                    (u'g122b', u'r'),
                    (u'g122c', u's'),
                    (u'g122d', u's'),
                    (u'g122e', u't'),
                    (u'g122f', u'u'),
                    (u'g1230', u'u'),
                    (u'g1231', u'u'),
                    (u'g1232', u'u'),
                    (u'g1233', u'U'),
                    (u'g1234', u'w'),
                    (u'g1235', u'w'),
                    (u'g1236', u'x'),
                    (u'g1237', u'y'),
                    (u'g1238', u'y'),
                    (u'g1239', u'y'),
                    (u'g1253', u'A'),
                    (u'g1254', u'A'),
                    (u'g1255', u'B'),
                    (u'g1256', u'B'),
                    (u'g1257', u'C'),
                    (u'g1258', u'C'),
                    (u'g1259', u'D'),
                    (u'g125a', u'D'),
                    (u'g125b', u'E'),
                    (u'g125c', u'E'),
                    (u'g125d', u'F'),
                    (u'g125e', u'F'),
                    (u'g125f', u'G'),
                    (u'g1260', u'G'),
                    (u'g1261', u'H'),
                    (u'g1262', u'H'),
                    (u'g1263', u'I'),
                    (u'g1264', u'I'),
                    (u'g1265', u'I'),
                    (u'g1266', u'I'),
                    (u'g1267', u'L'),
                    (u'g1268', u'L'),
                    (u'g1269', u'M'),
                    (u'g126a', u'N'),
                    (u'g126b', u'N'),
                    (u'g126c', u'O'),
                    (u'g126d', u'O'),
                    (u'g126e', u'O'),
                    (u'g126f', u'O'),
                    (u'g1270', u'O'),
                    (u'g1271', u'P'),
                    (u'g1272', u'Q'),
                    (u'g1273', u'S'),
                    (u'g1274', u'S'),
                    (u'g1275', u'T'),
                    (u'g1276', u'T'),
                    (u'g1277', u'U'),
                    (u'g1278', u'U'),
                    (u'g1279', u'U'),
                    (u'g127a', u'V'),
                    (u'g127b', u'W'),
                    (u'g127c', u'X'),
                    (u'g127d', u'Y'),
                    (u'g127e', u'Z'),
                    (u'g127f', u'C'),
                    (u'g1280', u'L'),
                    (u'g1281', u'M'),
                    (u'g1282', u'V'),
                    (u'g1283', u'X'),
                    (u'g1293', u'e'),
                    (u'g1294', u'c'),
                    (u'g1295', u'A'),
                    (u'g1296', u'e'),
                    (u'g1297', u'G'),
                    (u'g1298', u'0'),
                    (u'g1299', u'o'),
                    (u'g129a', u'3'),
                    (u'g129b', u'e'),
                    (u'g129c', u'f'),
                    (u'g129d', u'n'),
                    (u'g129e', u'ae'),
                    (u'g129f', u'ae'),
                    (u'g12a0', u'c'),
                    (u'g12a1', u'c'),
                    (u'g12a2', u'A'),
                    (u'g12a3', u'e'),
                    (u'g12a4', u'e'),
                    (u'g12a5', u'e'),
                    (u'g12a6', u'e'),
                    (u'g12a7', u'ae'),
                    (u'g12cf', u':'),
                ]

    @property
    def gaiji_url(self):
        return u'http://i.yimg.jp/images/dic/ss/gnc/'

    def create_example_sentences(self, example_sentence_strings):
        """
        Create example sentence objects.

        example_sentence_strings (list of [jap_example_sent, eng_trans] tuples):
            These are the example sentences we want to clean up and turn
            into ExampleSentence objects.

        Returns a list of clean ExampleSentence objects.
        """
        example_sentences = []

        for jap_sentence, eng_trans in example_sentence_strings:
            # remove links
            eng_trans = re.sub(u'<a.*?>', u'', eng_trans)
            eng_trans = re.sub(u'</a>', u'', eng_trans)

            eng_trans = self.remove_parenthesis(eng_trans)

            # Sometimes there are "（※"  without a matching "）" on the end of the line...
            # Try to remove them.
            if re.search(u'（※', eng_trans) and not re.search(u'）', eng_trans):
                eng_trans = re.sub(u'（※.*$', u'', eng_trans)

            # Take out things like 〈やや書〉, 〈米話〉, and 〈米〉.
            eng_trans = re.sub(u'〈(やや書|米話|米|ことわざ|話|軽蔑的|集合的|英|書)〉(\s*)',
                    u'', eng_trans)

            # Take out things like 〔法律〕
            eng_trans = re.sub(u'〔(法律|医学)〕(\s*)', u' ', eng_trans)

            # There are often hints to japanese users that suggest words not to use
            # This looks like [show, × teach].
            # We want to take out the × items, but leave in the correct items.
            def remove_x_in_parens(eng_trans, opening_char, closing_char):
                escaped_opening_char = re.escape(opening_char)
                escaped_closing_char = re.escape(closing_char)

                matches = re.findall(u'%s(.*?)%s' %
                        (escaped_opening_char, escaped_closing_char), eng_trans)
                for m in matches:
                    words = m.split(',')
                    new_words = []
                    for w in words:
                        w = w.strip()
                        if w[0] != u'×':
                            new_words.append(w)
                    new_suggest = u''
                    for w in new_words:
                        new_suggest += u'%s, ' % w
                    if len(new_suggest) > 2 and new_suggest[-2:] == ', ':
                        new_suggest = new_suggest[:-2]

                    eng_trans = re.sub(u'%s%s%s' %
                            (escaped_opening_char, re.escape(m), escaped_closing_char),
                            u'%s%s%s' % (opening_char, new_suggest, closing_char), eng_trans)

                # after the previous replacement, we have to make sure there are
                # no [] groups left
                eng_trans = re.sub(u'(\s*)%s%s' % (escaped_opening_char, escaped_closing_char),
                        u'', eng_trans)

                return eng_trans

            eng_trans = remove_x_in_parens(eng_trans, '[', ']')
            eng_trans = remove_x_in_parens(eng_trans, '(', ')')

            # There are occasionally suggestions for opposites.
            # For example, "(⇔came up to)".  Take these out.
            eng_trans = re.sub(u'(\s*)\(⇔.*?\)', u'', eng_trans)

            # for japanese sentences, we want to change "..." to "…"
            jap_sentence = jap_sentence.replace(u'...', u'…')

            # for japanese sentences, we want to change "." to "。"
            jap_sentence = jap_sentence.replace(u'.', u'。')

            eng_trans = eng_trans.strip()
            jap_sentence = jap_sentence.strip()

            example_sentences.append(ExampleSentence(jap_sentence, eng_trans))

        return example_sentences

    def create_definitions_from_html(self, html_definitions):
        definitions = []

        for splt in html_definitions:
            # find english definition
            english_def = u''

            # remove first table stuff
            splt = re.sub(u'^(<td>\n)?<table border="0" cellspacing="0" cellpadding="0"><tr valign="top"><td>', u'', splt)

            # make sure not to match on the initial character telling whether
            # it is a noun,verb, etc
            match = re.search(u'^(.*?)</td></tr></table>', splt)
            if match and not splt.startswith('<table'):
                english_def = match.group(1)

            # find example sentences
            example_sentence_strings = []
            matches = re.findall(u'<td><small><font color="#008800"><b>(.*?)</b></font><br><font color="#666666">(.*?)</font></small></td>', splt)
            if matches:
                for m in matches:
                    jap_example_sentence = m[0]
                    eng_trans = m[1]
                    example_sentence_strings.append([jap_example_sentence, eng_trans])

            # find kaiwa
            matches = re.findall(u'<font color="#660000"><b>会話</b></font><br> <br><small>(.*?)」 “(.*?)</small>', splt)
            if matches:
                for m in matches:
                    jap_example_sentence = u'%s」' % m[0]
                    eng_trans = u'“%s' % m[1]
                    example_sentence_strings.append([jap_example_sentence, eng_trans])

            def_parts = self.clean_def_string(english_def)
            example_sentences = self.create_example_sentences(example_sentence_strings)

            definitions.append(Definition(def_parts, example_sentences))

        return definitions

    def split_definitions_html(self, html):
        # split the definitions into the big I, II, groups
        html_definitions = []

        big_splits = re.split(u'(?:<table border="0" cellspacing="0" cellpadding="0"><tr valign="top"><td>\[(?:名|動|形)\](?:</td></tr></table><br>)?)', html)
        if len(big_splits) > 1:
            big_splits = big_splits[1:]

        for s in big_splits:
            # split the page into pieces for each definition
            small_splits = re.split(u'(?:<table border="0" cellspacing="0" cellpadding="0"><tr valign="top"><td><b>［[１|２|３|４|５|６|７|８|９|０]+］</b>)', s)
            # throw away the first split because it's useless information
            if len(small_splits) > 1:
                small_splits = small_splits[1:]

            html_definitions += small_splits

        real_html_defs = []

        for h in html_definitions:
            smaller_splits = re.split(u'(?:<td>[0-9]+\u300A.*?\u300B)', h)
            #if len(smaller_splits) > 1:
            #    smaller_splits = smaller_splits[1:]

            real_html_defs += smaller_splits

        return real_html_defs

    def preclean_html(self, html_string):
        """
        Clean up the big picture HTML. For example, this cleans things out from
        the beginning that we don't want.
        """
        html_string = self.replace_gaiji(html_string)
        return html_string

    def parse_definition(self, tree):
        def_elems = tree.xpath("//table[@class='d-detail']/tr/td")[0]
        html = etree.tostring(def_elems, pretty_print=False, method="html", encoding='unicode')

        html = self.preclean_html(html)
        html_definitions = self.split_definitions_html(html)
        definitions = self.create_definitions_from_html(html_definitions)

        return definitions


