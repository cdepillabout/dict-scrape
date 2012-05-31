#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

import re
import sys
import urllib

from lxml import etree
from StringIO import StringIO

#from IPython import embed ; embed()


hiragana = """
あいうえお
ぁぃぅぇぉ
かきくけこ
がぎぐげご
さしすせそ
ざじずぜぞ
たちつてと
だぢづでど
なにぬねの
はひふへほ
ばびぶべぼ
ぱぴぷぺぽ
や　ゆ　よ
ゃ　ゅ　ょ
らりるれろ
わゐ　ゑを
ゎ　っ
ん　ゔ　ー
"""
katakana = """
アイウエオ
ァィゥェォ
カキクケコ
ガギグゲゴ
サシスセソ
ザジズゼゾ
タチツテト
ダヂヅデド
ナニヌネノ
ハヒフヘホ
バビブベボ
パピプペポ
ヤ　ユ　ヨ
ャ　ュ　ョ
ラリルレロ
ワヰ　ヱヲ
ヮ　ッ
ン　ヴ　ー
"""
# get rid of unwanted characters
for i in (hiragana, katakana):
    i.replace("\n", "")
    i.replace(" ", "")
    i.replace("　", "")

class ExampleSentence(object):
    """
    A Japanese example sentence with an optional English translation.
    """
    def __init__(self, jap_sentence, eng_trans):
        self.result_jap_sentence = jap_sentence
        self.result_eng_trans = eng_trans

    @property
    def jap_sentence(self):
        return self.result_jap_sentence

    @property
    def eng_trans(self):
        return self.result_eng_trans

class Definition(object):
    """
    Contains the defintion from a dictionary along with example sentences.
    """
    def __init__(self, definition, example_sentences, kaiwa):
        self.result_definition = definition
        if example_sentences:
            self.result_example_sentences = example_sentences
        else:
            self.result_example_sentences = []

        if kaiwa:
            self.result_kaiwa = kaiwa
        else:
            self.result_kaiwa = []


    @property
    def definition(self):
        return self.result_definition

    @property
    def example_sentences(self):
        return self.result_example_sentences

    @property
    def kaiwai(self):
        return self.result_kaiwai

class Result(object):
    def __init__(self, kanji, kana, accent, jap_defs, eng_defs):
        self.result_kanji = kanji
        self.result_kana = kana
        self.result_accent = accent
        if jap_defs:
            self.result_jap_defs = jap_defs
        else:
            self.result_jap_defs = []
        if eng_defs:
            self.result_eng_defs = eng_defs
        else:
            self.result_eng_defs = []

    @property
    def kanji(self):
        return self.result_kanji

    @property
    def kana(self):
        return self.result_kana

    @property
    def accent(self):
        return self.result_accent

    @property
    def jap_defs(self):
        return self.result_jap_defs

    @property
    def eng_defs(self):
        return self.result_eng_defs

class Dictionary(object):
    DAIJIRIN_TYPE = 0
    DAIJISEN_TYPE = 1
    NEW_CENTURY_TYPE = 2
    PROGRESSIVE_TYPE = 3

    def __init__(self):
        pass

    def lookup(self, word_kanji, word_kana):
        tree = self.create_page_tree(word_kanji, word_kana)

        # make sure there is an entry
        result = etree.tostring(tree, pretty_print=False, method="html", encoding='UTF-8')
        word_not_found_string = \
                '<p><em>%s %s</em>に一致する情報はみつかりませんでした。</p>' % \
                (word_kanji, word_kana)
        word_not_found_string_no_space = \
                '<p><em>%s%s</em>に一致する情報はみつかりませんでした。</p>' % \
                (word_kanji, word_kana)

        # return None if we can't find a definition
        if word_not_found_string in result or word_not_found_string_no_space in result:
            #print("NO DEFINITION FOUND")
            return None

        # make sure this is the new century and not the progressive definition
        if self.dic_type == Dictionary.NEW_CENTURY_TYPE:
            if '<span class="dic-zero">ニューセンチュリー和英辞典</span>' in result:
                #print("NO DEFINITION FROM NEW CENTURY")
                return None

        kanji, kana, accent = self.parse_heading(tree)
        jap_defs_sentences, eng_defs_sentences = self.parse_definition(tree)
        return Result(kanji, kana, accent, jap_defs_sentences, eng_defs_sentences)

    def create_page_tree(self, word_kanji, word_kana):
        search = "%s　%s" % (word_kanji, word_kana)
        params = {'p': search, 'enc': "UTF-8", 'stype': 1,
                'dtype': self.dtype_search_param, 'dname': self.dname_search_param}
        encoded_params = urllib.urlencode(params)
        page = urllib.urlopen("http://dic.yahoo.co.jp/dsearch?%s" % encoded_params)
        page_string = page.read()

        parser = etree.HTMLParser()
        tree = etree.parse(StringIO(page_string), parser)
        return tree

    def parse_heading(self, tree):
        raise NotImplementedError, "This needs to be overrode in a child class."

    def parse_definition(self, tree):
        raise NotImplementedError, "This needs to be overrode in a child class."

    @property
    def dic_name(self):
        return self.dictionary_name

    @property
    def dic_type(self):
        return self.dictionary_type

class DaijirinDictionary(Dictionary):
    def __init__(self):
        self.dictionary_name = "Yahoo's Daijirin (大辞林)"
        self.dictionary_type = Dictionary.DAIJIRIN_TYPE
        self.dtype_search_param = '0'
        self.dname_search_param = '0ss'
        #super(DaijirinDictionary, self).__init__()

    def parse_heading(self, tree):
        div = tree.xpath("//div[@class='title-keyword']")[0]
        heading = div.getchildren()[0]
        children = heading.getchildren()

        result_accent = ""
        if children:
            for c in children:
                if c.tag == 'sub':
                    result_accent = heading.getchildren()[0].text

        result = heading.xpath("text()")
        result = "".join(result)

        m = re.search("^(.*)[ | |【|［|〔]".decode("utf-8"), result)
        if m:
            result_kana = m.group(1)
        else:
            # we didn't get a match, so the word we are trying to find
            # should just be the entire string
            result_kana = result

        # TODO: we will need to do a lot more to clean up the kana
        result_kana = result_kana.strip()

        # this is just in case we don't get any kanji later
        result_word = result_kana

        m = re.search("【(.*)】$".decode('utf-8'), result)
        if m:
            result_word = m.group(1)

        return result_word, result_kana, result_accent

    def parse_definition(self, tree):
        jap_defs = []
        definition_tables = tree.xpath("//table[@class='d-detail']/tr/td/table")
        for defi in definition_tables:
            result = etree.tostring(defi, pretty_print=True, method="html", encoding='UTF-8')
            text_def = defi.xpath("tr/td")[1]
            result = etree.tostring(text_def, pretty_print=False, method="html", encoding='UTF-8')
            result = re.sub("^<td>", "", result)
            result = re.sub("<br>.*$", "", result)
            result = result.strip()
            jap_defs.append(Definition(result, None, None))

        if not definition_tables:
            definition_tables = tree.xpath("//table[@class='d-detail']/tr/td")
            for defi in definition_tables:
                result = etree.tostring(defi, pretty_print=False, method="html", encoding='UTF-8')
                result = re.sub("^<td>", "", result)
                #result = re.sub("(?<! )<br>.*$", "", result)
                result = re.sub("<br></td>$", "", result)
                result = result.strip()
                jap_defs.append(Definition(result, None, None))

        return jap_defs, None

class DaijisenDictionary(DaijirinDictionary):
    def __init__(self):
        self.dictionary_name = "Yahoo's Daijisen (大辞泉)"
        self.dictionary_type = Dictionary.DAIJISEN_TYPE
        self.dtype_search_param = '0'
        self.dname_search_param = '0na'
        #super(DaijirinDictionary, self).__init__()

    def parse_definition(self, tree):
        defs = tree.xpath("//table[@class='d-detail']/tr/td")[0]
        result = etree.tostring(defs, pretty_print=False, method="html", encoding='UTF-8')
        jap_defs = []
        matches = re.findall("<b>[１|２|３|４|５|６|７|８|９|０]+</b> (.*?)<br>", result)
        if matches:
            for m in matches:
                jap_defs.append(Definition(m, None, None))
        else:
            result = re.sub("^<td>", "", result)
            result = re.sub("<br></td>.*$", "", result)
            result = result.strip()
            jap_defs.append(Definition(result, None, None))

        return jap_defs, None

class NewCenturyDictionary(DaijirinDictionary):
    def __init__(self):
        self.dictionary_name = "Yahoo's New Century Dictionary (ニューセンチュリー和英辞典)"
        self.dictionary_type = Dictionary.NEW_CENTURY_TYPE
        self.dtype_search_param = '3'
        self.dname_search_param = '2ss'

    def parse_definition(self, tree):
        def_elems = tree.xpath("//table[@class='d-detail']/tr/td")[0]
        result = etree.tostring(def_elems, pretty_print=False, method="html", encoding='UTF-8')

        # some replacements to make our lives easier
        result = result.replace('<img src="http://i.yimg.jp/images/dic/ss/gnc/g111a.gif" align="absbottom" border="0">', '〈')
        result = result.replace('<img src="http://i.yimg.jp/images/dic/ss/gnc/g111b.gif" align="absbottom" border="0">', '〉')
        result = result.replace('<img src="http://i.yimg.jp/images/dic/ss/gnc/g111c.gif" align="absbottom" border="0">', '⁝')
        result = result.replace('<img src="http://i.yimg.jp/images/dic/ss/gnc/g111d.gif" align="absbottom" border="0">', '＊')
        result = result.replace('<img src="http://i.yimg.jp/images/dic/ss/gnc/g111e.gif" align="absbottom" border="0">', '（同）')
        result = result.replace('<img src="http://i.yimg.jp/images/dic/ss/gnc/g111f.gif" align="absbottom" border="0">', 'Æ')

        definitions = []

        # do we have multiple definitions?
        matches = re.search('<table border="0" cellspacing="0" cellpadding="0"><tr valign="top"><td><b>［１］</b>', result)
        if matches:
            # split the page into pieces for each definition
            splits = re.split('(<table border="0" cellspacing="0" cellpadding="0"><tr valign="top"><td><b>［[１|２|３|４|５|６|７|８|９|０]+］</b>)', result)
            # make sure we have an odd number of splits
            assert(len(splits) % 2 == 1)
            # throw away the first split because it's useless information
            splits = splits[1:]
            # combine the following splits
            # This is stupidly complicated.  Basically we have a list like
            # ["ab", "cd", "ef", "gh", "hi", "jk"] and we want to combine it
            # to make a list like ["abcd", "efgh", "hijk"]
            splits = ["%s%s" % (splits[i], splits[i+1]) for i in range(0, len(splits), 2)]
        else:
            splits = [result]

        for splt in splits:
            # find english definition
            english_def = None
            # make sure not to match on the initial character telling whether
            # it is a noun,verb, etc
            match = re.search('<table border="0" cellspacing="0" cellpadding="0"><tr valign="top"><td>(?!<img src=".*?\.gif" align="absbottom" border="0">)(.*?)</td></tr></table>', splt)
            if match:
                english_def = match.group(1)

            # find example sentences
            example_sentences = []
            matches = re.findall('<td><small><font color="#008800"><b>(.*?)</b></font><br><font color="#666666">(.*?)</font></small></td>', splt)
            if matches:
                for m in matches:
                    jap_example_sentence = m[0]
                    eng_trans = m[1]
                    example_sentences.append(ExampleSentence(jap_example_sentence, eng_trans))

            # find kaiwa
            kaiwa = []
            matches = re.findall('<font color="#660000"><b>会話</b></font><br> <br><small>(.*?)」 “(.*?)</small>', splt)
            if matches:
                for m in matches:
                    jap_example_sentence = "%s」" % m[0]
                    eng_trans = "“%s" % m[1]
                    kaiwa.append(ExampleSentence(jap_example_sentence, eng_trans))

            definitions.append(Definition(english_def, example_sentences, kaiwa))

        return None, definitions

class ProgressiveDictionary(DaijirinDictionary):
    def __init__(self):
        self.dictionary_name = "Yahoo's Progressive Dictionary (プログレッシブ和英中辞典)"
        self.dictionary_type = Dictionary.PROGRESSIVE_TYPE
        self.dtype_search_param = '3'
        self.dname_search_param = '2na'

    def parse_definition(self, tree):
        defs = tree.xpath("//table[@class='d-detail']/tr/td")[0]
        result = etree.tostring(defs, pretty_print=False, method="html", encoding='UTF-8')

        definitions = []

        multiple_defs = True

        # do we have multiple definitions?
        matches = re.search('^<td>\n<b>1</b> 〔', result)
        if matches:
            # split the page into pieces for each definition
            splits = re.split('(<b>[1|2|3|4|5|6|7|8|9|0]+</b> 〔)', result)
            # make sure we have an odd number of splits
            assert(len(splits) % 2 == 1)
            # throw away the first split because it's useless information
            splits = splits[1:]
            # combine the following splits
            # This is stupidly complicated.  Basically we have a list like
            # ["ab", "cd", "ef", "gh", "hi", "jk"] and we want to combine it
            # to make a list like ["abcd", "efgh", "hijk"]
            splits = ["%s%s" % (splits[i], splits[i+1]) for i in range(0, len(splits), 2)]
        else:
            splits = [result]
            multiple_defs = False

        for splt in splits:
            # find english definition
            english_def = None
            # make sure not to match on the initial character telling whether
            # it is a noun,verb, etc
            if multiple_defs == True:
                match = re.search('<b>[1|2|3|4|5|6|7|8|9|0]+</b> 〔(.*?)<br><br>', splt)
                if match:
                    english_def = "〔%s" % match.group(1)
            else:
                match = re.search('^<td>\n(.*?)<br>', splt)
                if match:
                    if not match.group(1).startswith("[例文]"):
                        english_def =  match.group(1)


            # find example sentences
            example_sentences = []
            matches = re.findall('<td><small><font color="#008800"><b>(.*?)</b></font><br><font color="#666666">(.*?)</font></small></td>', splt)
            if matches:
                for m in matches:
                    example_sentences.append(ExampleSentence(m[0], m[1]))

            definitions.append(Definition(english_def, example_sentences, None))

        return None, definitions

def main(word_kanji, word_kana):
    check_daijirin(word_kanji, word_kana)
    print
    check_daijisen(word_kanji, word_kana)
    print
    check_new_century(word_kanji, word_kana)
    print
    check_progressive(word_kanji, word_kana)

if __name__ == '__main__':

    words = [
            ('強迫', 'きょうはく'),
            ('面白い', 'おもしろい'),
            ('赤し', 'あかし'),
            ('うっとり', ''),
            ('バリカン', ''),
            ('コンピエーニュ', ''),
            ('蜥蜴', 'とかげ'),
            ('らくだ', '駱駝'),
            ('成り済ます', 'なりすます'),
            #('行く', 'いく'),
            ('が', ''),
            ('遊ぶ', 'あそぶ'),
            #('遊ぶ', 'あすぶ'),        # this fails in the daijirin
            #('唸る', 'うなる'),         # this doesn't parse right in the progressive dict
            ]

    """
    for one, two in words:
        main(one, two)
        print
        """
    one = words[0]
    #main(one[0], one[1])

    daijirin_dic = DaijirinDictionary()
    daijisen_dic = DaijisenDictionary()
    new_century_dic = NewCenturyDictionary()
    progressive_dic = ProgressiveDictionary()

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
            if result.jap_defs:
                print("jap defs:")
            print_all_defs(result.jap_defs)
            if result.eng_defs:
                print("eng defs:")
            print_all_defs(result.eng_defs)
            print

