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
A script for working with testing.

This script enables you do add words to the test database,
reparse words, and run all the tests.

Running partial tests of only some of the words is also possible.
"""

import argparse
import codecs
import json
import nose
import operator
import os
import os.path
import sys
import subprocess
import traceback


PROJECT_ROOT = os.path.dirname(__file__)
sys.path.append(os.path.join(PROJECT_ROOT, "testing"))

from dictscrape import DaijirinDictionary, DaijisenDictionary, \
        ProgressiveDictionary, NewCenturyDictionary, KenkyuushaDictionary, \
        ExampleSentence, DefinitionPart, Definition, Result

import test_jdicscrape_word_parsing

WORDS_DIR_REL_PATH = os.path.join("testing", "support", "words")
WORDS_DIR_ABS_PATH = os.path.abspath(
        os.path.join(os.path.dirname(__file__), WORDS_DIR_REL_PATH))

dics = [DaijirinDictionary(),
        DaijisenDictionary(),
        ProgressiveDictionary(),
        NewCenturyDictionary(),
        KenkyuushaDictionary(),]

def die(string):
    error_string = u'ERROR! %s' % string
    if __name__ == '__main__':
        print(error_string)
        sys.exit(1)
    else:
        raise Exception(error_string)

words_db_rel_path = os.path.join(WORDS_DIR_REL_PATH, "words.db")
words_db_abs_path = os.path.join(WORDS_DIR_ABS_PATH, "words.db")
if not (os.path.exists(words_db_abs_path)):
    die("words.db does not exist! Something is wrong!")

def get_dics():
    """
    Return a list of all our dictionary objects.
    """
    return dics

def no_null_dictionaries(f):
    """
    Decorator that looks through the function's kwargs and picks
    out the dictionary argument.  If it is not available, or None,
    it gets set to all of the dics we have available.  If the dictionary
    argument is not a list, then it gets changed into a list.
    """
    def func_with_dictionaries(*args, **kwargs):
        if "dictionaries" not in kwargs or not kwargs["dictionaries"]:
            kwargs["dictionaries"] = get_dics()
        if not isinstance(kwargs["dictionaries"], list):
            kwargs["dictionaries"] = [kwargs["dictionaries"]]
        f(*args, **kwargs)
    return func_with_dictionaries

def get_words_from_wordsdb():
    """Get all the words from the words.db."""
    words = []

    # read in current words
    with codecs.open(words_db_abs_path, 'r', 'utf8') as f:
        lines = f.read().split('\n')
    for l in lines:
        if l != '':
            kana, kanji = l.split()
            words.append(tuple([kana, kanji]))

    return words

def get_paths_for_word(dic, kana, kanji):
    """
    Returns the paths for the raw and json result files for the
    word.

    dic (Dictionary object): Dictionary to look in.
    kana/kanji (unicode): Word to look up.

    Returns a 6tuple of the raw filename, the json result file name,
    the absolute path to the raw file, the absolute path to the json
    result file, the relative path to the raw file, and the relative
    path to the json result file.
    """
    dirname, rel_path, abs_path = get_paths_for_dic(dic)

    raw_filename = u'%s_%s.raw' % (kana, kanji)
    json_filename = u'%s_%s.result.json' % (kana, kanji)

    # absolute paths to the two files we will use
    raw_file_abs_path = os.path.join(abs_path, raw_filename)
    json_file_abs_path = os.path.join(abs_path, json_filename)

    # relative paths to the two files we will use to print out
    raw_file_rel_path = os.path.join(rel_path, raw_filename)
    json_file_rel_path = os.path.join(rel_path, json_filename)

    return raw_filename, json_filename, raw_file_abs_path, \
            json_file_abs_path, raw_file_rel_path, json_file_rel_path

def get_paths_for_dic(dic):
    """
    Returns the relative and absolute paths for the folder for the
    raw files and result files for this dictionary.

    dic (Dictionary object): Dictionary to use

    Returns a 3tuple of the directory name, the relative path to the
    directory, and the absolute path to the directory.
    """
    dirname = dic.short_name
    rel_path = os.path.join(WORDS_DIR_REL_PATH, dic.short_name)
    abs_path = os.path.join(WORDS_DIR_ABS_PATH, dic.short_name)

    return dirname, rel_path, abs_path

def sanity_check():
    """Make sure our words.db and actual words that have been downloaded match up."""
    words = get_words_from_wordsdb()

    # TODO: make sure every word in words is unique
    for kana, kanji in words:
        existing_words = [word for word in words if word[0] == kana and word[1] == kanji]
        if len(existing_words) > 1:
            die("%s (%s) exists more than once in words.db" % (kanji, kana))

    # make sure there is a file for each of our words in each dictionary directory
    for dic in dics:
        dirname, rel_path, abs_path = get_paths_for_dic(dic)
        for kana, kanji in words:
            tup = get_paths_for_word(dic, kana, kanji)
            raw_filename = tup[0]
            json_filename = tup[1]
            raw_file_abs_path = tup[2]
            json_file_abs_path = tup[3]
            raw_file_rel_path = tup[4]
            json_file_rel_path = tup[5]

            if not os.path.exists(raw_file_abs_path):
                die(u'%s (%s) is in words.db, but "%s" does not exist.' %
                        (kanji, kana, raw_file_rel_path))

            if not os.path.exists(json_file_abs_path):
                die(u'%s (%s) is in words.db, but "%s" does not exist.' %
                        (kanji, kana, json_file_rel_path))

        for entry in os.listdir(abs_path):
            if isinstance(entry, str):
                entry = entry.decode('utf8')
            assert(isinstance(entry, unicode))
            entry_rel_path = os.path.join(rel_path, entry)
            try:
                # rip off the extension
                name = entry.split('.')[0]
                # get kanji and kana
                kana, kanji = name.split('_')
            except:
                die("Inappropriate file %s" % entry_rel_path)

            # make sure kanji and kana are in words.db
            existing_words = [word for word in words if word[0] == kana and word[1] == kanji]
            if len(existing_words) < 1:
                die(u'%s (%s) from %s does not exist in words.db' %
                        (kanji, kana, entry_rel_path))

def add_word_to_wordsdb(word_kana, word_kanji):
    """Update the words.db with word_kanji and word_kana."""
    words = get_words_from_wordsdb()

    # make sure our new word is not in words.db
    for word in words:
        if word_kana == word[0] and word_kanji == word[1]:
            die("%s (%s) already exists in words.db." % (word_kanji, word_kana))

    # add our new word
    words.append(tuple([word_kana, word_kanji]))

    # sort words
    words = sorted(words, key=operator.itemgetter(1,0))

    # write sorted word list words
    with codecs.open(words_db_abs_path, 'w', 'utf8') as f:
        for word in words:
            f.write(u'%s %s\n' % (word[0], word[1]))

def get_raw_for_word(dic, word_kana, word_kanji):
    """Return the raw file for the word."""
    _, _, raw_abs_path, _, raw_rel_path, _ = get_paths_for_word(dic, word_kana, word_kanji)

    # make sure raw file exists
    if not os.path.exists(raw_abs_path):
        die(u'raw file "%s" does not exist.' % raw_rel_path)

    with codecs.open(raw_abs_path, 'r', 'utf8') as f:
        return f.read()

def get_json_for_word(dic, word_kana, word_kanji):
    """Return the json result file for the word."""
    _, _, _, json_abs_path, _, json_rel_path = get_paths_for_word(
            dic, word_kana, word_kanji)

    # make sure json file exists
    if not os.path.exists(json_abs_path):
        die(u'JSON result file "%s" does not exist.' % json_rel_path)

    with open(json_abs_path, "r") as f:
        return json.load(f, encoding="utf8")

def __write_word_encoding_result(dic, word_kana, word_kanji):
    """
    Try to get the result of the encoding and write it so we have
    something to work with.  If we can't get it, then just error
    out and write a blank result.

    dic (Dictionary object): dictionary to use to get the page.
    word_kana/kanji (unicode): words in kana and kanji to parse result of.

    Writes DictionaryName/WORDKANA_WORDKANJI.result.json file.
    """
    _, _, raw_abs_path, json_abs_path, raw_rel_path, json_rel_path = get_paths_for_word(
            dic, word_kana, word_kanji)

    raw = get_raw_for_word(dic, word_kana, word_kanji)

    with codecs.open(json_abs_path, 'w', 'utf8') as f:
        try:
            result = dic.lookup(word_kanji, word_kana, raw)
            jsonable = result.to_jsonable()
            json.dump(jsonable, f, encoding='utf8', sort_keys=True,
                    indent=4, ensure_ascii=False)
            print(u'Wrote result file: %s' % json_rel_path)
        except:
            traceback.print_exc()
            print(u'Error occured when parsing %s (%s) in %s.' %
                    (word_kanji, word_kana, dic.short_name))
            print(u'Writing template file "%s".' % json_rel_path)
            print(u'You need to go in and edit the information manually.')

            url = dic._create_url(word_kanji, word_kana)
            example_sentence = ExampleSentence(
                    u'***JAPANESE SENTENCE***', u'***ENGLISH SENTENCE***')
            part1 = DefinitionPart(u'***PART 1***')
            part2 = DefinitionPart(u'***PART 2***')
            definition = Definition([part1, part2], [example_sentence])
            result = Result(dic, word_kanji, word_kana, url,
                    u'***KANJI***', u'***KANA***', u'', [definition])
            jsonable = result.to_jsonable()
            json.dump(jsonable, f, encoding='utf8', sort_keys=True,
                    indent=4, ensure_ascii=False)

@no_null_dictionaries
def fetch_raw_word(word_kana, word_kanji, dictionaries=get_dics(), assert_word_in_db=False):
    """
    Fetch the raw file from dictionary and save it to disk.

    dic (Dictionary object): dictionary to use to get the page.
    word_kana/kanji (unicode): words in kana and kanji to download.

    Writes DictionaryName/WORDKANA_WORDKANJI.raw file.
    """
    if assert_word_in_db:
        # make sure word is in words.db
        words = get_words_from_wordsdb()
        if (word_kana, word_kanji) not in words:
            die("%s (%s) does not exist in words.db" % (kanji, kana))

    for dic in dictionaries:
        _, _, raw_file_abs_path, _, raw_file_rel_path, _ = get_paths_for_word(
                dic, word_kana, word_kanji)

        page_string = dic.get_raw(word_kanji, word_kana)

        with open(raw_file_abs_path, 'w') as f:
            f.write(page_string.encode('utf8'))
            print(u'Wrote raw file: %s' % raw_file_rel_path)

@no_null_dictionaries
def fetch_raw_all(dictionaries=get_dics()):
    """
    Fetch all raw files for all words from dictionary and save them to disk.

    dictionaries (list of Dictionary objects): dictionaries to reparse
        in.
    """
    words = get_words_from_wordsdb()
    for kana, kanji in words:
        fetch_raw_word(kana, kanji, dictionaries=dictionaries)

def addword(word_kana, word_kanji):
    """
    Add words to be tested.  Download the raw files for a word and
    parse those files. Write the parsed json result files.  Add words
    to words.db

    word_kana/kanji (unicode): words in kana and kanji to add.
    """
    # make sure we get unicode words
    assert(type(word_kanji) == type(unicode()))
    assert(type(word_kana) == type(unicode()))

    add_word_to_wordsdb(word_kana, word_kanji)

    for dic in get_dics():
        _, _, abs_path = get_paths_for_dic(dic)
        if not os.path.isdir(abs_path):
            die(u'Directory "%s" does not exist.' % abs_path)

        tup = get_paths_for_word(dic, word_kana, word_kanji)
        raw_file_abs_path = tup[2]
        json_file_abs_path = tup[3]
        raw_file_rel_path = tup[4]
        json_file_rel_path = tup[5]

        if os.path.exists(raw_file_abs_path):
            die(u'File "%s" already exists.' % raw_file_rel_path)

        if os.path.exists(json_file_abs_path):
            die(u'File "%s" already exists.' % json_file_rel_path)

        fetch_raw_word(word_kana, word_kanji, dic)
        __write_word_encoding_result(dic, word_kana, word_kanji)

@no_null_dictionaries
def reparse_word(word_kana, word_kanji, dictionaries=get_dics()):
    """
    Reparse the raw files we already downloaded, and rewrite the
    KANA_KANJI.result.json file.  This could be be used when updating
    how parsing takes place and adding corrections for words that
    are now parsed correctly.

    word_kana/kanji (unicode): words in kana and kanji to reparse.
        These words should already be in the words.db.
    dictionaries (list of Dictionary objects): dictionaries to reparse
        in.
    """
    # make sure we get unicode words
    assert(type(word_kanji) == type(unicode()))
    assert(type(word_kana) == type(unicode()))

    # make sure word is in words.db
    words = get_words_from_wordsdb()
    if (word_kana, word_kanji) not in words:
        die("%s (%s) does not exist in words.db" % (word_kanji, word_kana))

    for dic in dictionaries:
        __write_word_encoding_result(dic, word_kana, word_kanji)

@no_null_dictionaries
def reparse_all(dictionaries=get_dics()):
    """
    Reparse all raw files we already downloaded, and rewrite the
    KANA_KANJI.result.json file.  This could be be used when updating
    how parsing takes place and adding corrections for words that
    are now parsed correctly.

    dictionaries (list of Dictionary objects): dictionaries to reparse
        in.
    """
    words = get_words_from_wordsdb()
    for kana, kanji in words:
        reparse_word(kana, kanji, dictionaries=dictionaries)

def main():
    global sanity_check

    def unicode_type(utf8_string):
        return utf8_string.decode('utf8')

    def dic_choices():
        return [d.short_name for d in dics]

    description="Manage words that will be tested. Run all tests if no flags are provided."
    parser = argparse.ArgumentParser(description=description)

    # add a specific word
    parser.add_argument('--add-word', '-a', action='store', nargs=2, metavar=('KANJI', 'KANA'),
            type=unicode_type, help="fetch files for word")

    # sanity checks
    parser.add_argument('--sanity-check', '-s', action='store_true',
            help="run a sanity check to make sure our words.db and actual files match up")
    parser.add_argument('--no-sanity-check', '-S', action='store_true',
            help="never run a sanity check.  WARNING: you should probably not use this")

    # reparse the raw files and rewrite the result files
    parser.add_argument('--reparse-word', '-r', action='store', nargs=2,
            metavar=('KANJI', 'KANA'), type=unicode_type,
            help="reparse files for word and rewrite KANA_KANJI.result.json")
    parser.add_argument('--reparse-all', action='store_true',
            help="reparse files for all words and rewrite *.result.json files")

    # refetch the raw files and optionally reparse
    parser.add_argument('--refetch-raw', '-f', action='store', nargs=2,
            metavar=('KANJI', 'KANA'), type=unicode_type,
            help="get raw files for word and rewrite KANA_KANJI.raw")
    parser.add_argument('--refetch-raw-all', action='store_true',
            help="refetch the raw files for all words and rewrite *.raw files")
    parser.add_argument('--refetch-raw-reparse', '-F', action='store', nargs=2,
            metavar=('KANJI', 'KANA'), type=unicode_type,
            help="get raw files for word, parse word, and write KANA_KANJI.{raw,result.json}")
    parser.add_argument('--refetch-raw-reparse-all', action='store_true',
            help="refetch raw files for all words, parse, and write *.{raw,result.json} files")

    # test only a specific word
    parser.add_argument('--test-word', '-t', action='store', nargs=2, metavar=('KANJI', 'KANA'),
            type=unicode_type, help="run tests for just KANJI KANA")

    # specify a dictionary to use
    parser.add_argument('--dictionary', '-d', action='store',
            metavar='DICTIONARY', choices=dic_choices(),
            help="select a specific dictionary to operate on")

    args = parser.parse_args()

    # set the dictionary we will be using
    dictionaries = None
    if args.dictionary:
        for dic in dics:
            if dic.short_name == args.dictionary:
                dictionaries = dic

    # handle not doing sanity check
    if args.no_sanity_check:
        sanity_check = (lambda: 1)

    # do a sanity check
    if args.sanity_check:
        sanity_check()
        sys.exit(0)

    # add a new word
    if args.add_word:
        sanity_check()
        addword(args.add_word[1], args.add_word[0])
        sys.exit(0)

    # reparse a raw file and create a result.json file for a word
    if args.reparse_word:
        sanity_check()
        reparse_word(args.reparse_word[1], args.reparse_word[0], dictionaries=dictionaries)
        sys.exit(0)
    # reparse raw files for all words and create result.json files for all words
    if args.reparse_all:
        sanity_check()
        reparse_all(dictionaries=dictionaries)
        sys.exit(0)

    # refetch raw files for word
    if args.refetch_raw:
        sanity_check()
        fetch_raw_word(args.refetch_raw[1], args.refetch_raw[0], dictionaries=dictionaries,
                assert_word_in_db=True)
        sys.exit(0)
    if args.refetch_raw_all:
        sanity_check()
        fetch_raw_all(dictionaries=dictionaries)
        sys.exit(0)
    # refecth raw files for word and then reparse
    if args.refetch_raw_reparse:
        sanity_check()
        fetch_raw_word(args.refetch_raw_reparse[1], args.refetch_raw_reparse[0],
                dictionaries=dictionaries, assert_word_in_db=True)
        reparse_word(args.refetch_raw_reparse[1], args.refetch_raw_reparse[0],
                dictionaries=dictionaries)
        sys.exit(0)
    if args.refetch_raw_reparse_all:
        sanity_check()
        fetch_raw_all(dictionaries=dictionaries)
        reparse_all(dictionaries=dictionaries)
        sys.exit(0)


    # specify the words that we will use
    kanji = None
    kana = None
    if args.test_word:
        kana = args.test_word[1]
        kanji = args.test_word[0]

    # if no options are specified, then just run all tests
    sanity_check()
    test_jdicscrape_word_parsing.test_words(kanji=kanji, kana=kana, dictionaries=dictionaries)
    sys.exit(0)

if __name__ == '__main__':
    main()

