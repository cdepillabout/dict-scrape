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
import urllib

from lxml import etree
from StringIO import StringIO

from ..dictionary import Dictionary
from ...result import Result

class YahooDictionary(Dictionary):

    def lookup(self, word_kanji, word_kana, html=None):
        """
        Lookup a word in a dictionary.

        word_kanji (unicode): the kanji you want to lookup
        word_kana (unicode): the kanji for the word you want to lookup
        html (unicode): the source of the page we will parse to lookup the defintion.
        If html is None, then we will fetch the page from the internet.

        Returns a Result object.  If no result could be found, then it returns
        a Result object with everything blank ("").
        """
        # possibly download the html and create a tree for the page for the
        # word we are looking up.
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
        if self.dic_type == Dictionary.YAHOO_DAIJISEN_TYPE:
            if u'<span class="dic-zero">大辞泉</span>' in result:
                return Result(self, word_kanji, word_kana, url)

        # make sure this is the Daijirin and not the Daijisen definition
        if self.dic_type == Dictionary.YAHOO_DAIJIRIN_TYPE:
            if u'<span class="dic-zero">大辞林</span>' in result:
                return Result(self, word_kanji, word_kana, url)

        # make sure this is the new century and not the progressive definition
        if self.dic_type == Dictionary.YAHOO_NEW_CENTURY_TYPE:
            if u'<span class="dic-zero">ニューセンチュリー和英辞典</span>' in result:
                return Result(self, word_kanji, word_kana, url)

        # make sure this is the progressive and not the new century definition
        if self.dic_type == Dictionary.YAHOO_PROGRESSIVE_TYPE:
            if u'<span class="dic-zero">プログレッシブ和英中辞典</span>' in result:
                return Result(self, word_kanji, word_kana, url)

        kanji, kana, accent = self.parse_heading(tree)
        defs = self.parse_definition(tree)
        return Result(self, word_kanji, word_kana, url, kanji, kana, accent, defs)

    def parse_heading(self, tree):
        div = tree.xpath("//div[@class='title-keyword']")[0]
        heading = div.getchildren()[0]
        children = heading.getchildren()

        result_accent = ""
        if children:
            for i, c in enumerate(children):
                if c.tag == 'sub':
                    result_accent += heading.getchildren()[i].text

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
        """
        Parses the main definition of the dictionary page and returns a
        a list of Definition objects.
        """
        raise NotImplementedError, "This needs to be overrode in a child class."

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
        Fetches a parses the page for the word we are looking up with
        etree.parse(StringIO(page_string), etree.HTMLParser()).
        If html is None, then the page is fetched from the internet.
        If html is not None, then it is used as the html source.
        It is not fetched from the internet.

        word_kanji (unicode): the kanji you want to lookup
        word_kana (unicode): the kanji for the word you want to lookup
        html (unicode): the source of the page we will parse to lookup the defintion.
        If html is None, then we will fetch the page from the internet.

        Returns the parsed tree.
        """
        if html:
            page_string = html
        else:
            page_string = self._fetch_page(word_kanji, word_kana)

        parser = etree.HTMLParser()
        tree = etree.parse(StringIO(page_string), parser)
        return tree

    def replace_gaiji(self, html):
        """
        Replace gaiji in html.
        """
        def helper(string, gaiji_code, real_character):
            return re.sub(u'<img src="%s%s.gif" align="abs(bottom|middle)" border="0">' %
                    (self.gaiji_url, gaiji_code), real_character, string)

        # replace all gaiji characters that have been specified
        for gaiji_code, real_char in self.gaiji:
            html = helper(html, gaiji_code, real_char)

        # replace all non-specified characters with something that is
        # easy to see and replace by hand
        html = re.sub(u'(<img src="%s([0-9A-Za-z]+).gif" align="abs(?:bottom|middle)" border="0">)'
                % re.escape(self.gaiji_url), ur'＜\1:\2＞', html)

        return html

    @property
    def gaiji(self):
        """
        Return the gaiji for this dictionary.
        """
        raise NotImplementedError, "This needs to be overrode in a child class."

    @property
    def gaiji_url(self):
        """
        Return the gaiji base URL for this dictionary.
        """
        raise NotImplementedError, "This needs to be overrode in a child class."

