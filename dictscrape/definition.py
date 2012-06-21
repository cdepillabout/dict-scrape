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

"""
This contains the DefinitionPart and Definition objects.  These are
used by the Result object to represent definitions returned from
a Dictionary object.
"""

from .example_sentence import ExampleSentence

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
        part (unicode): part of a definition
        """
        if type(part) is not type(unicode()):
            raise UnicodeError, "item should be a unicode string"
        self._part = part
        self._definition = None

    @property
    def part(self):
        """Return the definition part."""
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
        """Return a jsonable object that represents this DefinitionPart class."""
        return self.part

    @classmethod
    def from_jsonable(cls, jsonable):
        """Return a DefinitionPart object based on the jsonable object."""
        return cls(jsonable)

class Definition(object):
    """
    Contains the defintion parts from a dictionary along with example sentences.
    """
    def __init__(self, parts, example_sentences):
        """
        parts (list of DefinitionPart objects): parts of the definition
        example_sentences (list of ExampleSentence objects): example sentences
        that go with this definition.
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
        """Return a jsonable object that represents this Definition class."""
        parts = []
        for p in self.parts:
            parts.append(p.to_jsonable())
        ex_sentences = []
        for e in self.example_sentences:
            ex_sentences.append(e.to_jsonable())
        return {"parts": parts, "example_sentences": ex_sentences}

    @classmethod
    def from_jsonable(cls, jsonable):
        """Return a DefinitionPart object based on the jsonable object."""
        parts = []
        for p in jsonable["parts"]:
            parts.append(DefinitionPart.from_jsonable(p))
        ex_sentences = []
        for e in jsonable["example_sentences"]:
            ex_sentences.append(ExampleSentence.from_jsonable(e))
        return cls(parts, ex_sentences)
