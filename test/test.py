
import os
import subprocess
import sys
import manage_test_words as manage_words

def test_words_sanity():
    # TODO: This should be moved to the run_test.sh script.
    """Check sanity of words database (keep this test first)"""
    script_path = os.path.join(os.path.dirname(__file__),
            "support", "words", "manage_test_words.py")
    p = subprocess.Popen([script_path, "-s"])
    sts = os.waitpid(p.pid, 0)[1]
    assert sts == 0

def test_test():
    assert 1 == 1

def checkword(dictionary, kanji, kana, html, json_result):
    assert 1 == 1

def test_words():
    words = manage_words.get_words_from_wordsdb()

    for dic in manage_words.get_dics():
        for word in words:
            _,_,html,json_result,_,_ = manage_words.get_paths_for_word(dic, word[0], word[1])
            checkword.description = u'check %s (%s) in %s' % (word[1], word[0], dic.short_name)
            yield checkword, dic, word[1], word[0], html, json_result

