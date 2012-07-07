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

class ProgressiveDictionary(YahooDictionary):
    """
    Progressive Dictionary from Yahoo.
    """

    long_dictionary_name = u"Yahoo's Progressive Dictionary (プログレッシブ和英中辞典)"
    short_dictionary_name = "Progressive"
    dictionary_type = Dictionary.PROGRESSIVE_TYPE
    dtype_search_param = '3'
    dname_search_param = '2na'

    def __init__(self):
        pass

    def clean_def_string(self, def_string):
        """
        Cleans up a definition string and splits up the definition parts.
        Removed some html, a long with things in parenthesis.

        def_string (unicode): A definition string from an entry.

        Returns list of cleaned definition parts.
        """
        # remove things in parenthesis
        def_string = re.sub(u'\(\(.*?\)\)', u'', def_string)
        def_string = re.sub(u'\(.*?\)', u'', def_string)

        # take out things in those weird japanese parenthesis
        def_string = re.sub(u'〔.*?〕', u'', def_string)

        # if it is just a redirect, then just take the word being redirected to
        def_string = re.sub(u'⇒<a href=".*?"><b>(.*?)</b></a>', ur'\1', def_string)

        # remove italics
        def_string = def_string.replace(u'<i>', u'')
        def_string = def_string.replace(u'</i>', u'')

        # remove those little stars from the beginning of the definition
        def_string = re.sub(u'^◇', u'', def_string)

        # sometimes there is a japanese word, and then a '|', and then an
        # English definition.  Try to search for this and remove it.
        def_string = re.sub(
                u'^[\u3041-\u3096\u30A0-\u30FF\u3400-\u4DB5\u4E00-\u9FCB\uF900-\uFA6A]*｜',
                u'', def_string)

        # strip whitespace
        def_string = def_string.strip()

        # remove trailing period
        if len(def_string) > 0 and def_string[-1] == u'.':
            def_string = def_string[:-1]

        # replace gaiji characters
        def_string = self.replace_gaiji(def_string)

        # replace japanse ， with english ,
        def_string = def_string.replace(u'，', u',')
        def_string = def_string.replace(u'、', u',')

        # split up the definition parts, breaking on ';'
        def_parts = self.split_def_parts(def_string, split_characters=[u';', u','])

        # only get unique def parts
        new_def_parts = []
        for part in def_parts:
            if part not in new_def_parts:
                new_def_parts.append(part)
        def_parts = new_def_parts

        return def_parts

    @property
    def gaiji_url(self):
        return u'http://dic.yahoo.co.jp/images/V2/yh_gaiji/l/'

    @property
    def gaiji(self):
        return [
                (u'AE8', u'e'),
                (u'AE9', u'e'),
                (u'AED', u'i'),
                (u'AEE', u'i'),
                (u'AFA', u'u'),
                (u'AFB', u'u'),
                (u'AFC', u'u'),
                (u'AFD', u'y'),
                (u'AFE', u'p'),

                (u'D32', u'a'),
                (u'D5D', u'c'),
                (u'D90', u'e'),
                (u'D92', u'e'),

                (u'FC3', u'e'),

                (u'_817C', u':'),
            ]

    def clean_eng_example_sent(self, eng_trans):
        """
        Cleans up an english example sentence.

        eng_trans (unicode): a dirty english example sentence

        Returns a clean english example sentence.
        """
        # take out things in those weird japanese parenthesis
        eng_trans = re.sub(u'〔.*?〕', u'', eng_trans)

        # take out italic tags
        eng_trans = eng_trans.replace(u'<i>', u'')
        eng_trans = eng_trans.replace(u'</i>', u'')

        # remove 「
        eng_trans = eng_trans.replace(u'「', u'')

        # remove markings for normal speech and american speech like ((口))
        eng_trans = re.sub(u'\(\((口|米)\)\)', u'', eng_trans)

        # remove (▼...)
        eng_trans = re.sub(u'\(▼.*?\)', u'', eng_trans)

        # remove ⇒見出し語
        eng_trans = re.sub(u'⇒<a href=".*?">見出し語</a>', u'', eng_trans)

        # strip whitespace
        eng_trans = eng_trans.strip()

        # fix some gaiji
        eng_trans = self.replace_gaiji(eng_trans)

        return eng_trans

    def create_definitions_from_html(self, html_definitions):
        """
        Returns a list of definition objects created from the list
        of html_definitions.
        """
        definitions = []

        for html_def in html_definitions:
            # find english definition
            english_def = u''

            # remove leading <td>
            html_def = re.sub(u'^<td>(\n)?', u'', html_def)

            # remove leading bold number
            html_def = re.sub(u'^<b>[1|2|3|4|5|6|7|8|9|0]+</b> ?', u'', html_def)

            # remove leading japanese word
            html_def = re.sub(u'^〔.*?〕', u'', html_def)

            # make sure not to match on the initial character telling whether
            # it is a noun,verb, etc
            match = re.search(u'^(.*?)<br>', html_def)
            if match:
                match_text = match.group(1)
                if not match_text.startswith(u'◇'):
                    if not match_text.startswith(u'[例文]'):
                        if not re.search(u'^<b>.*?</b>｜(.*?)(<br>|$)', match_text):
                            english_def = match_text

            # look for additional verb definitions and add them to our main
            # definnition
            match = re.search(u'(?:<br>)?◇.*?｜(.*?)<br><br>', html_def)
            if match:
                if english_def:
                    english_def = "%s; %s" % (english_def, match.group(1))
                else:
                    english_def = match.group(1)

            # find example sentences
            example_sentences = []

            # take out bolded words if they are not part of an example sentence
            # or if they are not followed by a ｜ character
            html_def = re.sub(ur'(?<=<br>)<b>.*?</b>(?!(</font>)|｜)', u'', html_def)

            # match either real example sentences or those other bold words
            # like "強迫観念" that come up when looking up "強迫".
            matches = re.findall(u'(<td><small><font color="#008800"><b>(.*?)</b></font><br><font color="#666666">(.*?)</font></small></td>)|((?:<br>)?<b>(.*?)</b>｜(.*?)<br>)', html_def)
            if matches:
                for m in matches:
                    assert(len(m) == 6)
                    if m[1]:
                        assert(not m[4] and not m[5])
                        jap_sent = m[1]
                        eng_sent = self.clean_eng_example_sent(m[2])
                    else:
                        assert(not m[1] and not m[2])
                        jap_sent = m[4]
                        eng_sent = self.clean_eng_example_sent(m[5])

                    example_sentences.append(ExampleSentence(jap_sent, eng_sent))

            def_parts = self.clean_def_string(english_def)

            definitions.append(Definition(def_parts, example_sentences))

        return definitions

    def split_definitions_html(self, html):
        """
        Splits the html for the definitions into different pieces for
        each definition.  Returns a list of strings of html for each definition.
        """
        html_definitions = []

        # split the definitions into the big I, II, groups
        big_splits = re.split(u'(?:<b>(?:I|II|III|IV|V|VI|VII|VIII|IX|X)</b>)', html)
        if len(big_splits) > 1:
            big_splits = big_splits[1:]

        for s in big_splits:
            # split the page into pieces for each definition
            small_splits = re.split(u'(?:<b>[1|2|3|4|5|6|7|8|9|0]+</b> 〔.*?〕)', s)
            # throw away the first split because it's useless information
            if len(small_splits) > 1:
                small_splits = small_splits[1:]

            html_definitions += small_splits

        return html_definitions

    def preclean_html(self, html_string):
        """
        Clean up the big picture HTML. For example, this cleans things out from
        the beginning that we don't want.
        """
        return html_string

    def parse_definition(self, tree):
        defs = tree.xpath("//table[@class='d-detail']/tr/td")[0]
        html = etree.tostring(defs, pretty_print=False, method="html", encoding='unicode')

        html = self.preclean_html(html)
        html_definitions = self.split_definitions_html(html)
        definitions = self.create_definitions_from_html(html_definitions)

        return definitions
