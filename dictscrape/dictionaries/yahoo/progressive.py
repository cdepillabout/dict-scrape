# -*- coding: UTF-8 -*-

import re

from lxml import etree

from ..dictionary import Dictionary
from .yahoo import YahooDictionary

from ...example_sentence import ExampleSentence
from ...definition import Definition

class ProgressiveDictionary(YahooDictionary):
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
        """
        # remove things in parenthesis
        def_string = re.sub(u'\(\(.*?\)\)', u'', def_string)
        def_string = re.sub(u'\(.*?\)', u'', def_string)

        # take out things in those weird japanese parenthesis
        def_string = re.sub(u'〔.*?〕', u'', def_string)

        # if it is just a redirect, then just take the word being redirected to
        def_string = re.sub(u'⇒<a href=".*?"><b>(.*?)</b></a>', ur'\1', def_string)

        # strip whitespace
        def_string = def_string.strip()

        # remove trailing period
        if len(def_string) > 0 and def_string[-1] == u'.':
            def_string = def_string[:-1]

        # split up the definition parts, breaking on ';'
        def_parts = self.split_def_parts(def_string, split_characters=u';')
        return def_parts

    def replace_gaiji(self, string):
        """
        Replace the gaiji that occur in the string with actual characters.
        """
        # TODO: this is nowhere near complete
        string = string.replace(u'<img src="http://dic.yahoo.co.jp/images/V2/yh_gaiji/l/AE8.gif" align="absmiddle" border="0">', u'e')
        string = string.replace(u'<img src="http://dic.yahoo.co.jp/images/V2/yh_gaiji/l/D32.gif" align="absmiddle" border="0">', u'a')
        string = string.replace(u'<img src="http://dic.yahoo.co.jp/images/V2/yh_gaiji/l/D5D.gif" align="absmiddle" border="0">', u'c')
        string = string.replace(u'<img src="http://dic.yahoo.co.jp/images/V2/yh_gaiji/l/D90.gif" align="absmiddle" border="0">', u'e')

        return string

    def clean_eng_example_sent(self, eng_trans):
        """
        Cleans up an english example sentence.
        """
        # take out things in those weird japanese parenthesis
        eng_trans = re.sub(u'〔.*?〕', u'', eng_trans)

        # take out italic tags
        eng_trans = eng_trans.replace(u'<i>', u'')
        eng_trans = eng_trans.replace(u'</i>', u'')

        # remove 「
        eng_trans = eng_trans.replace(u'「', u'')

        # remove ((口))
        eng_trans = eng_trans.replace(u'((口))', u'')

        # strip whitespace
        eng_trans = eng_trans.strip()

        # fix some gaiji
        eng_trans = self.replace_gaiji(eng_trans)

        return eng_trans

    def parse_definition(self, tree):
        # TODO: For now, we ignore words like "強迫観念" that come up when
        # looking up "強迫".

        defs = tree.xpath("//table[@class='d-detail']/tr/td")[0]
        result = etree.tostring(defs, pretty_print=False, method="html", encoding='unicode')

        definitions = []

        multiple_defs = True

        # do we have multiple definitions?
        matches = re.search(u'^<td>\n(<b>I</b><br><br>)?<b>1</b> 〔', result)
        if matches:
            # split the page into pieces for each definition
            splits = re.split(u'(<b>[1|2|3|4|5|6|7|8|9|0]+</b> 〔)', result)
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
            multiple_defs = False

        for splt in splits:
            # find english definition
            english_def = u''
            # make sure not to match on the initial character telling whether
            # it is a noun,verb, etc
            if multiple_defs == True:
                match = re.search(u'<b>[1|2|3|4|5|6|7|8|9|0]+</b> 〔(.*?)<br><br>', splt)
                if match:
                    english_def = u'〔%s' % match.group(1)
            else:
                match = re.search(u'^<td>\n(.*?)<br>(<br>◇.*?｜(.*?)<br><br>)?', splt)
                if match:
                    if not match.group(1).startswith(u'[例文]'):
                        english_def =  match.group(1)
                        if match.group(3):
                            english_def = "%s; %s" % (english_def, match.group(3))


            # find example sentences
            example_sentences = []
            matches = re.findall(u'<td><small><font color="#008800"><b>(.*?)</b></font><br><font color="#666666">(.*?)</font></small></td>', splt)
            if matches:
                for m in matches:
                    jap_sent = m[0]
                    eng_sent = self.clean_eng_example_sent(m[1])
                    example_sentences.append(ExampleSentence(jap_sent, eng_sent))

            def_parts = self.clean_def_string(english_def)

            definitions.append(Definition(def_parts, example_sentences))

        return definitions
