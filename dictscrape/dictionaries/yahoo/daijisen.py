# -*- coding: UTF-8 -*-

import re

from lxml import etree

from ..dictionary import Dictionary
from .yahoo import YahooDictionary

from ...example_sentence import ExampleSentence
from ...definition import Definition

class DaijisenDictionary(YahooDictionary):
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
            example_sentences.append(ExampleSentence(self.clean_def_string(e), u''))

        return Definition(def_parts, example_sentences)

    def clean_def_string(self, def_string):
        """
        Cleans a definition string.  It takes out <a> tags.
        """
        def_string = re.sub(u'<a.*?>', u'', def_string)
        def_string = re.sub(u'</a>', u'', def_string)

        # remove "arrows" groups
        # (this is the character that looks like two greater than signs
        # really close together)
        def_string = re.sub(u'\u300A.*?\u300B', u'', def_string)

        return def_string

    def parse_definition(self, tree):
        defs = tree.xpath("//table[@class='d-detail']/tr/td")[0]
        result = etree.tostring(defs, pretty_print=False, method="html", encoding='unicode')
        jap_defs = []
        matches = re.split(u'(<b>[１|２|３|４|５|６|７|８|９|０]+</b>.*?<br>)', result)
        if matches and len(matches) > 1:
            for i,m in enumerate(matches):
                # check this match and see if it has a definition
                def_match = re.search(
                        u'<b>[１|２|３|４|５|６|７|８|９|０]+</b> (.*?)<br>', m)
                # if there is no match, then we just continue the function
                if not def_match:
                    continue
                definition = def_match.group(1)

                # look for extra example sentences in the next match object
                extra_example_sentences = []
                if len(matches) > i+1:
                    extra_example_sentences_matches = re.findall(
                            u'<table border="0" cellpadding="0" cellspacing="0"><tbody><tr valign="top"><td><img src="http://i.yimg.jp/images/clear.gif" height="1" width="25"></td><td valign="top"></td><td><small><font color="#008800"><b>(.*?)</b></font></small></td></tr></tbody></table>', matches[i+1])
                    for match in extra_example_sentences_matches:
                        extra_example_sentences.append(match)
                definition = self.clean_def_string(definition)
                df = self.create_def(definition, extra_example_sentences)
                jap_defs.append(df)
        else:
            result = re.sub(u'^<td>', u'', result)
            result = re.sub(u'<br></td>.*$', u'', result)

            # remove "arrows" groups
            # (this is the character that looks like two greater than signs
            # really close together)
            result = re.sub(u'\u300A.*?\u300B', u'', result)

            # remove the verb conjugation markings
            # for instance, we take out things like ［動カ五（四）］
            result = re.sub(u'^\n［動.*?］', u'', result)

            # remove any arrows (⇒) redirecting to other entries
            result = result.replace(u'⇒', u'')

            # look for extra example sentences
            extra_example_sentences = []
            extra_example_sentences_matches = re.findall(
                        u'<table border="0" cellpadding="0" cellspacing="0"><tbody><tr valign="top"><td><img src="http://i.yimg.jp/images/clear.gif" height="1" width="25"></td><td valign="top"></td><td><small><font color="#008800"><b>(.*?)</b></font></small></td></tr></tbody></table>', result)
            for match in extra_example_sentences_matches:
                extra_example_sentences.append(match)

            # remove the </br>s and everything after them
            result = re.sub(u'<br>.*$', u'', result)
            result = result.strip()
            result = self.clean_def_string(result)
            jap_defs.append(self.create_def(result, extra_example_sentences))

        return jap_defs
