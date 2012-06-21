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

"""
Tests for comparing parsing for dictionary entries.
"""

import json
import os
import subprocess
import sys
import textwrap
import traceback

# we need stuff from the directory above us
PROJECT_ROOT = os.path.dirname(__file__)
sys.path.append(os.path.join(PROJECT_ROOT, ".."))

from dictscrape import Result
import test as manage_words

ERRORS = []

def print_helper(object_a, object_b, object_a_desc, object_b_desc, member_string):
    value_a = object_a.__getattribute__(member_string)
    value_b = object_b.__getattribute__(member_string)

    if hasattr(object_a, 'dic'):
        dic_name_a = object_a.dic.short_name
    else:
        dic_name_a = object_a.result.dic.short_name

    if hasattr(object_b, 'dic'):
        dic_name_b = object_b.dic.short_name
    else:
        dic_name_b = object_b.result.dic.short_name

    # print if different
    if value_a != value_b:
        print(u'\n\t%s: "%s" attribute -- %s' %
                (object_a_desc, member_string, value_a))
        print(u'\t%s: "%s" attribute -- %s' %
                (object_b_desc, member_string, value_b))
        print_separator()

def pretty_format(obj, tab_amount=0):
    indent = ""
    for i in range(tab_amount):
        indent += "\t"

    wrapper = textwrap.TextWrapper(initial_indent=indent, subsequent_indent=indent, width=35)
    return wrapper.fill(u'%s' % obj)

def print_separator():
    print(u'--------------------------------------------')

def print_differences_example_sentence(exsent_a, exsent_b, exsent_a_string, exsent_b_string):
    """
    Prints the differences to between two example sentences.
    """
    print_helper(exsent_a, exsent_b, exsent_a_string, exsent_b_string, "jap_sentence")
    print_helper(exsent_a, exsent_b, exsent_a_string, exsent_b_string, "eng_trans")

def print_differences_definition_part(part_a, part_b, part_a_string, part_b_string):
    """
    Prints the differences to between two definition parts.
    """
    print_helper(part_a, part_b, part_a_string, part_b_string, "part")

def print_differences_definition(def_a, def_b, def_a_string, def_b_string):
    """
    Prints the differences to between two definitions.
    """
    parts_a = def_a.parts
    parts_b = def_b.parts

    if len(parts_a) != len(parts_b):
        print(u'\n\tnumber of parts for definition is different')
        print(u'\n\t\tparts from %s: (%s)' % (def_a_string, len(parts_a)))
        for p in parts_a:
            print(pretty_format(p, tab_amount=2))
        print(u'\n\t\tparts from %s: (%s)' % (def_b_string, len(parts_b)))
        for p in parts_b:
            print(pretty_format(p, tab_amount=2))
        print_separator()
    else:
        for part_a, part_b in zip(parts_a, parts_b):
            part_a_string = def_a_string + ".part"
            part_b_string = def_b_string + ".part"
            print_differences_definition_part(part_a, part_b, part_a_string, part_b_string)

    exs_a = def_a.example_sentences
    exs_b = def_b.example_sentences

    if len(exs_a) != len(exs_b):
        print(u'\n\tnumber of example sentences for definition is different')
        print(u'\tdefinition: %s' % def_a.pretty_definition().strip())
        print(u'\n\t\texample sentences from %s: (%s)' % (def_a_string, len(exs_a)))
        for e in exs_a:
            print(pretty_format(e, tab_amount=2))
        print(u'\n\t\texample sentences from %s: (%s)' % (def_b_string, len(exs_b)))
        for e in exs_b:
            print(pretty_format(e, tab_amount=2))
        print_separator()
    else:
        for ex_a, ex_b in zip(exs_a, exs_b):
            ex_a_string = def_a_string + ".example_sentence"
            ex_b_string = def_b_string + ".example_sentence"
            print_differences_example_sentence(ex_a, ex_b, ex_a_string, ex_b_string)

def print_differences_result(result_a, result_b, result_a_string, result_b_string):
    """
    Prints the differences to between two results.
    """
    print_helper(result_a, result_b, result_a_string, result_b_string, "original_kanji")
    print_helper(result_a, result_b, result_a_string, result_b_string, "original_kana")
    print_helper(result_a, result_b, result_a_string, result_b_string, "url")
    print_helper(result_a, result_b, result_a_string, result_b_string, "kanji")
    print_helper(result_a, result_b, result_a_string, result_b_string, "kana")
    print_helper(result_a, result_b, result_a_string, result_b_string, "accent")

    defs_a = result_a.defs
    defs_b = result_b.defs

    if len(defs_a) != len(defs_b):
        print(u'\n\tnumber of definitions is different')
        print(u'\tdefs from %s: (%s)' % (result_a_string, len(defs_a)))
        for d in defs_a:
            print(pretty_format(d, tab_amount=2))
        print(u'\tdefs from %s: (%s)' % (result_b_string, len(defs_b)))
        for d in defs_b:
            print(pretty_format(d, tab_amount=2))
        print_separator()
    else:
        for def_a, def_b in zip(defs_a, defs_b):
            def_a_string = result_a_string + ".definition"
            def_b_string = result_b_string + ".definition"
            print_differences_definition(def_a, def_b, def_a_string, def_b_string)

def checkword(dictionary, kanji, kana):
    """
    dictionary (Dictionary): the dictionary we want to check in
    kanji (unicode): the kanji we want to check
    kana (unicode): the kana we want to check
    """
    html = manage_words.get_html_for_word(dictionary, kana, kanji)
    json_object = manage_words.get_json_for_word(dictionary, kana, kanji)

    html_parse_result = dictionary.lookup(kanji, kana, html)
    json_result = Result.from_jsonable(dictionary, json_object)

    if (json_result != html_parse_result):
        print_differences_result(json_result, html_parse_result, "JSON result", "HTML result")
        assert(json_result == html_parse_result)

@manage_words.no_null_dictionaries
def test_words(kanji=None, kana=None, dictionaries=manage_words.get_dics()):
    """
    Test our words to make sure everything parses correct.  This tries to parse
    an hmlt page for a word and compares its output to that of the json file
    from disk.  If something doesn't match, then we have an error.

    This is used to make sure that changes made to the Dictionary's parsing
    functions don't make some other word/definition mess up.  For instance,
    if we are trying to fix something where we need to take out the 動 kanji,
    we may make an error and remove all 動 from the entire definition.  These
    tests would catch this error.

    kanji (unicode): the kanji we want to check
    kana (unicode): the kana we want to check
    dictionaries (list of Dictionary objects): the dictionaries we want to check in

    kanji and kana should correspond to a word in our words.db.  If kanji and kana
    are None, then we just test all the words.

    Prints errors if there are any.
    """
    if kanji is None and kana is None:
        words = manage_words.get_words_from_wordsdb()
    else:
        words = [[kana, kanji]]

    for kana, kanji in words:
        for dic in dictionaries:
            description = '%s (%s) in %s' % (kana, kanji, dic.short_name)
            sys.stdout.write(u'check %s... ' % description)
            try:
                checkword(dic, kanji, kana)
                print("PASS")
            except:
                tb = traceback.format_exc().decode('utf8')
                ERRORS.append([description, tb])
                print("FAIL")
    if ERRORS:
        print("\n\n%d ERRORS:\n" % len(ERRORS))
        for description, tb in ERRORS:
            print("%s\n============================\n%s\n" % (description, tb))


if __name__ == '__main__':
    test_words()
