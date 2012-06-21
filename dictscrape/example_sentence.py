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
