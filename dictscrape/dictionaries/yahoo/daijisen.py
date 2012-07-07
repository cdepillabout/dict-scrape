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

class DaijisenDictionary(YahooDictionary):
    """
    Daijisen Dictionary from Yahoo.
    """

    long_dictionary_name = u"Yahoo's Daijisen (大辞泉)"
    short_dictionary_name = "Daijisen"
    dictionary_type = Dictionary.DAIJISEN_TYPE
    dtype_search_param = '0'
    dname_search_param = '0na'

    def __init__(self):
        pass

    def split_example_sentences(self, example_sentences_string):
        """
        Split a list of example sentences into separate ExampleSentence objects.
        For instance, if passed the string 「これは日本語です。」「私は犬です。」,
        it would return the list [ExampleSentence("これは日本語です。"),
        ExampleSentence("私は犬です。")].
        """
        assert(isinstance(example_sentences_string, unicode))
        splits = example_sentences_string.split(u'」')
        example_sentences = []
        for s in splits:
            if s:
                if s[0] == u'「':
                    s = s[1:]
                example_sentences.append(ExampleSentence(s, u''))
        return example_sentences

    def create_def(self, def_string, extra_example_sentences=[]):
        """
        Takes a def string, splits up the defintion parts,
        takes out the example sentences, and puts it all together in
        a definition object.

        For instance, with the defintion string
        "あることをするよう無理に要求すること。むりじい。「寄付を―する」",
        it will basically create something like this:

        part1 = DefinitionPart("あることをするよう無理に要求すること")
        part2 = DefinitionPart("むりじい")
        ex_sent = ExampleSentence("寄付を―する", "")
        return Definition([part1, part2], [ex_sent])
        """

        # these need to be cleaned here too
        def_string = re.sub(u'^［(形動|名|動.*?|名・形動|副)］', u'', def_string)

        # this is trying to catch things like 彫刻 where there is →彫塑
        # at the end of the definition string.  Move this to before the 「」 parts.
        def_string = re.sub(u'^(.*?。)(「.*?)→(.*?)$', ur'\1\3。\2', def_string)

        def_parts = self.split_def_parts(def_string)
        example_sentences = []

        # check to see if the last part of the definition contains
        # example sentences.  The second part of this comparison is trying to
        # catch bad things like the definition for 遊ぶ（あすぶ）which is something
        # like 「あそぶ」の音変化。TODO: This still wouldn't work if it had example
        # sentences.
        if def_parts[-1].part.startswith(u'「') and def_parts[-1].part[-1] == u'」':
            example_sentences_string = def_parts[-1].part
            def_parts = def_parts[:-1]
            example_sentences = self.split_example_sentences(example_sentences_string)

        # append the extra example sentences
        for e in extra_example_sentences:
            example_sentences.append(ExampleSentence(e, u''))

        return Definition(def_parts, example_sentences)

    def create_definitions_from_html(self, html_definitions):
        """
        Returns a list of definition objects created from the list
        of html_definitions.
        """
        definitions = []
        for html_def in html_definitions:

            splits = html_def.split(u'<br>')
            html_def = splits[0]
            html_def = html_def.strip()

            # look for extra definitions
            for s in splits:
                if re.match(u'^(①|②|③|④|⑤|⑥|⑦|⑧|⑨|⑩|⑪|⑫|⑬|⑭|⑮|⑯|⑰|⑱|⑲|⑳)', s):
                    html_def += s[1:]

            # look for extra example sentences
            extra = u'<br>'.join(splits[1:])
            extra_example_sentences = []
            extra_example_sentences_matches = re.findall(
                        u'<table border="0" cellpadding="0" cellspacing="0"><tbody><tr valign="top"><td><img src="http://i.yimg.jp/images/clear.gif" height="1" width="25"></td><td valign="top"></td><td><small><font color="#008800"><b>(.*?)</b></font></small></td></tr></tbody></table>', extra)
            for match in extra_example_sentences_matches:
                extra_example_sentences.append(match)

            df = self.create_def(html_def, extra_example_sentences=extra_example_sentences)
            definitions.append(df)

        return definitions

    def split_definitions_html(self, html):
        """
        Splits the html for the definitions into different pieces for
        each definition.  Returns a list of strings of html for each definition.
        """
        html_definitions = []

        # split the definitions into the big ⓵ groups
        big_splits = re.split(u'<br>(?:⓵|⓶|⓷|⓸|⓹|⓺)', html)
        if len(big_splits) > 1:
            big_splits = big_splits[1:]

        for s in big_splits:
            # split the page into pieces for each definition
            small_splits = re.split(u'<b>[１|２|３|４|５|６|７|８|９|０]+</b>', s)
            # throw away the first split because it's useless information
            if len(small_splits) > 1:
                small_splits = small_splits[1:]

            html_definitions += small_splits

        return html_definitions

    @property
    def gaiji(self):
        return [
                    (u'01676', u'①'),
                    (u'01678', u'②'),
                    #(u'', u'③'),
                    #(u'', u'④'),
                    #(u'', u'⑤'),
                    #(u'', u'⑥'),
                    #(u'', u'⑦'),
                    #(u'', u'⑧'),
                    #(u'', u'⑨'),
                    #(u'', u'⑩'),
                    (u'02539', u'⓵'),
                    (u'02540', u'⓶'),
                    (u'02541', u'⓷'),
                    (u'02542', u'⓸'),
                    (u'02543', u'⓹'),
                    (u'02544', u'⓺'),
               ]

    @property
    def gaiji_url(self):
        return "http://dic.yahoo.co.jp/images/V2/yh_gaiji/l/"

    def preclean_html(self, html):
        """
        Cleans the html before it has been split or anything has been done to it.
        This will take out leading <td>s, verb types, etc.
        """
        html = re.sub(u'^<td>\n?', u'', html)

        # remove the verb conjugation markings
        # this removes ［形動］, etc from the beginning of a definition
        html = re.sub(u'^［(形動|名|動.*?|名・形動|副)］', u'', html)
        html = re.sub(u'^［文］', u'', html)
        html = re.sub(u'^［ナリ］', u'', html)
        html = re.sub(u'^\(スル\)', u'', html)

        # remove "arrows" groups
        # (this is the character that looks like two greater than signs
        # really close together)
        html = re.sub(u'\u300A.*?\u300B', u'', html)

        #html = re.sub(u'<br></td>.*$', u'', html)

        # remove links
        html = re.sub(u'<a.*?>', u'', html)
        html = re.sub(u'</a>', u'', html)

        # remove any arrows (⇒) redirecting to other entries
        html = html.replace(u'⇒', u'')

        html = self.replace_gaiji(html)

        return html

    def parse_definition(self, tree):
        defs = tree.xpath("//table[@class='d-detail']/tr/td")[0]
        html = etree.tostring(defs, pretty_print=False, method="html", encoding='unicode')

        html = self.preclean_html(html)
        definitions_html = self.split_definitions_html(html)
        definitions = self.create_definitions_from_html(definitions_html)

        return definitions
