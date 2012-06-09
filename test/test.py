
import json
import os
import subprocess
import sys
import manage_test_words as manage_words

from jdicscrape import Result

def test_words_sanity():
    # TODO: This should be moved to the run_test.sh script.
    """Check sanity of words database (keep this test first)"""
    script_path = os.path.join(os.path.dirname(__file__),
            "support", "words", "manage_test_words.py")
    p = subprocess.Popen([script_path, "-s"])
    sts = os.waitpid(p.pid, 0)[1]
    assert sts == 0

def checkword(dictionary, kanji, kana):
    html = manage_words.get_html_for_word(dictionary, kana, kanji)
    json_object = manage_words.get_json_for_word(dictionary, kana, kanji)

    html_parse_result = dictionary.lookup(kanji, kana, html)
    json_result = Result.from_jsonable(json_object)

    if (json_result != html_parse_result):
        # TODO: find out what doesn't match
        assert(json_result == html_parse_result)

def test_words():
    words = manage_words.get_words_from_wordsdb()
    for dic in manage_words.get_dics():
        for kana, kanji in words:
            checkword.description = u'check %s (%s) in %s' % (kana, kanji, dic.short_name)
            yield checkword, dic, kanji, kana

