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
            result = re.sub("(?<! )<br>.*$", "", result)
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

def check_daijirin(word_kanji, word_kana):
    tree = create_page_tree(word_kanji, word_kana, daijirin['dtype'], daijirin['dname'])
    daijirin_heading(tree)
    daijirin_definition(tree)

def check_daijisen(word_kanji, word_kana):
    tree = create_page_tree(word_kanji, word_kana, daijisen['dtype'], daijisen['dname'])

    daijisen_heading(tree)
    daijisen_definition(tree)

def main(word_kanji, word_kana):
    check_daijirin(word_kanji, word_kana)
    check_daijisen(word_kanji, word_kana)

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
            ]

    for one, two in words:
        main(one, two)
        print

    """
    one = words[1]
    main(one[0], one[1])
    """

