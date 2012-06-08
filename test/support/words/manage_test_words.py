#!/usr/bin/env python2

# A script for adding testable words.
import argparse
import os.path
import sys

PROJECT_ROOT = os.path.dirname(__file__)
sys.path.append(os.path.join(PROJECT_ROOT, "..", "..", ".."))

from jdicscrape import DaijirinDictionary, DaijisenDictionary, \
        ProgressiveDictionary, NewCenturyDictionary

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

    for dic in dics:
        dirname = dic.short_dic_name
        path = os.path.join(os.path.dirname(__file__), dic.short_dic_name)
        path = os.path.abspath(path)
        if not os.path.isdir(path):
            die(u'Directory "%s" does not exist.' % path)

        page_string = dic._fetch_page(word_kanji, word_kana)
        page_string = page_string.decode('utf8')

        html_filename = u'%s_%s.html' % (word_kana, word_kanji)
        result_filename = u'%s_%s.result.json' % (word_kana, word_kanji)

        html_filename_full_path = os.path.join(path, html_filename)
        result_filename_full_path = os.path.join(path, result_filename)

        if os.path.exists(html_filename_full_path):
            die(u'File "%s" already exists.' % html_filename_full_path)

        if os.path.exists(result_filename_full_path):
            die(u'File "%s" already exists.' % result_filename_full_path)

        with open(html_filename_full_path, 'w') as f:
            f.write(page_string.encode('utf8'))
            print(u'Wrote "%s".' % html_filename_full_path)

        #result = dic.lookup(word_kanji, word_kana)


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
