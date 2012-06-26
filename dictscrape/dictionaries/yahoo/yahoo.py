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

from ..dictionary import Dictionary

class YahooDictionary(Dictionary):
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
        html = re.sub(u'(<img src="%s([0-9a-z]+).gif" align="abs(?:bottom|middle)" border="0">)'
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

