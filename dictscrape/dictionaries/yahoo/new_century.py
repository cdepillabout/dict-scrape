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
    dictionary_type = Dictionary.NEW_CENTURY_TYPE
    dtype_search_param = '3'
    dname_search_param = '2ss'

    def __init__(self):
        pass

    def clean_def_string(self, def_string):
        """
        Cleans up a definition string and splits up the definition parts.
        Removed some html, a long with things in parenthesis.

        def_string (unicode): A definition string from an entry.

        Returns list of cleaned definition parts.
        """
        # remove things in brackets and parenthesis
        def_string = re.sub(u'【.*?】', u'', def_string)
        def_string = re.sub(u'〈.*?〉', u'', def_string)
        def_string = re.sub(u'（.*?）', u'', def_string)
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
        def_parts = self.split_def_parts(def_string, split_characters=[u';', u','])
        return def_parts

    def replace_gaiji(self, string):
        """
        Replace the gaiji that occur in the string with actual characters.
        """
        def helper(string, gaiji_code, real_character):
            return string.replace(u'<img src="http://i.yimg.jp/images/dic/ss/gnc/%s.gif" align="absbottom" border="0">' % gaiji_code, real_character)

        string = helper(string, u'g111a', u'〈')
        string = helper(string, u'g111b', u'〉')
        string = helper(string, u'g111c', u'⁝')
        string = helper(string, u'g111d', u'＊')
        string = helper(string, u'g111e', u'（同）')
        string = helper(string, u'g111f', u'Æ')

        string = helper(string, u'g1147', u'⇔')

        string = helper(string, u'g11f7', u'a')
        string = helper(string, u'g11f8', u'a')
        string = helper(string, u'g11f9', u'a')

        string = helper(string, u'g11bd', u'〔')
        string = helper(string, u'g11be', u'〕')

        string = helper(string, u'g1202', u'c')
        string = helper(string, u'g1203', u'c')
        string = helper(string, u'g1204', u'c')
        string = helper(string, u'g1205', u'd')
        string = helper(string, u'g1206', u'e')
        string = helper(string, u'g1207', u'e')
        string = helper(string, u'g1208', u'e')
        string = helper(string, u'g1209', u'e')
        string = helper(string, u'g1210', u'g')
        string = helper(string, u'g1211', u'g')
        string = helper(string, u'g1212', u'h')
        string = helper(string, u'g1213', u'h')
        string = helper(string, u'g1214', u'h')
        string = helper(string, u'g1215', u'i')
        string = helper(string, u'g1216', u'i')
        string = helper(string, u'g1217', u'i')
        string = helper(string, u'g1218', u'i')
        string = helper(string, u'g1219', u'i')
        string = helper(string, u'g1220', u'o')
        string = helper(string, u'g1221', u'o')
        string = helper(string, u'g1222', u'o')
        string = helper(string, u'g1223', u'o')
        string = helper(string, u'g1224', u'o')
        string = helper(string, u'g1225', u'p')
        string = helper(string, u'g1226', u'P')
        string = helper(string, u'g1227', u'q')
        string = helper(string, u'g1228', u'r')
        string = helper(string, u'g1229', u'r')
        string = helper(string, u'g1230', u'u')
        string = helper(string, u'g1231', u'u')
        string = helper(string, u'g1232', u'u')
        string = helper(string, u'g1233', u'U')
        string = helper(string, u'g1234', u'w')
        string = helper(string, u'g1235', u'w')
        string = helper(string, u'g1236', u'x')
        string = helper(string, u'g1237', u'y')
        string = helper(string, u'g1238', u'y')
        string = helper(string, u'g1238', u'y')


        string = helper(string, u'g129b', u'e')
        return string

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

            # replace gaiji characters
            #eng_trans = self.replace_gaiji(eng_trans)

            # Remove parenthesis.  This is a little difficult because
            # we have to loop through the list multiple times until we
            # are certain there are no more parenthesis.  Just to be
            # on the safe side, we will raise an exception if we
            # loop through too many times.
            # In order to do this properly, we might need to use a
            # proper parsing library like pyparsing.
            count = 0
            while re.search(u'（.*?）', eng_trans):
                eng_trans = re.sub(u'（.[^（]*?）', u'', eng_trans)
                count += 1
                if count > 100:
                    raise Exception(
                            "Looped thru eng_trans too many times looking for matching ().")

            # Sometimes there are "（※"  without a matching "）" on the end of the line...
            # Try to remove them.
            if re.search(u'（※', eng_trans) and not re.search(u'）', eng_trans):
                eng_trans = re.sub(u'（※.*$', u'', eng_trans)

            # Take out things like 〈やや書〉, 〈米話〉, and 〈米〉.
            eng_trans = re.sub(u'〈(やや書|米話|米|ことわざ|話|軽蔑的|集合的)〉(\s*)', u'', eng_trans)

            # Take out things like 〔法律〕
            eng_trans = re.sub(u'〔法律〕(\s*)', u' ', eng_trans)

            # There are often hints to japanese users that suggest words not to use
            # This looks like [show, × teach].
            # We want to take out the × items, but leave in the correct items.
            matches = re.findall(u'\[(.*?)\]', eng_trans)
            for m in matches:
                words = m.split(',')
                new_words = []
                for w in words:
                    w = w.strip()
                    a = w[0] != u'×'
                    if w[0] != u'×':
                        new_words.append(w)
                new_suggest = u''
                for w in new_words:
                    new_suggest += u'%s, ' % w
                if len(new_suggest) > 2 and new_suggest[-2:] == ', ':
                    new_suggest = new_suggest[:-2]

                eng_trans = re.sub(u'\[%s\]' % re.escape(m),
                        u'[%s]' % new_suggest, eng_trans)

            # after the previous replacement, we have to make sure there are
            # no [] groups left
            eng_trans = re.sub(u'(\s*)\[\]', u'', eng_trans)

            # There are occasionally suggestions for opposites.
            # For example, "(⇔came up to)".  Take these out.
            eng_trans = re.sub(u'(\s*)\(⇔.*?\)', u'', eng_trans)

            # for japanese sentences, we want to change "." to "。"
            jap_sentence = jap_sentence.replace(u'.', u'。')

            eng_trans = eng_trans.strip()
            jap_sentence = jap_sentence.strip()

            example_sentences.append(ExampleSentence(jap_sentence, eng_trans))

        return example_sentences

    def parse_definition(self, tree):
        def_elems = tree.xpath("//table[@class='d-detail']/tr/td")[0]
        result = etree.tostring(def_elems, pretty_print=False, method="html",
                encoding='unicode')

        result = self.replace_gaiji(result)

        definitions = []

        # do we have multiple definitions?
        matches = re.search(u'<table border="0" cellspacing="0" cellpadding="0"><tr valign="top"><td><b>［１］</b>', result)
        if matches:
            # split the page into pieces for each definition
            splits = re.split(u'(<table border="0" cellspacing="0" cellpadding="0"><tr valign="top"><td><b>［[１|２|３|４|５|６|７|８|９|０]+］</b>)', result)
            # make sure we have an odd number of splits
            assert(len(splits) % 2 == 1)
            # throw away the first split because it's useless information
            splits = splits[1:]
            # combine the following splits
            # This is stupidly complicated.  Basically we have a list like
            # ["ab", "cd", "ef", "gh", "hi", "jk"] and we want to combine it
            # to make a list like ["abcd", "efgh", "hijk"]
            splits = [u'%s%s' % (splits[i], splits[i+1]) for i in range(0, len(splits), 2)]
        else:
            splits = [result]

        for splt in splits:
            # find english definition
            english_def = u''
            # make sure not to match on the initial character telling whether
            # it is a noun,verb, etc
            match = re.search(u'<table border="0" cellspacing="0" cellpadding="0"><tr valign="top"><td>(?!<img src=".*?\.gif" align="absbottom" border="0">)(.*?)</td></tr></table>', splt)
            if match:
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
