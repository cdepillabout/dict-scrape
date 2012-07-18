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


from ..dictionary import Dictionary
from .epwing import EpwingDictionary

from ...example_sentence import ExampleSentence
from ...definition import Definition

class KenkyuushaDictionary(EpwingDictionary):
    """
    Kenkyuusha Epwing Dictionary.
    """

    long_dictionary_name = u"研究社 新和英大辞典 第５版"
    short_dictionary_name = "Kenkyuusha"
    dictionary_type = Dictionary.EPWING_KENKYUUSHA_TYPE

