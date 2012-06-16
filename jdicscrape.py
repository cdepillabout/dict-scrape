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
        self._jap_sentence = jap_sentence
        self._eng_trans = eng_trans

        self._definition = None

    @property
    def jap_sentence(self):
        """Return the Japanese sentence."""
        return self._jap_sentence

    @property
    def eng_trans(self):
        """Return the English sentence."""
        return self._eng_trans

    def set_definition(self, definition):
        """Set the Definition that this ExampleSentence belongs to."""
        self._definition = definition

    @property
    def definition(self):
        """Return the Definition that this ExampleSentence belongs to."""
        return self._definition

    @property
    def result(self):
        """Return the Result that this ExampleSentence belongs to."""
        return self.definition.result

    def __unicode__(self):
        result_string = u"\n      - %s" % self._jap_sentence
        if self._eng_trans:
            result_string += u"\n        %s" % self._eng_trans
        return result_string

    def __str__(self):
        return unicode(self).encode("utf8")

    def __eq__(self, other):
        return (isinstance(other, self.__class__) and
                self.jap_sentence == other.jap_sentence and
                self.eng_trans == other.eng_trans)

    def to_jsonable(self):
        return {'jap_sentence': self.jap_sentence, 'eng_trans': self.eng_trans}

    @classmethod
    def from_jsonable(cls, jsonable):
        return cls(jsonable['jap_sentence'], jsonable['eng_trans'])

class DefinitionPart(object):
    """
    A part of a definition.  This is a part of a definition that makes up a whole definition.

    For instance, in the definition "あることをするよう無理に要求すること。むりじい。", there
    would be two definition parts.
    1) あることをするよう無理に要求すること
    2) むりじい
    """
    def __init__(self, part):
        """
        item is a string corresponding to a part of a definition.
        """
        if type(part) is not type(unicode()):
            raise UnicodeError, "item should be a unicode string"
        self._part = part
        self._definition = None

    @property
    def part(self):
        """Return the part."""
        return self._part

    def set_definition(self, definition):
        """Set the Definition that this DefinitionPart belongs to."""
        self._definition = definition

    @property
    def definition(self):
        """Return the Definition that this DefinitionPart belongs to."""
        return self._definition

    @property
    def result(self):
        """Return the Result that this DefinitionPart belongs to."""
        return self.definition.result

    def __unicode__(self):
        result_string = u"%s" % self.part
        return result_string

    def __str__(self):
        return unicode(self).encode("utf8")

    def __eq__(self, other):
        return (isinstance(other, self.__class__) and
                self.part == other.part)

    def to_jsonable(self):
        return self.part

    @classmethod
    def from_jsonable(cls, jsonable):
        return cls(jsonable)

class Definition(object):
    """
    Contains the defintion from a dictionary along with example sentences.
    """
    def __init__(self, parts, example_sentences):
        """
        parts is a list of DefinitionPart objects from a dictionary in either
        Japanese or English.
        example_sentences is a lists of ExampleSentence objects.
        """
        if parts:
            self._parts = parts
            for p in self._parts:
                if p.definition is not None:
                    raise Exception(u'part "%s" already has def object defined' %
                            unicode(p))
                p.set_definition(self)
        else:
            self._parts = []

        if example_sentences:
            self._example_sentences = example_sentences
            for e in self._example_sentences:
                if e.definition is not None:
                    raise Exception(u'example sentence "%s" already has def object defined' %
                            unicode(e))
                e.set_definition(self)
        else:
            self._example_sentences = []

        self._result = None

    @property
    def parts(self):
        """Return definition parts."""
        return self._parts

    @property
    def example_sentences(self):
        """Return a list of example sentences in the form of ExampleSentence objects."""
        return self._example_sentences

    def set_result(self, result):
        """Set the Result that this Definition belongs to."""
        self._result = result

    @property
    def result(self):
        """Return the Result that this Definition belongs to."""
        return self._result

    def pretty_definition(self):
        """Pretty print the definition parts."""
        if self._parts:
            result_string = u'\n＊ '
            for p in self.parts:
                result_string += p.part + u'。'
        else:
            result_string = u"\nNO DEFINITION AVAILABLE"
        return result_string

    def __unicode__(self):
        result_string = self.pretty_definition()
        for e in self._example_sentences:
            result_string += unicode(e)
        return result_string

    def __str__(self):
        return unicode(self).encode("utf8")

    def __eq__(self, other):
        return (isinstance(other, self.__class__) and
                self.parts == other.parts and
                self.example_sentences == other.example_sentences)

    def to_jsonable(self):
        parts = []
        for p in self.parts:
            parts.append(p.to_jsonable())
        ex_sentences = []
        for e in self.example_sentences:
            ex_sentences.append(e.to_jsonable())
        return {"parts": parts, "example_sentences": ex_sentences}

    @classmethod
    def from_jsonable(cls, jsonable):
        parts = []
        for p in jsonable["parts"]:
            parts.append(DefinitionPart.from_jsonable(p))
        ex_sentences = []
        for e in jsonable["example_sentences"]:
            ex_sentences.append(ExampleSentence.from_jsonable(e))
        return cls(parts, ex_sentences)

class Result(object):
    """
    This is an object representing the result of a dictionary lookup.
    """
    def __init__(self, dic, original_kanji, original_kana, url,
            kanji=None, kana=None, accent=None, defs=[]):
        """
        dic is the dictionary this result came from.
        original_kanji/kana is the kanji/kana that we searched for in the
        dictionary.
        url is the url that we searched on.
        kanji is a string with the kanji from the result. This may be the same
        as kana.
        kana is a string with the kana from the result.
        accent is the accent marking.  This may be None.
        defs is a list of Definition objects for the definitions
        contained in the dictionary.
        """
        assert(isinstance(dic, Dictionary))
        if type(original_kanji) is not type(unicode()):
            raise UnicodeError, "original_kanji should be a unicode string"
        if type(original_kana) is not type(unicode()):
            raise UnicodeError, "original_kana should be a unicode string"
        if type(kanji) is not type(unicode()) and kanji is not None:
            raise UnicodeError, "kanji should be a unicode string"
        if type(kana) is not type(unicode()) and kana is not None:
            raise UnicodeError, "kana should be a unicode string"
        self._dic = dic
        self._original_kanji = original_kanji
        self._original_kana = original_kana
        self._url = url
        self._kanji = kanji
        self._kana = kana
        self._accent = accent
        if defs:
            self._defs = defs
            for d in self._defs:
                if d.result is not None:
                    raise Exception(u'def "%s" already has result object defined' % unicode(d))
                d.set_result(self)
        else:
            self._defs = []

    @property
    def dic(self):
        """Return the dic that this result came from."""
        return self._dic

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

    def __eq__(self, other):
        return (isinstance(other, self.__class__) and
                self.original_kanji == other.original_kanji and
                self.original_kana == other.original_kana and
                self.url == other.url and
                self.kanji == other.kanji and
                self.kana == other.kana and
                self.accent == other.accent and
                self.defs == other.defs)

    def to_jsonable(self):
        dfs = []
        for d in self.defs:
            dfs.append(d.to_jsonable())
        return {"original_kanji": self.original_kanji, "original_kana": self.original_kana,
                "url": self.url, "result_kanji": self.kanji, "result_kana": self.kana,
                "accent": self.accent, "defs": dfs}

    @classmethod
    def from_jsonable(cls, dictionary, jsonable):
        dfs = []
        for d in jsonable["defs"]:
            dfs.append(Definition.from_jsonable(d))
        return cls(dictionary, jsonable["original_kanji"], jsonable["original_kana"],
                jsonable["url"], jsonable["result_kanji"], jsonable["result_kana"],
                jsonable["accent"], dfs)

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

    def lookup(self, word_kanji, word_kana, html=None):
        """
        Lookup a word in a dictionary.  word_kanji is a string for the kanji
        you want to lookup, and word_kana is the same but for the kana. html is
        the source of the page we will parse to lookup the defintion. If html
        is None, then we will fetch the page from the internet.  Returns a
        Definition object or None if no result could be found.
        """
        tree = self.__create_page_tree(word_kanji, word_kana, html)

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
            return Result(self, word_kanji, word_kana, url)

        # make sure this is the new century and not the progressive definition
        if self.dic_type == Dictionary.NEW_CENTURY_TYPE:
            if u'<span class="dic-zero">ニューセンチュリー和英辞典</span>' in result:
                #print("NO DEFINITION FROM NEW CENTURY")
                return Result(self, word_kanji, word_kana, url)

        # make sure this is the Daijisen and not the Daijirin definition
        if self.dic_type == Dictionary.DAIJISEN_TYPE:
            if u'<span class="dic-zero">大辞泉</span>' in result:
                #print("NO DEFINITION FROM NEW CENTURY")
                return Result(self, word_kanji, word_kana, url)

        kanji, kana, accent = self.parse_heading(tree)
        defs_sentences = self.parse_definition(tree)
        return Result(self, word_kanji, word_kana, url, kanji, kana, accent, defs_sentences)

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

    def __create_page_tree(self, word_kanji, word_kana, html=None):
        """
        Fetches a page from the internet and parses the page with
        etree.parse(StringIO(page_string), etree.HTMLParser()). If html is not
        None, then it is used as the html source.  It is not fetched from the
        internet.  Returns the parsed tree.
        """
        if html:
            page_string = html
        else:
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

    def split_def_parts(self, definition_string, split_characters=u'。'):
        """
        Split a definition into definition parts.
        definition_string is just a string for the definition.
        split_characters is either a list or a string.  If a string,
        then it is used as a character to split on.  If it is a list,
        then each character in the list is used as a split item.
        """
        assert(isinstance(definition_string, unicode))
        if isinstance(split_characters, list):
            pattern = '|'.join(map(re.escape, split_characters))
            splits = re.split(pattern, definition_string)
        else:
            splits = definition_string.split(split_characters)
        parts = []
        for s in splits:
            if s:
                s = s.strip()
                # if the beginning of a definition part start with 'また、', then
                # rip off the 'また'
                if s.startswith(u'また、'):
                    s = s[3:]
                parts.append(DefinitionPart(s))
        return parts

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

            text_def = defi.xpath(u'tr/td')[1]
            result = etree.tostring(text_def, pretty_print=False, method="html",
                    encoding='unicode')
            result = re.sub(u'^<td>', u'', result)
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

                # this checks if there is a 補説 at the top of the file.  We don't want this.
                result = re.sub(u'<b>〔補説〕</b> (.*?)<br>', u'', result)

                result = re.sub(u'^<td>', u'', result)
                result = re.sub(u'<br></td>$', u'', result)
                result = result.strip()
                def_parts = self.split_def_parts(result)
                jap_defs.append(Definition(def_parts, None))

        return jap_defs

class DaijisenDictionary(DaijirinDictionary):
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
        # example sentences
        if def_parts[-1].part.startswith(u'「'):
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

            # remove the </br>s and everything after them
            result = re.sub(u'<br>.*$', u'', result)
            result = result.strip()
            result = self.clean_def_string(result)
            jap_defs.append(self.create_def(result))

        return jap_defs

class NewCenturyDictionary(DaijirinDictionary):
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
        """
        # remove things in brackets and parenthesis
        def_string = re.sub(u'【.*?】', u'', def_string)
        def_string = re.sub(u'〈.*?〉', u'', def_string)
        def_string = re.sub(u'（.*?）', u'', def_string)
        # remove bold
        def_string = def_string.replace(u'<b>', u'')
        def_string = def_string.replace(u'</b>', u'')

        # strip whitespace
        def_string = def_string.strip()

        # remove trailing period
        if def_string[-1] == u'.':
            def_string = def_string[:-1]

        # split up the definition parts, breaking on ';'
        def_parts = self.split_def_parts(def_string, split_characters=[u';', u','])
        return def_parts

    def create_example_sentences(self, example_sentence_strings):
        """
        This creates example sentence objects.  The input is a
        list of [japanese_example_sentence, english_translation] tuples.
        This returns a list of ExampleSentence objects.
        """
        example_sentences = []

        for jap_sentence, eng_trans in example_sentence_strings:
            # remove links
            eng_trans = re.sub(u'<a.*?>', u'', eng_trans)
            eng_trans = re.sub(u'</a>', u'', eng_trans)

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

            # for japanese sentences, we want to change "." to "。"
            jap_sentence = jap_sentence.replace(u'.', u'。')


            example_sentences.append(ExampleSentence(jap_sentence, eng_trans))

        return example_sentences


    def parse_definition(self, tree):
        def_elems = tree.xpath("//table[@class='d-detail']/tr/td")[0]
        result = etree.tostring(def_elems, pretty_print=False, method="html",
                encoding='unicode')

        # some replacements to make our lives easier
        result = result.replace(u'<img src="http://i.yimg.jp/images/dic/ss/gnc/g111a.gif" align="absbottom" border="0">', u'〈')
        result = result.replace(u'<img src="http://i.yimg.jp/images/dic/ss/gnc/g111b.gif" align="absbottom" border="0">', u'〉')
        result = result.replace(u'<img src="http://i.yimg.jp/images/dic/ss/gnc/g111c.gif" align="absbottom" border="0">', u'⁝')
        result = result.replace(u'<img src="http://i.yimg.jp/images/dic/ss/gnc/g111d.gif" align="absbottom" border="0">', u'＊')
        result = result.replace(u'<img src="http://i.yimg.jp/images/dic/ss/gnc/g111e.gif" align="absbottom" border="0">', u'（同）')
        result = result.replace(u'<img src="http://i.yimg.jp/images/dic/ss/gnc/g111f.gif" align="absbottom" border="0">', u'Æ')

        result = result.replace(u'<img src="http://i.yimg.jp/images/dic/ss/gnc/g1202.gif" align="absbottom" border="0">', u'c')
        result = result.replace(u'<img src="http://i.yimg.jp/images/dic/ss/gnc/g1203.gif" align="absbottom" border="0">', u'c')
        result = result.replace(u'<img src="http://i.yimg.jp/images/dic/ss/gnc/g1204.gif" align="absbottom" border="0">', u'c')
        result = result.replace(u'<img src="http://i.yimg.jp/images/dic/ss/gnc/g1205.gif" align="absbottom" border="0">', u'd')
        result = result.replace(u'<img src="http://i.yimg.jp/images/dic/ss/gnc/g1206.gif" align="absbottom" border="0">', u'e')
        result = result.replace(u'<img src="http://i.yimg.jp/images/dic/ss/gnc/g1207.gif" align="absbottom" border="0">', u'e')
        result = result.replace(u'<img src="http://i.yimg.jp/images/dic/ss/gnc/g1208.gif" align="absbottom" border="0">', u'e')
        result = result.replace(u'<img src="http://i.yimg.jp/images/dic/ss/gnc/g1209.gif" align="absbottom" border="0">', u'e')
        result = result.replace(u'<img src="http://i.yimg.jp/images/dic/ss/gnc/g1210.gif" align="absbottom" border="0">', u'g')
        result = result.replace(u'<img src="http://i.yimg.jp/images/dic/ss/gnc/g1211.gif" align="absbottom" border="0">', u'g')
        result = result.replace(u'<img src="http://i.yimg.jp/images/dic/ss/gnc/g1212.gif" align="absbottom" border="0">', u'h')
        result = result.replace(u'<img src="http://i.yimg.jp/images/dic/ss/gnc/g1213.gif" align="absbottom" border="0">', u'h')
        result = result.replace(u'<img src="http://i.yimg.jp/images/dic/ss/gnc/g1214.gif" align="absbottom" border="0">', u'h')
        result = result.replace(u'<img src="http://i.yimg.jp/images/dic/ss/gnc/g1215.gif" align="absbottom" border="0">', u'i')
        result = result.replace(u'<img src="http://i.yimg.jp/images/dic/ss/gnc/g1216.gif" align="absbottom" border="0">', u'i')
        result = result.replace(u'<img src="http://i.yimg.jp/images/dic/ss/gnc/g1217.gif" align="absbottom" border="0">', u'i')
        result = result.replace(u'<img src="http://i.yimg.jp/images/dic/ss/gnc/g1218.gif" align="absbottom" border="0">', u'i')
        result = result.replace(u'<img src="http://i.yimg.jp/images/dic/ss/gnc/g1219.gif" align="absbottom" border="0">', u'i')
        result = result.replace(u'<img src="http://i.yimg.jp/images/dic/ss/gnc/g1220.gif" align="absbottom" border="0">', u'o')
        result = result.replace(u'<img src="http://i.yimg.jp/images/dic/ss/gnc/g1221.gif" align="absbottom" border="0">', u'o')
        result = result.replace(u'<img src="http://i.yimg.jp/images/dic/ss/gnc/g1222.gif" align="absbottom" border="0">', u'o')
        result = result.replace(u'<img src="http://i.yimg.jp/images/dic/ss/gnc/g1223.gif" align="absbottom" border="0">', u'o')
        result = result.replace(u'<img src="http://i.yimg.jp/images/dic/ss/gnc/g1224.gif" align="absbottom" border="0">', u'o')
        result = result.replace(u'<img src="http://i.yimg.jp/images/dic/ss/gnc/g1225.gif" align="absbottom" border="0">', u'p')
        result = result.replace(u'<img src="http://i.yimg.jp/images/dic/ss/gnc/g1226.gif" align="absbottom" border="0">', u'P')
        result = result.replace(u'<img src="http://i.yimg.jp/images/dic/ss/gnc/g1227.gif" align="absbottom" border="0">', u'q')
        result = result.replace(u'<img src="http://i.yimg.jp/images/dic/ss/gnc/g1228.gif" align="absbottom" border="0">', u'r')
        result = result.replace(u'<img src="http://i.yimg.jp/images/dic/ss/gnc/g1229.gif" align="absbottom" border="0">', u'r')
        result = result.replace(u'<img src="http://i.yimg.jp/images/dic/ss/gnc/g1230.gif" align="absbottom" border="0">', u'u')
        result = result.replace(u'<img src="http://i.yimg.jp/images/dic/ss/gnc/g1231.gif" align="absbottom" border="0">', u'u')
        result = result.replace(u'<img src="http://i.yimg.jp/images/dic/ss/gnc/g1232.gif" align="absbottom" border="0">', u'u')
        result = result.replace(u'<img src="http://i.yimg.jp/images/dic/ss/gnc/g1233.gif" align="absbottom" border="0">', u'U')
        result = result.replace(u'<img src="http://i.yimg.jp/images/dic/ss/gnc/g1234.gif" align="absbottom" border="0">', u'w')
        result = result.replace(u'<img src="http://i.yimg.jp/images/dic/ss/gnc/g1235.gif" align="absbottom" border="0">', u'w')
        result = result.replace(u'<img src="http://i.yimg.jp/images/dic/ss/gnc/g1236.gif" align="absbottom" border="0">', u'x')
        result = result.replace(u'<img src="http://i.yimg.jp/images/dic/ss/gnc/g1237.gif" align="absbottom" border="0">', u'y')
        result = result.replace(u'<img src="http://i.yimg.jp/images/dic/ss/gnc/g1238.gif" align="absbottom" border="0">', u'y')
        result = result.replace(u'<img src="http://i.yimg.jp/images/dic/ss/gnc/g1238.gif" align="absbottom" border="0">', u'y')

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
            english_def = None
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

class ProgressiveDictionary(DaijirinDictionary):
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
        matches = re.search(u'^<td>\n<b>1</b> 〔', result)
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

def main(word_kanji, word_kana):
    check_daijirin(word_kanji, word_kana)
    print
    check_daijisen(word_kanji, word_kana)
    print
    check_new_century(word_kanji, word_kana)
    print
    check_progressive(word_kanji, word_kana)

if __name__ == '__main__':

    daijirin_dic = DaijirinDictionary()
    daijisen_dic = DaijisenDictionary()
    new_century_dic = NewCenturyDictionary()
    progressive_dic = ProgressiveDictionary()

    if len(sys.argv) == 3:
        kanji = sys.argv[1].decode("utf8")
        kana = sys.argv[2].decode("utf8")
        for d in [daijirin_dic, daijisen_dic, new_century_dic, progressive_dic]:
            print("\t\t\t\t%s\n%s\n\n" % (d.short_name, d.lookup(kanji, kana)))
        sys.exit(1)


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


    one = words[0]
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

