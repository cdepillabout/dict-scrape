# -*- coding: UTF-8 -*-

import re

from lxml import etree

from ..dictionary import Dictionary
from .yahoo import YahooDictionary

from ...example_sentence import ExampleSentence
from ...definition import DefinitionPart, Definition

class DaijirinDictionary(YahooDictionary):
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
        This looks for example sentences through their coloring.
        """
        example_sentences = []

        matches = re.findall(
                u'<small><font color="#008800"><b>(.*?)</b></font></small>', result)
        if matches:
            for m in matches:
                example_sentences.append(ExampleSentence(m, u''))

        return example_sentences

    def parse_definition(self, tree):
        jap_defs = []
        definition_tables = tree.xpath("//table[@class='d-detail']/tr/td/table")
        for defi in definition_tables:
            result = etree.tostring(defi, pretty_print=True, method="html", encoding='unicode')
            example_sentences = self.parse_example_sentences(result)

            # words like 遊ぶ（あすぶ） don't have any tr/td elements, but they
            # do have example sentences
            if not defi.xpath(u'tr/td'):
                definition = tree.xpath("//table[@class='d-detail']/tr/td")[0]
                result = etree.tostring(definition, pretty_print=False, method="html",
                            encoding='unicode')
            else:
                text_def = defi.xpath(u'tr/td')[1]
                result = etree.tostring(text_def, pretty_print=False, method="html",
                        encoding='unicode')

            result = re.sub(u'^<td>', u'', result)

            # remove the verb conjugation from the beginning
            result = re.sub(u'^\n?<b>\(動..［.］\)</b> <br>', u'', result)

            # remove the 補説 from the beginning
            result = re.sub(u'^\n?<b>〔補説〕</b> .*?<br>', u'', result)

            # remove everything after the first <br>
            result = re.sub(u'<br>.*$', u'', result)
            result = result.strip()
            def_parts = self.split_def_parts(result)
            jap_defs.append(Definition(def_parts, example_sentences))

        if not definition_tables:
            definition_tables = tree.xpath("//table[@class='d-detail']/tr/td")
            for defi in definition_tables:
                result = etree.tostring(defi, pretty_print=False, method="html",
                        encoding='unicode')

                # this checks for if we are redirected to another entry.  For example,
                # for the word 赤し
                m = re.match(u'<td>\n<b>\(.*?\)</b> <br>→<a href=".*?">(.*?)</a><br></td>',
                        result)
                if m:
                    def_part = DefinitionPart(m.group(1))
                    jap_defs.append(Definition([def_part], None))
                    continue

                result = re.sub(u'^<td>', u'', result)
                result = re.sub(u'<br></td>$', u'', result)
                result = result.strip()

                # remove 補説 at the top of the entry
                result = re.sub(u'^<b>〔補説〕</b> (.*?)<br>', u'', result)

                # remove verb conjugation types at the top of the entry
                result = re.sub(u'^<b>\(動..［.］\)</b> <br>', u'', result)

                # remove the〔可能〕at the end of the entry
                result = re.sub(u'<br><b>〔可能〕</b> .*$', u'', result)

                result = result.strip()
                def_parts = self.split_def_parts(result)
                jap_defs.append(Definition(def_parts, None))

        return jap_defs
