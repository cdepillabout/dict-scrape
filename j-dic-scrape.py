#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

import re
import sys
import urllib

from lxml import etree
from StringIO import StringIO

daijirin = {'dtype': '0', 'dname': '0ss'}
daijisen = {'dtype': '0', 'dname': '0na'}
progressive = {'dtype': '3', 'dname': '2na'}
new_century = {'dtype': '3', 'dname': '2ss'}

hiragana = """
あいうえお
ぁぃぅぇぉ
かきくけこ
がぎぐげご
さしすせそ
ざじずぜぞ
たちつてと
だぢづでど
なにぬねの
はひふへほ
ばびぶべぼ
ぱぴぷぺぽ
や　ゆ　よ
ゃ　ゅ　ょ
らりるれろ
わゐ　ゑを
ゎ　っ
ん　ゔ　ー
"""
katakana = """
アイウエオ
ァィゥェォ
カキクケコ
ガギグゲゴ
サシスセソ
ザジズゼゾ
タチツテト
ダヂヅデド
ナニヌネノ
ハヒフヘホ
バビブベボ
パピプペポ
ヤ　ユ　ヨ
ャ　ュ　ョ
ラリルレロ
ワヰ　ヱヲ
ヮ　ッ
ン　ヴ　ー
"""
# get rid of unwanted characters
for i in (hiragana, katakana):
    i.replace("\n", "")
    i.replace(" ", "")
    i.replace("　", "")

def create_page_tree(word_kanji, word_kana, dtype, dname):
    search = "%s　%s" % (word_kanji, word_kana)
    params = {'p': search, 'enc': "UTF-8", 'stype': 1, 'dtype': dtype, 'dname': dname}
    encoded_params = urllib.urlencode(params)
    page = urllib.urlopen("http://dic.yahoo.co.jp/dsearch?%s" % encoded_params)
    page_string = page.read()

    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(page_string), parser)
    return tree

def daijirin_heading(tree):
    div = tree.xpath("//div[@class='title-keyword']")[0]
    #result = etree.tostring(div, pretty_print=True, method="html", encoding='UTF-8')
    #print(result)
    heading = div.getchildren()[0]
    children = heading.getchildren()
    #from IPython import embed ; embed()

    result_accent = ""
    if children:
        for c in children:
            if c.tag == 'sub':
                result_accent = heading.getchildren()[0].text

    result = heading.xpath("text()")
    result = "".join(result)

    m = re.search("^(.*?)[ | |【|［]".decode("utf-8"), result)
    if m:
        result_kana = m.group(1)
    else:
        # we didn't get a match, so the word we are trying to find
        # should just be the entire string
        result_kana = result

    # this is just in case we don't get any kanji later
    result_word = result_kana

    m = re.search("【(.*)】$".decode('utf-8'), result)
    if m:
        result_word = m.group(1)

    print("%s: \"%s\" [%s]" %
            (result_word.encode('utf-8'), result_kana.encode('utf-8'), result_accent))

def daijirin_definition(tree):
    #definition_tables = tree.xpath("//table[@class='d-detail']/tr/td")[0]
    #result = etree.tostring(definition_tables, pretty_print=True, method="html", encoding='UTF-8')
    #print(result)
    counter = 1
    definition_tables = tree.xpath("//table[@class='d-detail']/tr/td/table")
    for defi in definition_tables:
        result = etree.tostring(defi, pretty_print=True, method="html", encoding='UTF-8')
        text_def = defi.xpath("tr/td")[1]
        result = etree.tostring(text_def, pretty_print=False, method="html", encoding='UTF-8')
        result = re.sub("^<td>", "", result)
        result = re.sub("<br>.*$", "", result)
        result = result.strip()
        print("（%d）%s" % (counter, result))
        counter += 1

    if not definition_tables:
        definition_tables = tree.xpath("//table[@class='d-detail']/tr/td")
        for defi in definition_tables:
            result = etree.tostring(defi, pretty_print=False, method="html", encoding='UTF-8')
            result = re.sub("^<td>", "", result)
            #result = re.sub("(?<! )<br>.*$", "", result)
            result = re.sub("<br></td>$", "", result)
            result = result.strip()
            print("（%d）%s" % (counter, result))
            counter += 1

def daijisen_heading(tree):
    # THIS IS BASICALLY THE SAME AS daijirin heading
    div = tree.xpath("//div[@class='title-keyword']")[0]
    #result = etree.tostring(div, pretty_print=True, method="html", encoding='UTF-8')
    #print(result)
    heading = div.getchildren()[0]
    children = heading.getchildren()
    #from IPython import embed ; embed()

    result = heading.xpath("text()")
    result = "".join(result)

    m = re.search("^(.*?)[ | |【|［|〔]".decode("utf-8"), result)
    if m:
        result_kana = m.group(1)
    else:
        # we didn't get a match, so the word we are trying to find
        # should just be the entire string
        result_kana = result

    # this is just in case we don't get any kanji later
    result_word = result_kana

    m = re.search("【(.*)】$".decode('utf-8'), result)
    if m:
        result_word = m.group(1)

    print("%s: \"%s\"" %
            (result_word.encode('utf-8'), result_kana.encode('utf-8')))

def daijisen_definition(tree):
    #definition_tables = tree.xpath("//table[@class='d-detail']/tr/td")[0]
    #result = etree.tostring(definition_tables, pretty_print=True, method="html", encoding='UTF-8')
    #print(result)
    counter = 1
    definitions = tree.xpath("//table[@class='d-detail']/tr/td")[0]
    result = etree.tostring(definitions, pretty_print=False, method="html", encoding='UTF-8')
    #print(result)
    matches = re.findall("<b>[１|２|３|４|５|６|７|８|９|０]+</b> (.*?)<br>", result)
    if matches:
        for m in matches:
            print("（%d）%s" % (counter, m))
            counter += 1
    else:
        result = re.sub("^<td>", "", result)
        result = re.sub("<br></td>.*$", "", result)
        result = result.strip()
        print("（1）%s" % result)

def new_century_heading(tree):
    # THIS IS VERY SIMILAR TO DAIJIRIN HEADING
    div = tree.xpath("//div[@class='title-keyword']")[0]
    #result = etree.tostring(div, pretty_print=True, method="html", encoding='UTF-8')
    #print(result)
    heading = div.getchildren()[0]
    children = heading.getchildren()
    #from IPython import embed ; embed()

    result = heading.xpath("text()")
    result = "".join(result)
    #print(result)

    # THIS IS DIFFERENT!!! this takes out the non-greedy match
    m = re.search("^(.*)[ | |【|［|〔]".decode("utf-8"), result)
    if m:
        result_kana = m.group(1)
    else:
        # we didn't get a match, so the word we are trying to find
        # should just be the entire string
        result_kana = result

    # THIS STRIPS< THIS IS DIFFERENT
    result_kana = result_kana.strip()

    # this is just in case we don't get any kanji later
    result_word = result_kana

    m = re.search("【(.*)】$".decode('utf-8'), result)
    if m:
        result_word = m.group(1)

    print("%s: \"%s\"" %
            (result_word.encode('utf-8'), result_kana.encode('utf-8')))

def new_century_definition(tree):
    definitions = tree.xpath("//table[@class='d-detail']/tr/td")[0]
    result = etree.tostring(definitions, pretty_print=False, method="html", encoding='UTF-8')

    # some replacements to make our lives easier
    result = result.replace('<img src="http://i.yimg.jp/images/dic/ss/gnc/g111a.gif" align="absbottom" border="0">', '〈')
    result = result.replace('<img src="http://i.yimg.jp/images/dic/ss/gnc/g111b.gif" align="absbottom" border="0">', '〉')
    result = result.replace('<img src="http://i.yimg.jp/images/dic/ss/gnc/g111c.gif" align="absbottom" border="0">', '⁝')
    result = result.replace('<img src="http://i.yimg.jp/images/dic/ss/gnc/g111d.gif" align="absbottom" border="0">', '＊')
    result = result.replace('<img src="http://i.yimg.jp/images/dic/ss/gnc/g111e.gif" align="absbottom" border="0">', '（同）')
    result = result.replace('<img src="http://i.yimg.jp/images/dic/ss/gnc/g111f.gif" align="absbottom" border="0">', 'Æ')

    # do we have multiple definitions?
    matches = re.search('<table border="0" cellspacing="0" cellpadding="0"><tr valign="top"><td><b>［１］</b>', result)
    if matches:
        # split the page into pieces for each definition
        splits = re.split('(<table border="0" cellspacing="0" cellpadding="0"><tr valign="top"><td><b>［[１|２|３|４|５|６|７|８|９|０]+］</b>)', result)
        # make sure we have an odd number of splits
        assert(len(splits) % 2 == 1)
        # throw away the first split because it's useless information
        splits = splits[1:]
        # combine the following splits
        # This is stupidly complicated.  Basically we have a list like
        # ["ab", "cd", "ef", "gh", "hi", "jk"] and we want to combine it
        # to make a list like ["abcd", "efgh", "hijk"]
        splits = ["%s%s" % (splits[i], splits[i+1]) for i in range(0, len(splits), 2)]
        #for s in splits:
        #    print "M: %s" % s
        #    print
        #    print
        #    print
        #print("multiple definitions")
    else:
        splits = [result]

    definition_counter = 1
    for splt in splits:
        print("DEFINTION %d********************************" % definition_counter)
        definition_counter += 1

        # find english definition
        #print splt
        # make sure not to match on the initial character telling whether
        # it is a noun,verb, etc
        match = re.search('<table border="0" cellspacing="0" cellpadding="0"><tr valign="top"><td>(?!<img src=".*?\.gif" align="absbottom" border="0">)(.*?)</td></tr></table>', splt)
        if match:
            print("(ENGLISH) %s" % match.group(1))

        # find example sentences
        matches = re.findall('<td><small><font color="#008800"><b>(.*?)</b></font><br><font color="#666666">(.*?)</font></small></td>', splt)
        counter = 1
        print("EXAMPLE SENTENCES:")
        if matches:
            for m in matches:
                print("（%d）%s (%s)" % (counter, m[0], m[1]))
                counter += 1

        # find kaiwa
        print("KAIWA:")
        matches = re.findall('<font color="#660000"><b>会話</b></font><br> <br><small>(.*?)」 “(.*?)</small>', splt)
        if matches:
            for m in matches:
                print("（%d）%s」 (“%s)" % (counter, m[0], m[1]))
                counter += 1

def check_daijirin(word_kanji, word_kana):
    tree = create_page_tree(word_kanji, word_kana, daijirin['dtype'], daijirin['dname'])
    daijirin_heading(tree)
    daijirin_definition(tree)

def check_daijisen(word_kanji, word_kana):
    tree = create_page_tree(word_kanji, word_kana, daijisen['dtype'], daijisen['dname'])
    daijisen_heading(tree)
    daijisen_definition(tree)

def check_new_century(word_kanji, word_kana):
    tree = create_page_tree(word_kanji, word_kana, new_century['dtype'], new_century['dname'])
    # make sure there is an entry
    result = etree.tostring(tree, pretty_print=False, method="html", encoding='UTF-8')
    word_not_found_string = '<p><em>%s %s</em>に一致する情報はみつかりませんでした。</p>' % \
            (word_kanji, word_kana)
    word_not_found_string_no_space = \
            '<p><em>%s%s</em>に一致する情報はみつかりませんでした。</p>' % \
            (word_kanji, word_kana)
    if word_not_found_string in result or word_not_found_string_no_space in result:
        print("NO DEFINITION FOUND")
        return
    # make sure this is the new century and not the progressive definition
    if '<span class="dic-zero">ニューセンチュリー和英辞典</span>' in result:
        print("NO DEFINITION FROM NEW CENTURY")
        return
    new_century_heading(tree)
    new_century_definition(tree)

def main(word_kanji, word_kana):
    check_daijirin(word_kanji, word_kana)
    print
    check_daijisen(word_kanji, word_kana)
    #print
    #check_progressive(word_kanji, word_kana)
    print
    check_new_century(word_kanji, word_kana)

if __name__ == '__main__':
    words = [
            ('強迫', 'きょうはく'),
            ('面白い', 'おもしろい'),
            ('赤し', 'あかし'),
            ('うっとり', ''),
            ('バリカン', ''),
            ('コンピエーニュ', ''),
            ('蜥蜴', 'とかげ'),
            ('らくだ', '駱駝'),
            ('成り済ます', 'なりすます'),
            ('行く', 'いく'),
            ('が', ''),
            ('遊ぶ', 'あそぶ'),
            #('遊ぶ', 'あすぶ'),
            ]

    """
    for one, two in words:
        main(one, two)
        print
        """
    one = words[11]
    main(one[0], one[1])

