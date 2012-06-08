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
        """
        jap_sentence is a sentence in Japanese and eng_trans is
        the English translation of that sentence.  Both are strings.
        """
        if type(jap_sentence) is not type(unicode()):
            raise UnicodeError, "jap_sentence should be a unicode string"
        if type(eng_trans) is not type(unicode()):
            raise UnicodeError, "eng_trans should be a unicode string"
        self.result_jap_sentence = jap_sentence
        self.result_eng_trans = eng_trans

    @property
    def jap_sentence(self):
        """Return the Japanese sentence."""
        return self.result_jap_sentence

    @property
    def eng_trans(self):
        """Return the English sentence."""
        return self.result_eng_trans

    def __unicode__(self):
        result_string = u"\n      - %s" % self.result_jap_sentence
        if self.result_eng_trans:
            result_string += u"\n        %s" % self.result_eng_trans
        return result_string

    def __str__(self):
        return unicode(self).encode("utf8")

    def to_jsonable(self):
        return {'jap_sentences': self.jap_sentence, 'eng_trans': self.eng_trans}

class Definition(object):
    """
    Contains the defintion from a dictionary along with example sentences.
    """
    def __init__(self, definition, example_sentences, kaiwa = []):
        """
        definition is the definition from a dictionary in either
        Japanese or English.  It should be a unicode object.
        example_sentences and kaiwa are lists of ExampleSentence objects.
        """
        if type(definition) is not type(unicode()):
            raise UnicodeError, "definition should be a unicode string"
        self._definition = definition

        if example_sentences:
            self._example_sentences = example_sentences
        else:
            self._example_sentences = []

        if kaiwa:
            self._kaiwa = kaiwa
        else:
            self._kaiwa = []


    @property
    def definition(self):
        """Return Japanese or English definition."""
        return self._definition

    @property
    def example_sentences(self):
        """Return a list of example sentences in the form of ExampleSentence objects."""
        return self._example_sentences

    @property
    def kaiwai(self):
        """Return a list of kaiwa in the form of ExampleSentence objects."""
        return self._kaiwai

    def __unicode__(self):
        if self._definition:
            result_string = u"\n＊ %s" % self._definition
        else:
            result_string = u"\nNO DEFINITION AVAILABLE"
        for e in self._example_sentences:
            result_string += unicode(e)
        return result_string

    def __str__(self):
        return unicode(self).encode("utf8")

    def to_jsonable(self):
        #TODO: NOT GETTING KAIWA"""
        ex_sentences = []
        for e in self.example_sentences:
            ex_sentences.append(e.to_jsonable())
        return {"definition": self.definition, "example_sentences": ex_sentences}

class Result(object):
    """
    This is an object representing the result of a dictionary lookup.
    """
    def __init__(self, original_kanji, original_kana, url,
            kanji=None, kana=None, accent=None, defs=[]):
        """
        kanji is a string with the kanji from the result. This may be the same
        as kana.
        kana is a string with the kana from the result.
        accent is the accent marking.  This may be None.
        defs is a list of Definition objects for the definitions
        contained in the dictionary.
        """
        if type(original_kanji) is not type(unicode()):
            raise UnicodeError, "original_kanji should be a unicode string"
        if type(original_kana) is not type(unicode()):
            raise UnicodeError, "original_kana should be a unicode string"
        if type(kanji) is not type(unicode()) and kanji is not None:
            raise UnicodeError, "kanji should be a unicode string"
        if type(kana) is not type(unicode()) and kana is not None:
            raise UnicodeError, "kana should be a unicode string"
        self._original_kanji = original_kanji
        self._original_kana = original_kana
        self._url = url
        self._kanji = kanji
        self._kana = kana
        self._accent = accent
        if defs:
            self._defs = defs
        else:
            self._defs = []

    @property
    def original_kanji(self):
        """Return the original kanji from the search."""
        return self._original_kanji

    @property
    def original_kana(self):
        """Return the original kana from the search."""
        return self._original_kana

    @property
    def url(self):
        """Return the url of the search."""
        return self._url

    @property
    def kanji(self):
        """Return the kanji from the dictionary."""
        return self._kanji

    @property
    def kana(self):
        """Return the kana from the dictionary."""
        return self._kana

    @property
    def accent(self):
        """Return the accent from the dictionary."""
        return self._accent

    @property
    def defs(self):
        """
        Return the Japanese definitions from the dictionary in
        a list of Definition objects.
        """
        return self._defs

    def definition_found(self):
        """
        Return true if this definition was found.
        i.e. kanji and kana are not null.
        """
        return (self._kanji and self._kana)

    def __str__(self):
        return unicode(self).encode("utf8")

    def __unicode__(self):
        result_string = u'RESULT: %s (%s) %s: (originally: %s %s [%s])' % \
                (self._kanji, self._kana, self._accent,
                        self._original_kanji, self._original_kana, self._url)
        for d in self._defs:
            result_string += unicode(d)
        return result_string

    def to_jsonable(self):
        dfs = []
        for d in self.defs:
            dfs.append(d.to_jsonable())
        return {"url": self.url, "kanji": self.kanji, "kana": self.kana,
                "accent": self.accent, "defs": dfs}




class Dictionary(object):
    """
    An object representing an online dictionary in which to lookup
    definitions.
    """

    # These are constants for the type of a dictionary.
    DAIJIRIN_TYPE = 0
    DAIJISEN_TYPE = 1
    NEW_CENTURY_TYPE = 2
    PROGRESSIVE_TYPE = 3

    def __init__(self):
        pass

    def lookup(self, word_kanji, word_kana):
        """
        Lookup a word in a dictionary.  word_kanji is a string
        for the kanji you want to lookup, and word_kana is the same
        but for the kana. Returns a Definition object or None if no
        result could be found.
        """
        tree = self.__create_page_tree(word_kanji, word_kana)

        # make sure there is an entry
        result = etree.tostring(tree, pretty_print=False, method="html", encoding='unicode')
        url = self._create_url(word_kanji, word_kana)
        word_not_found_string = \
                u'<p><em>%s %s</em>に一致する情報はみつかりませんでした。</p>' % \
                (word_kanji, word_kana)
        word_not_found_string_no_space = \
                u'<p><em>%s%s</em>に一致する情報はみつかりませんでした。</p>' % \
                (word_kanji, word_kana)

        # return None if we can't find a definition
        if word_not_found_string in result or word_not_found_string_no_space in result:
            #print("NO DEFINITION FOUND")
            return Result(word_kanji, word_kana, url)

        # make sure this is the new century and not the progressive definition
        if self.dic_type == Dictionary.NEW_CENTURY_TYPE:
            if u'<span class="dic-zero">ニューセンチュリー和英辞典</span>' in result:
                #print("NO DEFINITION FROM NEW CENTURY")
                return Result(word_kanji, word_kana, url)

        kanji, kana, accent = self.parse_heading(tree)
        defs_sentences = self.parse_definition(tree)
        return Result(word_kanji, word_kana, url, kanji, kana, accent, defs_sentences)

    def _create_url(self, word_kanji, word_kana):
        """Returns a URL for the word/page we are trying to lookup."""
        # this is annoying because urlencode only takes utf8 input for some reason
        search = "%s　%s" % (word_kanji.encode("utf8"), word_kana.encode("utf8"))
        params = {'p': search, 'enc': "UTF-8", 'stype': 1,
                'dtype': self.dtype_search_param, 'dname': self.dname_search_param}
        encoded_params = urllib.urlencode(params)
        return "http://dic.yahoo.co.jp/dsearch?%s" % encoded_params

    def _fetch_page(self, word_kanji, word_kana):
        """Fetches the word's page from the internet and returns its contents."""
        url = self._create_url(word_kanji, word_kana)
        page = urllib.urlopen(url)
        page_string = page.read()
        return page_string

    def __create_page_tree(self, word_kanji, word_kana):
        """
        Fetches a page from the internet and parses the page with
        etree.parse(StringIO(page_string), etree.HTMLParser()).
        Returns the parsed tree.
        """
        page_string = self._fetch_page(word_kanji, word_kana)

        parser = etree.HTMLParser()
        tree = etree.parse(StringIO(page_string), parser)
        return tree

    def parse_heading(self, tree):
        """
        Parses the heading of the dictionary page and returns a 3-tuple of
        the kanji for the word being looked up, the kana, and the accent.
        Return None for the accent if it doesn't exist.
        """
        raise NotImplementedError, "This needs to be overrode in a child class."

    def parse_definition(self, tree):
        """
        Parses the main definition of the dictionary page and returns a 2-tuple of
        a list of Definition objects for the Japanese definitions, and a list of
        Definition objects for the English definitions.
        """
        raise NotImplementedError, "This needs to be overrode in a child class."

    @property
    def long_dic_name(self):
        """Return the dictionary name."""
        return self.long_dictionary_name

    @property
    def short_name(self):
        """Return the dictionary name."""
        return self.short_dictionary_name

    @property
    def dic_type(self):
        """Return the dictionary type."""
        return self.dictionary_type

class DaijirinDictionary(Dictionary):
    long_dictionary_name = u"Yahoo's Daijirin (大辞林)"
    short_dictionary_name = "Daijirin"
    dictionary_type = Dictionary.DAIJIRIN_TYPE
    dtype_search_param = '0'
    dname_search_param = '0ss'

    def __init__(self):
        #super(DaijirinDictionary, self).__init__()
        pass

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
            jap_defs.append(Definition(result.decode("utf8"), None, None))

        if not definition_tables:
            definition_tables = tree.xpath("//table[@class='d-detail']/tr/td")
            for defi in definition_tables:
                result = etree.tostring(defi, pretty_print=False, method="html", encoding='UTF-8')
                result = re.sub("^<td>", "", result)
                #result = re.sub("(?<! )<br>.*$", "", result)
                result = re.sub("<br></td>$", "", result)
                result = result.strip()
                result = result.decode("utf8")
                jap_defs.append(Definition(result, None, None))

        return jap_defs

class DaijisenDictionary(DaijirinDictionary):
    long_dictionary_name = u"Yahoo's Daijisen (大辞泉)"
    short_dictionary_name = "Daijisen"
    dictionary_type = Dictionary.DAIJISEN_TYPE
    dtype_search_param = '0'
    dname_search_param = '0na'

    def __init__(self):
        pass

    def parse_definition(self, tree):
        defs = tree.xpath("//table[@class='d-detail']/tr/td")[0]
        result = etree.tostring(defs, pretty_print=False, method="html", encoding='UTF-8')
        jap_defs = []
        matches = re.findall("<b>[１|２|３|４|５|６|７|８|９|０]+</b> (.*?)<br>", result)
        if matches:
            for m in matches:
                jap_defs.append(Definition(m.decode("utf8"), None, None))
        else:
            result = re.sub("^<td>", "", result)
            result = re.sub("<br></td>.*$", "", result)
            result = result.strip()
            result = result.decode("utf8")
            jap_defs.append(Definition(result, None, None))

        return jap_defs

class NewCenturyDictionary(DaijirinDictionary):
    long_dictionary_name = u"Yahoo's New Century Dictionary (ニューセンチュリー和英辞典)"
    short_dictionary_name = "New_Century"
    dictionary_type = Dictionary.NEW_CENTURY_TYPE
    dtype_search_param = '3'
    dname_search_param = '2ss'

    def __init__(self):
        pass

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
                    jap_example_sentence = m[0].decode("utf8")
                    eng_trans = m[1].decode("utf8")
                    example_sentences.append(ExampleSentence(jap_example_sentence, eng_trans))

            # find kaiwa
            kaiwa = []
            matches = re.findall('<font color="#660000"><b>会話</b></font><br> <br><small>(.*?)」 “(.*?)</small>', splt)
            if matches:
                for m in matches:
                    jap_example_sentence = "%s」" % m[0]
                    eng_trans = "“%s" % m[1]

                    jap_example_sentence = jap_example_sentence.decode("utf8")
                    eng_trans = eng_trans.decode("utf8")

                    kaiwa.append(ExampleSentence(jap_example_sentence, eng_trans))

            definitions.append(Definition(english_def.decode("utf8"), example_sentences, kaiwa))

        return definitions

class ProgressiveDictionary(DaijirinDictionary):
    long_dictionary_name = u"Yahoo's Progressive Dictionary (プログレッシブ和英中辞典)"
    short_dictionary_name = "Progressive"
    dictionary_type = Dictionary.PROGRESSIVE_TYPE
    dtype_search_param = '3'
    dname_search_param = '2na'

    def __init__(self):
        pass

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
            english_def = ""
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
                    jap_sent = m[0].decode("utf8")
                    eng_sent = m[1].decode("utf8")
                    example_sentences.append(ExampleSentence(jap_sent, eng_sent))

            definitions.append(Definition(english_def.decode("utf8"), example_sentences, None))

        return definitions

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

    """
    for one, two in words:
        main(one, two)
        print
        """

    """
    one = words[0]
    result = NewCenturyDictionary().lookup(one[0], one[1])
    print(result)
    """

    daijirin_dic = DaijirinDictionary()
    daijisen_dic = DaijisenDictionary()
    new_century_dic = NewCenturyDictionary()
    progressive_dic = ProgressiveDictionary()

    """
    one = words[1]
    for d in [daijirin_dic, daijisen_dic, new_century_dic, progressive_dic]:
        print(d.lookup(one[0], one[1]))
        print
        """

    for word in words:
        for d in [daijirin_dic, daijisen_dic, new_century_dic, progressive_dic]:
            print(d.lookup(word[0], word[1]).to_jsonable())
            print
        print

    """
    daijirin_dic = DaijirinDictionary()
    daijisen_dic = DaijisenDictionary()
    new_century_dic = NewCenturyDictionary()
    progressive_dic = ProgressiveDictionary()
    """

    """
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
            print_all_defs(result.defs)
            print
            """

