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

from ..definition import DefinitionPart

class Dictionary(object):
    """
    An object representing an online dictionary in which to lookup
    definitions.

    TODO: Many of these functions will probably have to be added to the
    YahooDictionary object.
    """

    #These are constants for the type of a dictionary.
    YAHOO_DAIJIRIN_TYPE = 0
    YAHOO_DAIJISEN_TYPE = 1
    YAHOO_NEW_CENTURY_TYPE = 2
    YAHOO_PROGRESSIVE_TYPE = 3
    EPWING_KENKYUUSHA_TYPE = 4

    def __init__(self):
        pass

    def lookup(self, word_kanji, word_kana, html=None):
        """
        Lookup a word in a dictionary.

        word_kanji (unicode): the kanji you want to lookup
        word_kana (unicode): the kanji for the word you want to lookup
        html (unicode): the source of the page we will parse to lookup the defintion.
        If html is None, then we will fetch the page from the dictionary (possible the
        internet).

        Returns a Result object.  If no result could be found, then it returns
        a Result object with everything blank ("").
        """
        raise NotImplementedError, "This needs to be overrode in a child class."

    def split_def_parts(self, definition_string, split_characters=u'。'):
        """
        Split a definition into definition parts.

        definition_string (unicode):  the definition
        split_characters (list or unicode): If a string, then it is used as
            the character to split on.  If it is a list,
            then each character in the list is used as a split item.

        Returns list of DefinitionPart objects.
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
