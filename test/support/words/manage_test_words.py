#!/usr/bin/env python2

# A script for adding testable words.
import argparse
import codecs
import json
import operator
import os.path
import sys
import traceback

PROJECT_ROOT = os.path.dirname(__file__)
sys.path.append(os.path.join(PROJECT_ROOT, "..", "..", ".."))

from jdicscrape import DaijirinDictionary, DaijisenDictionary, \
        ProgressiveDictionary, NewCenturyDictionary, ExampleSentence, \
        Definition, Result

def die(string):
    print(u'ERROR! %s' % string)
    sys.exit(1)

def addword(word_kanji, word_kana):
    # make sure we get unicode words
    assert(type(word_kanji) == type(unicode()))
    assert(type(word_kana) == type(unicode()))

    # get the page
    dics = [DaijirinDictionary(),
            DaijisenDictionary(),
            ProgressiveDictionary(),
            NewCenturyDictionary()]

    add_word_to_wordsdb(word_kanji, word_kana)

    for dic in dics:
        dirname = dic.short_dic_name
        rel_path = os.path.join(os.path.dirname(__file__), dic.short_dic_name)
        abs_path = os.path.abspath(rel_path)
        if not os.path.isdir(abs_path):
            die(u'Directory "%s" does not exist.' % abs_path)

        url = dic._create_url(word_kanji, word_kana)
        page_string = dic._fetch_page(word_kanji, word_kana)
        page_string = page_string.decode('utf8')

        html_filename = u'%s_%s.html' % (word_kana, word_kanji)
        result_filename = u'%s_%s.result.json' % (word_kana, word_kanji)

        # absolute paths to the two files we will use
        html_file_abs_path = os.path.join(abs_path, html_filename)
        result_file_abs_path = os.path.join(abs_path, result_filename)

        # relative paths to the two files we will use to print out
        html_file_rel_path = os.path.join(rel_path, html_filename)
        result_file_rel_path = os.path.join(rel_path, result_filename)

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
                        (word_kanji, word_kana, dic.short_dic_name))
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

def add_word_to_wordsdb(word_kanji, word_kana):
    # Update the words.db with the current word we just added.
    words_db_rel_path = os.path.join(os.path.dirname(__file__), "words.db")
    words_db_abs_path = os.path.abspath(words_db_rel_path)
    if not (os.path.exists(words_db_abs_path)):
        die("words.db does not exist! Something is wrong!")

    words = []

    # read in current words
    with codecs.open(words_db_abs_path, 'r', 'utf8') as f:
        lines = f.read().split('\n')
    for l in lines:
        if l != '':
            kana, kanji = l.split()
            words.append(tuple([kana, kanji]))

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

def main():
    """
    parser = argparse.ArgumentParser(description="Install the current kernel.")
    parser.add_argument('--make', '-m', action='store_true',
            help="run `make`")
    parser.add_argument('--make-install-modules', '-i', action='store_true',
            help="run `make modules_install`")

    parser.add_argument('--install-kernel', '-k', action='store_true',
            help="install kernel image to /boot")

    parser.add_argument('--ssh', '-s', action='store', metavar='REMOTE_MACHINE',
            help="use ssh to copy kernel to REMOTE_MACHINE")

    parser.add_argument('--jobs', '-j', action='store', default=get_default_jobs(), type=int,
            help="specify the number of jobs (default %s)" % get_default_jobs())

    parser.add_argument('--ctags', '-t', action='store_true',
            help="run `make tags`")

    make_config_group = parser.add_mutually_exclusive_group()
    make_config_group.add_argument('--make-menuconfig', '-c', action='store_true',
            help="run `make menuconfig` first")
    make_config_group.add_argument('--make-oldconfig', '-o', action='store_true',
            help="run `make oldconfig` first")

    build_dir_group = parser.add_mutually_exclusive_group()
    build_dir_group.add_argument('--build-dir', '-b', action='store',
            help="use a separate build directory, defaults to \"build/\"",
            default="./build")
    build_dir_group.add_argument('--no-build-dir', '-n', action='store_true',
            help="don't use a separate build directory")

    ccache_group = parser.add_mutually_exclusive_group()
    ccache_group.add_argument('--ccache', '-f', action='store_true',
            default=default_use_ccache, help=ccache_help)
    ccache_group.add_argument('--no-ccache', '-g', action='store_true',
            default=(not default_use_ccache), help=no_ccache_help)

    args = parser.parse_args()

    if args.no_build_dir:
        builddir = "."
    else:
        builddir = args.build_dir
    """

    def unicode_type(utf8_string):
        return utf8_string.decode('utf8')

    parser = argparse.ArgumentParser(description="Manage words that will be tested.")
    parser.add_argument('--add-word', '-a', action='store', nargs=2, metavar=('KANJI', 'KANA'),
            type=unicode_type, help="fetch files for word")

    args = parser.parse_args()

    if args.add_word:
        addword(args.add_word[0], args.add_word[1])

if __name__ == '__main__':
    main()
