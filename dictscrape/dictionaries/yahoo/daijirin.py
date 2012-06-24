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
from ...definition import DefinitionPart, Definition

class DaijirinDictionary(YahooDictionary):
    """
    Daijirin Dictionary from Yahoo.
    """

    long_dictionary_name = u"Yahoo's Daijirin (大辞林)"
    short_dictionary_name = "Daijirin"
    dictionary_type = Dictionary.DAIJIRIN_TYPE
    dtype_search_param = '0'
    dname_search_param = '0ss'

    def __init__(self):
        #super(DaijirinDictionary, self).__init__()
        pass

    def parse_example_sentences(self, result):
        """
        Take an html definition string and parse out the example sentences.
        This looks for example sentences through their html and coloring coloring.

        result (unicode): the html string for this definition

        Returns a list of ExampleSentence objects.
        """
        example_sentences = []

        matches = re.findall(
                u'<small><font color="#008800"><b>(.*?)</b></font></small>', result)
        if matches:
            for m in matches:
                example_sentences.append(ExampleSentence(m, u''))

        return example_sentences

    def clean_definition(self, result):
        """
        Cleans a definition string.
        """
        result = re.sub(u'^<td>(\n)?', u'', result)
        result = re.sub(u'<br></td>$', u'', result)
        result = result.strip()

        # remove the verb conjugation from the beginning
        result = re.sub(u'^\n?<b>\(動..［.］\)</b> <br>', u'', result)
        result = re.sub(u'^\n?<b>\((形動|名)\)</b> <br>', u'', result)
        result = re.sub(u'^\n?<b><small>(\[文\])?(ナリ|スル)</small></b> <br>', u'', result)

        # remove the 補説 from the beginning
        result = re.sub(u'^\n?<b>〔補説〕</b> .*?<br>', u'', result)

        # remove the〔可能〕at the end of the entry
        result = re.sub(u'<br><b>〔可能〕</b> .*$', u'', result)

        # remove everything after the first <br>
        result = re.sub(u'<br>.*$', u'', result)
        result = result.strip()

        return result

    def clean_html(self, html_string):
        """
        Clean up the big picture HTML. For example, this cleans things out from
        the beginning that we don't want.
        """
        # remove beginning <td>
        html_string = re.sub(u'^<td>\n?', u'', html_string)

        #<b>(形)</b> <br><b><small>[文]ク おもしろ・し</small>

        # remove beginning word type
        html_string = re.sub(u'^<b>\((形ク?|動..［.］|名|形動)\)</b> ?(<br>)?', u'', html_string)

        #<b><small>[文]ク おもしろ・し</small></b> <br>

        # remove conjugation stuff
        html_string = re.sub(u'^<b><small>.*?</small></b> ?(<br>)?', u'', html_string)

        # remove verb types

        # remove 補説
        html_string = re.sub(u'^<b>〔補説〕</b> .*?<br>', u'', html_string)

        # turn redirections into just the normal word
        html_string = re.sub(u'→<a href="http://.*?">(.*?)</a>', ur'\1', html_string)

        return html_string

    def parse_definition(self, tree):
        jap_defs = []

        def_elems = tree.xpath("//table[@class='d-detail']/tr/td")[0]
        result = etree.tostring(def_elems, pretty_print=False, method="html",
                encoding='unicode')

        #print result

        result = self.clean_html(result)

        #print result
        definitions = []
        matches = re.search(u'<table><tr valign="top" align="left" num="3"><td><b>［1］</b>', result)
        if matches:
            # split the page into pieces for each definition
            splits = re.split(u'(<table><tr valign="top" align="left" num="3"><td><b>.*?</b>)', result)

            # throw away the first split
            splits = splits[1:]

            # throw away odd splits
            splits = [s for i, s in enumerate(splits) if i % 2 == 1]
        else:
            splits = [result]

        for splt in splits:
            # find english definition
            jap_def = u''

            # remove leading <td>
            splt = re.sub(u'^<td>\n?', u'', splt)
            # remove leading </td>
            splt = re.sub(u'^</td>\n?', u'', splt)
            # remove leading <td>
            splt = re.sub(u'^<td>\n?', u'', splt)

            # remove 補説
            splt = re.sub(u'^<b>〔補説〕</b> .*?<br>', u'', splt)

            match = re.search(u'^(.*?)(?=<br>)', splt)
            if match:
                jap_def = match.group(1)

            # find example sentences
            example_sentence_strings = []
            matches = re.findall(u'<td><small><font color="#008800"><b>(.*?)</b></font><br><font color="#666666">(.*?)</font></small></td>', splt)
            if matches:
                for m in matches:
                    jap_example_sentence = m[0]
                    eng_trans = m[1]
                    example_sentence_strings.append([jap_example_sentence, eng_trans])

            jap_def = self.clean_definition(jap_def)
            def_parts = self.split_def_parts(jap_def)
            example_sentences = self.parse_example_sentences(splt)

            definitions.append(Definition(def_parts, example_sentences))


        return definitions
