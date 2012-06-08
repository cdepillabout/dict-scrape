#!/usr/bin/env python2

# A script for adding testable words.
import argparse
import codecs
import json
import operator
import os
import os.path
import sys
import traceback

PROJECT_ROOT = os.path.dirname(__file__)
sys.path.append(os.path.join(PROJECT_ROOT, "..", "..", ".."))

from jdicscrape import DaijirinDictionary, DaijisenDictionary, \
        ProgressiveDictionary, NewCenturyDictionary, ExampleSentence, \
        Definition, Result

dics = [DaijirinDictionary(),
        DaijisenDictionary(),
        ProgressiveDictionary(),
        NewCenturyDictionary()]

def die(string):
    error_string = u'ERROR! %s' % string
    if __name__ == '__main__':
        print(error_string)
        sys.exit(1)
    else:
        raise Exception(error_string)

words_db_rel_path = os.path.join(os.path.dirname(__file__), "words.db")
words_db_abs_path = os.path.abspath(words_db_rel_path)
if not (os.path.exists(words_db_abs_path)):
    die("words.db does not exist! Something is wrong!")

def get_dics():
    return dics

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
    dirname, rel_path, abs_path = get_paths_for_dic(dic)

    html_filename = u'%s_%s.html' % (kana, kanji)
    result_filename = u'%s_%s.result.json' % (kana, kanji)

    # absolute paths to the two files we will use
    html_file_abs_path = os.path.join(abs_path, html_filename)
    result_file_abs_path = os.path.join(abs_path, result_filename)

    # relative paths to the two files we will use to print out
    html_file_rel_path = os.path.join(rel_path, html_filename)
    result_file_rel_path = os.path.join(rel_path, result_filename)

    return html_filename, result_filename, html_file_abs_path, \
            result_file_abs_path, html_file_rel_path, result_file_rel_path

def get_paths_for_dic(dic):
    dirname = dic.short_name
    rel_path = os.path.join(os.path.dirname(__file__), dic.short_name)
    abs_path = os.path.abspath(rel_path)

    return dirname, rel_path, abs_path

def sanity_check():
    """Make sure our words.db and actual words that have been downloaded match up."""
    words = get_words_from_wordsdb()

    # TODO: make sure every word in words is unique
    for w in words:
        kana = w[0]
        kanji = w[1]
        existing_words = [word for word in words if word[0] == kana and word[1] == kanji]
        if len(existing_words) > 1:
            die("%s (%s) exists more than once in words.db" % (kanji, kana))

    # make sure there is a file for each of our words in each dictionary directory
    for dic in dics:
        dirname, rel_path, abs_path = get_paths_for_dic(dic)
        for w in words:
            kana = w[0]
            kanji = w[1]

            tup = get_paths_for_word(dic, kana, kanji)
            html_filename = tup[0]
            result_filename = tup[1]
            html_file_abs_path = tup[2]
            result_file_abs_path = tup[3]
            html_file_rel_path = tup[4]
            result_file_rel_path = tup[5]

            if not os.path.exists(html_file_abs_path):
                die(u'%s (%s) is in words.db, but "%s" does not exist.' %
                        (kanji, kana, html_file_rel_path))

            if not os.path.exists(result_file_abs_path):
                die(u'%s (%s) is in words.db, but "%s" does not exist.' %
                        (kanji, kana, result_file_rel_path))

        for entry in os.listdir(abs_path):
            entry = entry.decode('utf8')
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

def add_word_to_wordsdb(word_kanji, word_kana):
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
    for word in words:
        print("%s (%s)" % (word[1], word[0]))

    # write sorted word list words
    with codecs.open(words_db_abs_path, 'w', 'utf8') as f:
        for word in words:
            f.write(u'%s %s\n' % (word[0], word[1]))


def addword(word_kanji, word_kana):
    # make sure we get unicode words
    assert(type(word_kanji) == type(unicode()))
    assert(type(word_kana) == type(unicode()))

    # get the page

    add_word_to_wordsdb(word_kanji, word_kana)

    for dic in dics:
        dirname, rel_path, abs_path = get_paths_for_dic(dic)
        if not os.path.isdir(abs_path):
            die(u'Directory "%s" does not exist.' % abs_path)

        url = dic._create_url(word_kanji, word_kana)
        page_string = dic._fetch_page(word_kanji, word_kana)
        page_string = page_string.decode('utf8')

        tup = get_paths_for_word(dic, kana, kanji)
        html_filename = tup[0]
        result_filename = tup[1]
        html_file_abs_path = tup[2]
        result_file_abs_path = tup[3]
        html_file_rel_path = tup[4]
        result_file_rel_path = tup[5]

        if os.path.exists(html_file_abs_path):
            die(u'File "%s" already exists.' % html_file_rel_path)

        if os.path.exists(result_file_abs_path):
            die(u'File "%s" already exists.' % result_file_rel_path)

        with open(html_file_abs_path, 'w') as f:
            f.write(page_string.encode('utf8'))
            print(u'Wrote html file: %s' % html_file_rel_path)

        # try to get the result of the encoding and write it so we have
        # something to work with.  If we can't get it, then just error
        # out and write a blank result.
        with codecs.open(result_file_abs_path, 'w', 'utf8') as f:
            try:
                result = dic.lookup(word_kanji, word_kana)
                jsonable = result.to_jsonable()
                json.dump(jsonable, f, encoding='utf8', sort_keys=True,
                        indent=4, ensure_ascii=False)
                print(u'Wrote result file: %s' % result_file_rel_path)
            except:
                traceback.print_exc()
                print(u'Error occured when parsing %s (%s) in %s.' %
                        (word_kanji, word_kana, dic.short_name))
                print(u'Writing template file "%s".' % result_file_rel_path)
                print(u'You need to go in and edit the information manually.')

                example_sentence = ExampleSentence(
                        u'***JAPANESE SENTENCE***', u'***ENGLISH SENTENCE***')
                definition = Definition(u'***DEFINITION***', [example_sentence])
                result = Result(word_kanji, word_kana, url,
                        u'***KANJI***', u'***KANA***', u'', [definition])
                jsonable = result.to_jsonable()
                json.dump(jsonable, f, encoding='utf8', sort_keys=True,
                        indent=4, ensure_ascii=False)


def main():
    def unicode_type(utf8_string):
        return utf8_string.decode('utf8')
    parser = argparse.ArgumentParser(description="Manage words that will be tested.")
    parser.add_argument('--add-word', '-a', action='store', nargs=2, metavar=('KANJI', 'KANA'),
            type=unicode_type, help="fetch files for word")
    parser.add_argument('--sanity-check', '-s', action='store_true',
            help="run a sanity check to make sure our words.db and actual files match up")

    args = parser.parse_args()

    if args.sanity_check:
        sanity_check()
        sys.exit(0)
    if args.add_word:
        sanity_check()
        addword(args.add_word[0], args.add_word[1])
        sys.exit(0)

if __name__ == '__main__':
    main()
