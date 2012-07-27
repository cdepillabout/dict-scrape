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

import re

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

    def clean_jap_sent(self, jap_sent):
        # change english periods to japanese periods
        jap_sent = jap_sent.replace(u'.', u'。')

        return jap_sent

    def clean_eng_sent(self, eng_sent):
        # remove uneeded character
        eng_sent = eng_sent.replace(u'⌐', u'')

        # remove japanese stuff
        eng_sent = re.sub(u'〔.*?〕', u'', eng_sent)

        # (this is the character that looks like two greater than signs
        # really close together)
        eng_sent = re.sub(u'\u300A(口)\u300B', u'', eng_sent)

        # change all the other two greater than sign things with english words
        # in them to something else that doesn't use the two greater than signs
        eng_sent = re.sub(u'\u300A([A-Za-z ]+)\u300B', ur'〈\1〉', eng_sent)

        # take out double spaces that may have appeared while
        # taking out something above
        eng_sent = re.sub(u'\s+', u' ', eng_sent)

        eng_sent = eng_sent.strip()

        return eng_sent

    def clean_def(self, def_string):
        # remove leading number
        def_string = re.sub(u'^[0-9]+\s*', u'', def_string)

        # remove japanese words
        def_string = re.sub(u'〔.*?〕', u'', def_string)
        def_string = re.sub(u'【.*?】', u'', def_string)

        # remove references
        def_string = re.sub(u'\[?⇒(<reference>.*?</reference=[0-9]+:[0-9]+>(, )?)+\]?',
                u'', def_string)

        # remove uneeded character
        def_string = def_string.replace(u'⌐', u'')

        # take out double spaces that may have appeared while
        # taking out something above
        def_string = re.sub(u'\s+', u' ', def_string)

        return def_string

    def create_def(self, def_string, example_sentences=[]):
        """
        Creates a Definition() object.
        """
        def_string = self.clean_def(def_string)

        if def_string:
            def_parts = self.split_def_parts(def_string, split_characters=[u'.', u';'])
        else:
            def_parts = []

        example_sent_objects = []

        # append the extra example sentences
        for e in example_sentences:
            # split on last full space in the string
            try:
                jap_sent, eng_sent = e.rsplit(u'　', 1)
            except ValueError:
                # ValueError: need more than 1 value to unpack
                jap_sent = e
                eng_sent = u""

            jap_sent = self.clean_jap_sent(jap_sent)
            eng_sent = self.clean_eng_sent(eng_sent)

            example_sent_objects.append(ExampleSentence(jap_sent, eng_sent))

        return Definition(def_parts, example_sent_objects)


    def parse_heading(self, text):
        result_kana = u''
        result_kanji = u''
        result_accent = u''

        # ignore actual first line because it's just the heading for the dictionary entry
        first_line = text.split('\n')[1]

        # Remove sup tag
        first_line = re.sub("<sup>.*?</sup>", "", first_line)

        # Case 1: "うつくしい【美しい】 ﾛｰﾏ(utsukushii)"
        # The と is to match words like うっとり that have an optional と
        m = re.match(u"^(?P<reading>.*?)(\(と\))?【(?P<expression>.*?)】 ﾛｰﾏ\(.*?\)$", first_line)
        if (m):
            result_kana = m.group("reading")
            result_kanji = m.group("expression")
        else:
            # Case 2: "スキーマ ﾛｰﾏ(sukīma)"
            # The と is to match words like うっとり that have an optional と
            m = re.match(u"^(?P<expression>.*?)(\(と\))? ﾛｰﾏ\(.*?\)$", first_line)
            if (m):
                result_kana = m.group("expression")
                result_kanji = result_kana
            else:
                # Case 3: "隙間産業　a niche industry; a niche business."
                m = re.match(u"^(?P<expression>.*?)　(?P<definition>.*?)$", first_line)
                if (m):
                    result_kanji = m.group("expression")
                    result_kana = u'?????????'

        return result_kanji, result_kana, result_accent

    def parse_definition(self, text):
        """
        Parses the main definition of the dictionary page and returns a
        a list of Definition objects.
        """
        lines = text.split(u'\n')
        # ignore first two lines because it is just heading
        lines = lines[2:]

        current_definition = ""
        current_example_sentences = []
        all_defs = []

        for line in lines:
            line = line.strip()

            # this is starting a new definition
            if re.match(u"(([1-9]+ )?(〔|【))|[a-zA-Z()]", line):
                if current_definition or current_example_sentences:
                    all_defs.append([current_definition, current_example_sentences])
                    current_definition = ""
                    current_example_sentences = []
                current_definition += line
                continue

            # this is a sub definition, for example the second line in the
            # result for 勉強.
            if line.startswith(u'〜'):
                # this should never happen if we don't have example sentences?
                assert(not current_example_sentences)
                current_definition += line
                continue

            # this is a new sub definition that may have it's own example sentences.
            # for example, 社会[人生]勉強 that appears in the entry for 勉強.
            if line.startswith(u'◧'):
                if current_definition or current_example_sentences:
                    all_defs.append([current_definition, current_example_sentences])
                    current_definition = ""
                    current_example_sentences = []
                current_example_sentences.append(line[1:])
                continue

            # these are just standard example sentences
            if line.startswith(u'▲') or line.startswith(u'・'):
                current_example_sentences.append(line[1:])
                continue

            # otherwise, we just create a new definition and add this word as
            # an example sentence
            if current_definition or current_example_sentences:
                all_defs.append([current_definition, current_example_sentences])
                current_definition = ""
                current_example_sentences = []
            current_example_sentences.append(line)

        definitions = []
        for defs, example_sents in all_defs:
            df = self.create_def(defs, example_sents)
            definitions.append(df)

        return definitions

    narrow_gaiji_chars = {
        41256: '\xEF\xBD\x9E', # ～
        41257: '\xEF\xBD\x9E\xCC\x81', # ～́
        41258: '\xEF\xBD\x9E\xCC\x80', # ～̀
        41259: '\xEF\xBD\x9E\xCC\x81', # ～́
        41260: '\xEF\xBD\x9E', # ～
        41269: '\x2A', # * cb4960
        41270: '\xE2\x80\xB3', # ″ cb4960
        41271: '\xC2\xB4', # ´
        41272: '\xC3\x81', # Á
        41273: '\xC3\x89', # É
        41274: '\xC3\x8D', # Í
        41275: '\xC3\x93', # Ó
        41276: '\xC3\x9A', # Ú
        41277: '\xC3\x9D', # Ý
        41278: '\xC3\xA1', # á
        41279: '\xC3\xA9', # é
        41280: '\xC3\xAD', # í
        41281: '\xC3\xB3', # ó
        41282: '\xC3\xBA', # ú
        41283: '\xC3\xBD', # ý
        41284: '\xC3\x81', # Á
        41285: '\xC3\x89', # É
        41286: '\xC3\x8D', # Í
        41287: '\xC3\x93', # Ó
        41288: '\xC3\x9A', # Ú
        41289: '\xC3\x9D', # Ý
        41290: '\xC3\xA1', # á
        41291: '\xC3\xA9', # é
        41292: '\xC3\xAD', # í
        41293: '\xC3\xB3', # ó
        41294: '\xC3\xBA', # ú
        41295: '\xC3\xBD', # ý
        41296: '\xCA\x8C\xCC\x81', # ʌ́
        41297: '\xC7\xBF', # ǿ
        41298: '\xC2\xB4', # ´
        41299: '\xC3\x81', # Á
        41300: '\xC3\x89', # É
        41301: '\xC3\x8D', # Í
        41302: '\xC3\x93', # Ó
        41303: '\xC3\x9A', # Ú
        41304: '\xC3\x9D', # Ý
        41305: '\xC3\xA1', # á
        41306: '\xC3\xA9', # é
        41307: '\xC3\xAD', # í
        41308: '\xC3\xB3', # ó
        41309: '\xC3\xBA', # ú
        41310: '\xC3\xBD', # ý
        41311: '\xC7\xBF', # ǿ
        41312: '\xCA\x8C\xCC\x81', # ʌ́
        41313: '\xC3\x80', # À
        41314: '\xC3\x88', # È
        41315: '\xC3\x8C', # Ì
        41316: '\xC3\x92', # Ò
        41317: '\xC3\x99', # Ù
        41318: '\xE1\xBB\xB2', # Ỳ
        41319: '\xC3\xA0', # à
        41320: '\xC3\xA8', # è
        41321: '\xC3\xAC', # ì
        41322: '\xC3\xB2', # ò
        41323: '\xC3\xB9', # ù
        41324: '\xE1\xBB\xB3', # ỳ
        41325: '\x60', # `
        41326: '\xC3\x80', # À
        41327: '\xC3\x88', # È
        41328: '\xC3\x8C', # Ì
        41329: '\xC3\x92', # Ò
        41330: '\xC3\x99', # Ù
        41331: '\xE1\xBB\xB2', # Ỳ
        41332: '\xC3\xA0', # à
        41333: '\xC3\xA8', # è
        41334: '\xC3\xAC', # ì
        41335: '\xC3\xB2', # ò
        41336: '\xC3\xB9', # ù
        41337: '\xE1\xBB\xB3', # ỳ
        41338: '\xCA\x8C\xCC\x80', # ʌ̀
        41339: '\xC3\xB8\xCC\x80', # ø̀
        41340: '\xC3\x84', # Ä
        41341: '\xC3\x8B', # Ë
        41342: '\xC3\x8F', # Ï
        41505: '\xC3\x96', # Ö
        41506: '\xC3\x9C', # Ü
        41507: '\xC5\xB8', # Ÿ
        41508: '\xC3\xA4', # ä
        41509: '\xC3\xAB', # ë
        41510: '\xC3\xAF', # ï
        41511: '\xC3\xB6', # ö
        41512: '\xC3\xBC', # ü
        41513: '\xC3\xBF', # ÿ
        41515: '\xC3\x82', # Â
        41516: '\xC3\x8A', # Ê
        41517: '\xC3\x8E', # Î
        41518: '\xC3\x94', # Ô
        41519: '\xC3\x9B', # Û
        41520: '\xC3\xA2', # â
        41521: '\xC3\xAA', # ê
        41522: '\xC3\xAE', # î
        41523: '\xC3\xB4', # ô
        41524: '\xC3\xBB', # û
        41525: '\xC4\x81', # ā
        41526: '\xC4\x93', # ē
        41527: '\xC4\xAB', # ī
        41528: '\xC5\x8D', # ō
        41529: '\xC5\xAB', # ū
        41530: '\xD3\xAF', # ӯ
        41532: '\xC3\x87', # Ç
        41533: '\xC3\xA7', # ç
        41534: '\xC9\x99\xCC\x81', # ə́
        41535: '\xC9\x9A\xCC\x81', # ɚ́
        41536: '\xC9\x9B\xCC\x81', # ɛ́
        41537: '\xC4\xB1\xCC\x81', # ı́
        41538: '\xC9\x94\xCC\x81', # ɔ́
        41539: '\xCA\x8A\xCC\x81', # ʊ́
        41540: '\xC9\xAF\xCC\x81', # ɯ́
        41541: '\xCA\x8F\xCC\x81', # ʏ́
        41542: '\xC9\x91\xCC\x81', # ɑ́
        41543: '\xC9\x99\xCC\x81', # ə́
        41544: '\xC9\x9A\xCC\x81', # ɚ́
        41545: '\xC9\x9B\xCC\x81', # ɛ́
        41546: '\xC4\xB1\xCC\x81', # ı́
        41547: '\xC9\x94\xCC\x81', # ɔ́
        41548: '\xCA\x8A\xCC\x81', # ʊ́
        41549: '\xC9\xAF\xCC\x81', # ɯ́
        41550: '\xCA\x8F\xCC\x81', # ʏ́
        41551: '\xC9\x91\xCC\x81', # ɑ́
        41552: '\xC9\x99\xCC\x80', # ə̀
        41553: '\xC9\x9A\xCC\x80', # ɚ̀
        41554: '\xC9\x9B\xCC\x80', # ɛ̀
        41555: '\xC4\xB1\xCC\x80', # ı̀
        41556: '\xC9\x94\xCC\x80', # ɔ̀
        41557: '\xCA\x8A\xCC\x80', # ʊ̀
        41558: '\xC9\xAF\xCC\x80', # ɯ̀
        41559: '\xCA\x8F\xCC\x80', # ʏ̀
        41560: '\xC9\x91\xCC\x80', # ɑ̀
        41561: '\x7E', # ~
        41562: '\xC9\x9B\xCC\x83', # ɛ̃
        41563: '\xC4\xB1\xCC\x83', # ı̃
        41564: '\xC9\x94\xCC\x83', # ɔ̃
        41565: '\xC9\x91\xCC\x83', # ɑ̃
        41566: '\xC3\xA3', # ã
        41567: '\xC3\xB1', # ñ
        41568: '\xCA\x8C\xCC\x83', # ʌ̃
        41581: '\xCA\x8C', # ʌ
        41582: '\xC3\xB8', # ø
        41583: '\xC9\x99', # ə
        41584: '\xC9\x9A', # ɚ
        41585: '\xC9\x9B', # ɛ
        41586: '\xC4\xB1', # ı
        41587: '\xC9\x94', # ɔ
        41588: '\xCA\x8A', # ʊ
        41589: '\xCE\xB8', # θ
        41590: '\xC3\xB0', # ð
        41591: '\xCA\x83', # ʃ
        41592: '\xCA\x92', # ʒ
        41593: '\xC5\x8B', # ŋ
        41594: '\xCB\x90', # ː
        41595: '\xC9\x91', # ɑ
        41596: '\xC3\x98', # Ø
        41597: '\x74\xCC\xA3', # ṭ
        41761: '\xCB\x98', # ˘
        41768: '\xCB\x98', # ˘
        41769: '\xC4\x82', # Ă
        41770: '\xC4\x94', # Ĕ
        41771: '\xC4\xAC', # Ĭ
        41772: '\xC5\x8E', # Ŏ
        41773: '\xC5\xAC', # Ŭ
        41774: '\x59\xCC\x86', # Y̆
        41775: '\xC4\x83', # ă
        41776: '\xC4\x95', # ĕ
        41777: '\x67\xCC\x86', # ğ
        41778: '\x6C\xCC\x86', # l̆
        41779: '\xC5\x8F', # ŏ
        41780: '\xC5\xAD', # ŭ
        41781: '\x79\xCC\x86', # y̆
        41782: '\xCB\x87', # ˇ
        41783: '\xC7\x8D', # Ǎ
        41784: '\xC4\x8C', # Č
        41785: '\x49\xCC\x8C', # Ǐ
        41786: '\x4E\xCC\x8C', # Ň
        41787: '\xC5\x98', # Ř
        41788: '\xC5\xA0', # Š
        41789: '\xC5\xBD', # Ž
        41790: '\xC7\x8E', # ǎ
        41791: '\xC4\x8D', # č
        41792: '\xC4\x9B', # ě
        41793: '\x69\xCC\x8C', # ǐ
        41794: '\x6E\xCC\x8C', # ň
        41795: '\xC5\x99', # ř
        41796: '\xC5\xA1', # š
        41797: '\xC5\xBE', # ž
        41798: '\x6B\xCC\xA0', # k̠
        41799: '\x74\xCC\xA0', # t̠
        41800: '\xCB\x9B', # ˛
        41801: '\xC4\x84', # Ą
        41802: '\xC4\x98', # Ę
        41803: '\x4F\xCC\xA8', # Ǫ
        41804: '\xC4\x85', # ą
        41805: '\xC4\x99', # ę
        41806: '\x6F\xCC\xA8', # ǫ
        41807: '\xC3\x87', # Ç
        41808: '\xC5\x9E', # Ş
        41809: '\xC5\xA2', # Ţ
        41810: '\xC3\xA7', # ç
        41811: '\xC5\x9F', # ş
        41812: '\xC5\xA3', # ţ
        41814: '\x44\xCC\xBB', # D̻
        41815: '\x48\xCC\xBB', # H̻
        41816: '\x68\xCC\xBB', # h̻
        41817: '\x6D\xCC\xBB', # m̻
        41818: '\x6E\xCC\xBB', # n̻
        41819: '\x6E\xCC\xA9', # n̩
        41820: '\x6D\xCC\x81', # ḿ
        41821: '\xC4\x86', # Ć
        41822: '\xC5\x9A', # Ś
        41823: '\xC4\x87', # ć
        41824: '\xC5\x84', # ń
        41825: '\xC5\x9B', # ś
        41826: '\xC5\xBA', # ź
        41827: '\x42\xCC\x81', # B́
        41828: '\xC4\x86', # Ć
        41829: '\x44\xCC\x81', # D́
        41830: '\x46\xCC\x81', # F́
        41831: '\x47\xCC\x81', # Ǵ
        41832: '\x48\xCC\x81', # H́
        41833: '\x4A\xCC\x81', # J́
        41834: '\x4B\xCC\x81', # Ḱ
        41835: '\xC4\xB9', # Ĺ
        41836: '\x4D\xCC\x81', # Ḿ
        41837: '\xC5\x83', # Ń
        41838: '\x50\xCC\x81', # Ṕ
        41839: '\x51\xCC\x81', # Q́
        41840: '\xC5\x94', # Ŕ
        41841: '\xC5\x9A', # Ś
        41842: '\x54\xCC\x81', # T́
        41843: '\x56\xCC\x81', # V́
        41844: '\xE1\xBA\x82', # Ẃ
        41845: '\x58\xCC\x81', # X́
        41846: '\xC5\xB9', # Ź
        41847: '\x62\xCC\x81', # b́
        41848: '\xC4\x87', # ć
        41849: '\x64\xCC\x81', # d́
        41850: '\x66\xCC\x81', # f́
        41851: '\x67\xCC\x81', # ǵ
        41852: '\x68\xCC\x81', # h́
        41853: '\x6A\xCC\x81', # j́
        41854: '\x6B\xCC\x81', # ḱ
        42017: '\xC4\xBA', # ĺ
        42018: '\x6D\xCC\x81', # ḿ
        42019: '\xC5\x84', # ń
        42020: '\x70\xCC\x81', # ṕ
        42021: '\x71\xCC\x81', # q́
        42022: '\xC5\x95', # ŕ
        42023: '\xC5\x9B', # ś
        42024: '\x74\xCC\x81', # t́
        42025: '\x76\xCC\x81', # v́
        42026: '\xE1\xBA\x83', # ẃ
        42027: '\x78\xCC\x81', # x́
        42028: '\xC5\xBA', # ź
        42029: '\x32\xCC\x81', # 2́
        42030: '\x34\xCC\x81', # 4́
        42031: '\x38\xCC\x81', # 8́
        42032: '\x39\xCC\x81', # 9́
        42033: '\x42\xCC\x80', # B̀
        42034: '\x43\xCC\x80', # C̀
        42035: '\x44\xCC\x80', # D̀
        42036: '\x46\xCC\x80', # F̀
        42037: '\x47\xCC\x80', # G̀
        42038: '\x48\xCC\x80', # H̀
        42039: '\x4A\xCC\x80', # J̀
        42040: '\x4B\xCC\x80', # K̀
        42041: '\x4C\xCC\x80', # L̀
        42042: '\x4D\xCC\x80', # M̀
        42043: '\x4E\xCC\x80', # Ǹ
        42044: '\x50\xCC\x80', # P̀
        42045: '\x51\xCC\x80', # Q̀
        42046: '\x52\xCC\x80', # R̀
        42047: '\x53\xCC\x80', # S̀
        42048: '\x54\xCC\x80', # T̀
        42049: '\x56\xCC\x80', # V̀
        42050: '\xE1\xBA\x80', # Ẁ
        42051: '\x58\xCC\x80', # X̀
        42052: '\x5A\xCC\x80', # Z̀
        42053: '\xCA\x87', # ʇ
        42054: '\xC9\xAF', # ɯ
        42055: '\xCA\x8F', # ʏ
        42056: '\xC9\xA5', # ɥ
        42057: '\xC9\xB8', # ɸ
        42058: '\xCA\x94', # ʔ
        42059: '\xC4\x90', # Đ
        42060: '\xC4\x91', # đ
        42061: '\xE2\x80\x98', # ‘
        42063: '\xC5\x81', # Ł
        42066: '\xC2\xBF', # ¿
        42068: '\xC5\x82', # ł
        42069: '\xC3\x83', # Ã
        42070: '\xC3\x91', # Ñ
        42071: '\xC3\xB5', # õ
        42073: '\xC5\x90', # Ő
        42074: '\xC5\x91', # ő
        42075: '\xC3\x85', # Å
        42076: '\xC3\xA5', # å
        42077: '\xC5\xAF', # ů
        42078: '\x79\xCC\x8A', # ẙ
        42079: '\x77\xCC\x8A', # ẘ
        42080: '\x44\xCC\xA3', # Ḍ
        42081: '\x48\xCC\xA3', # Ḥ
        42082: '\x4B\xCC\xA3', # Ḳ
        42083: '\x4D\xCC\xA3', # Ṃ
        42084: '\x4E\xCC\xA3', # Ṇ
        42085: '\x52\xCC\xA3', # Ṛ
        42086: '\x53\xCC\xA3', # Ṣ
        42087: '\x54\xCC\xA3', # Ṭ
        42088: '\x5A\xCC\xA3', # Ẓ
        42089: '\x64\xCC\xA3', # ḍ
        42090: '\x68\xCC\xA3', # ḥ
        42091: '\x6B\xCC\xA3', # ḳ
        42092: '\x6D\xCC\xA3', # ṃ
        42093: '\x6E\xCC\xA3', # ṇ
        42094: '\x72\xCC\xA3', # ṛ
        42095: '\x73\xCC\xA3', # ṣ
        42096: '\x7A\xCC\xA3', # ẓ
        42098: '\x31\xCC\x87', # 1̇
        42099: '\x33\xCC\x87', # 3̇
        42100: '\x44\xCC\x87', # Ḋ
        42101: '\x47\xCC\x87', # Ġ
        42102: '\x49\xCC\x87', # İ
        42103: '\x55\xCC\x87', # U̇
        42104: '\x5A\xCC\x87', # Ż
        42105: '\x61\xCC\x87', # ȧ
        42106: '\xC4\x97', # ė
        42107: '\xC4\xA1', # ġ
        42108: '\x6D\xCC\x87', # ṁ
        42109: '\x6E\xCC\x87', # ṅ
        42110: '\x71\xCC\x87', # q̇
        42273: '\x75\xCC\x87', # u̇
        42274: '\x79\xCC\x87', # ẏ
        42279: '\xCA\x8A', # ʊ
        42280: '\xCA\x8E', # ʎ
        42294: '\x53\xCC\x88', # S̈
        42295: '\x54\xCC\x88', # T̈
        42296: '\x58\xCC\x88', # Ẍ
        42297: '\x59\xCC\x88', # Ÿ
        42298: '\x73\xCC\x88', # s̈
        42299: '\x74\xCC\x88', # ẗ
        42300: '\x78\xCC\x88', # ẍ
        42302: '\x31\xCC\x84', # 1̄
        42303: '\x32\xCC\x84', # 2̄
        42304: '\x33\xCC\x84', # 3̄
        42305: '\x34\xCC\x84', # 4̄
        42306: '\x36\xCC\x84', # 6̄
        42307: '\xC4\x80', # Ā
        42308: '\x42\xCC\x84', # B̄
        42309: '\x43\xCC\x84', # C̄
        42310: '\x44\xCC\x84', # D̄
        42311: '\xC4\x92', # Ē
        42312: '\x47\xCC\x84', # Ḡ
        42313: '\xC4\xAA', # Ī
        42314: '\x4B\xCC\x84', # K̄
        42315: '\x4D\xCC\x84', # M̄
        42316: '\xC5\x8C', # Ō
        42317: '\x52\xCC\x84', # R̄
        42318: '\xC5\xAA', # Ū
        42319: '\x56\xCC\x84', # V̄
        42320: '\x58\xCC\x84', # X̄
        42321: '\x59\xCC\x84', # Ȳ
        42322: '\x62\xCC\x84', # b̄
        42323: '\x63\xCC\x84', # c̄
        42324: '\x64\xCC\x84', # d̄
        42325: '\x68\xCC\x84', # h̄
        42326: '\x71\xCC\x84', # q̄
        42327: '\x73\xCC\x84', # s̄
        42328: '\x74\xCC\x84', # t̄
        42329: '\x78\xCC\x84', # x̄
        42330: '\x7A\xCC\x84', # z̄
        42338: '\x6E\xCC\x84', # n̄
        42339: '\x70\xCC\x84', # p̄
        42340: '\xC4\x9E', # Ğ
        42341: '\xC4\x9A', # Ě
        42342: '\xC5\x83', # Ń
        42343: '\xC5\xB9', # Ź
        42344: '\xE3\x80\x96', # 〖 cb4960
        42345: '\xE3\x80\x97', # 〗 cb4960
        42357: '\xC5\xBC', # ż
    }

    wide_gaiji_chars = {
        45390: '\xC7\xBD', # ǽ
        45391: '\xC3\xA6\xCC\x80', # æ̀
        45392: '\xC7\xBD', # ǽ
        45393: '\xC3\xA6\xCC\x84', # ǣ
        45396: '\xC3\xA6\xCC\x83', # æ̃
        45397: '\xC3\xA6', # æ
        45398: '\xC5\x93\xCC\x81', # œ́
        45399: '\xC5\x93\xCC\x80', # œ̀
        45400: '\xC5\x93\xCC\x81', # œ́
        45401: '\xC5\x93\xCC\x83', # œ̃
        45402: '\xC5\x93', # œ
        45403: '\xC5\x92', # Œ
        45406: '\xC3\x86', # Æ
        45429: '\xC2\xA9', # ©
        45430: '\xC2\xAE', # ®
        45433: '\xEF\xAC\x81', # ﬁ
        45629: '\xE2\x8C\x90', # ⌐ cb4960
        45630: '\xE2\x94\x90', # ┐ cb4960
        45631: '\xE2\x94\x94', # └ cb4960
        45632: '\xE2\x94\x98', # ┘ cb4960
        46449: '\xE2\x9E\xA1', # ➡ cb4960
        46686: '\xE2\x96\xB2', # ▲ cb4960
        46689: '\xE2\x9E\xAA', # ➪ cb4960
        46695: '\xEF\xBE\x9B\xEF\xBD\xB0\xEF\xBE\x8F', # ﾛｰﾏ cb4960
        46699: '\xE2\x97\xA7', # ◧ cb4960
        46700: '\xE2\x97\xA8', # ◨ cb4960
    }
