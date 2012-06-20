# -*- coding: UTF-8 -*-

import re
import urllib

from lxml import etree
from StringIO import StringIO

from ..definition import DefinitionPart
from ..result import Result


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

        # return empty result if we can't find a definition
        if word_not_found_string in result or word_not_found_string_no_space in result:
            return Result(self, word_kanji, word_kana, url)

        # make sure this is the Daijisen and not the Daijirin definition
        if self.dic_type == Dictionary.DAIJISEN_TYPE:
            if u'<span class="dic-zero">大辞泉</span>' in result:
                return Result(self, word_kanji, word_kana, url)

        # make sure this is the Daijirin and not the Daijisen definition
        if self.dic_type == Dictionary.DAIJIRIN_TYPE:
            if u'<span class="dic-zero">大辞林</span>' in result:
                return Result(self, word_kanji, word_kana, url)

        # make sure this is the new century and not the progressive definition
        if self.dic_type == Dictionary.NEW_CENTURY_TYPE:
            if u'<span class="dic-zero">ニューセンチュリー和英辞典</span>' in result:
                return Result(self, word_kanji, word_kana, url)

        # make sure this is the progressive and not the new century definition
        if self.dic_type == Dictionary.PROGRESSIVE_TYPE:
            if u'<span class="dic-zero">プログレッシブ和英中辞典</span>' in result:
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
