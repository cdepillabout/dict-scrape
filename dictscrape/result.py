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

from .definition import Definition

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
        #assert(isinstance(dic, Dictionary))
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
