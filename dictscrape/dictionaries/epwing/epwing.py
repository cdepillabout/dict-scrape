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
import string

from eb import *

from ..dictionary import Dictionary
from ...result import Result

from ...example_sentence import ExampleSentence
from ...definition import Definition

class EB_Hit:
    def __init__(self, book, subbook, position):
        self.book = book # EB instance
        self.subbook = subbook
        self.position = position # (heading, text)
    def heading(self, container=None):
        return self.book.get_content(
            self.subbook, self.position[0], container, eb_read_heading).decode('euc-jp')
    def text(self, container=None):
        return self.book.get_content(
            self.subbook, self.position[1], container, eb_read_text).decode('euc-jp')

class EB:
    def __init__(self, dir):
        self.book     = EB_Book()
        self.appendix = EB_Appendix()
        self.hookset  = EB_Hookset()
        eb_set_hooks(self.hookset, (
            (EB_HOOK_NEWLINE,              self.handle_newline),
            (EB_HOOK_SET_INDENT,           self.handle_set_indent),
            (EB_HOOK_NARROW_FONT,          self.handle_font),
            (EB_HOOK_WIDE_FONT,            self.handle_font),
            #(EB_HOOK_STOP_CODE,            self.handle_stop_code),
            (EB_HOOK_BEGIN_NARROW,         self.handle_tags),
            (EB_HOOK_END_NARROW,           self.handle_tags),
            (EB_HOOK_BEGIN_SUBSCRIPT,      self.handle_tags),
            (EB_HOOK_END_SUBSCRIPT,        self.handle_tags),
            (EB_HOOK_BEGIN_SUPERSCRIPT,    self.handle_tags),
            (EB_HOOK_END_SUPERSCRIPT,      self.handle_tags),
            (EB_HOOK_BEGIN_NO_NEWLINE,     self.handle_tags),
            (EB_HOOK_END_NO_NEWLINE,       self.handle_tags),
            (EB_HOOK_BEGIN_EMPHASIS,       self.handle_tags),
            (EB_HOOK_END_EMPHASIS,         self.handle_tags),
            (EB_HOOK_BEGIN_CANDIDATE,      self.handle_tags),
            (EB_HOOK_END_CANDIDATE_GROUP,  self.handle_tags),
            (EB_HOOK_END_CANDIDATE_LEAF,   self.handle_tags),
            (EB_HOOK_BEGIN_REFERENCE,      self.handle_tags),
            (EB_HOOK_END_REFERENCE,        self.handle_tags),
            (EB_HOOK_BEGIN_KEYWORD,        self.handle_tags),
            (EB_HOOK_END_KEYWORD,          self.handle_tags),
            (EB_HOOK_BEGIN_MONO_GRAPHIC,   self.handle_tags),
            (EB_HOOK_END_MONO_GRAPHIC,     self.handle_tags),
            (EB_HOOK_BEGIN_GRAY_GRAPHIC,   self.handle_tags),
            (EB_HOOK_END_GRAY_GRAPHIC,     self.handle_tags),
            (EB_HOOK_BEGIN_COLOR_BMP,      self.handle_tags),
            (EB_HOOK_BEGIN_COLOR_JPEG,     self.handle_tags),
            (EB_HOOK_END_COLOR_GRAPHIC,    self.handle_tags),
            (EB_HOOK_BEGIN_IN_COLOR_BMP,   self.handle_tags),
            (EB_HOOK_BEGIN_IN_COLOR_JPEG,  self.handle_tags),
            (EB_HOOK_END_IN_COLOR_GRAPHIC, self.handle_tags),
            (EB_HOOK_BEGIN_WAVE,           self.handle_tags),
            (EB_HOOK_END_WAVE,             self.handle_tags),
            (EB_HOOK_BEGIN_MPEG,           self.handle_tags),
            (EB_HOOK_END_MPEG,             self.handle_tags)))
        self.bind(dir)
        self.set_subbook(0)

    def handle_newline(self, book, appendix, container, code, argv):
        ##print "handle_newline: code=%d, argv=%s" % (code, repr(argv))
        self.hook_newline(container)
        return EB_SUCCESS

    def handle_set_indent(self, book, appendix, container, code, argv):
        ##print "handle_set_indent: code=%d, argv=%s" % (code, repr(argv))
        self.hook_set_indent(container, argv[1])
        return EB_SUCCESS

    def handle_font(self, book, appendix, container, code, argv):
        ##print "handle_font: code=%d, argv=%s" % (code, repr(argv))
        if code == EB_HOOK_NARROW_FONT:
            self.hook_narrow_font(container, argv[0])
        elif code == EB_HOOK_WIDE_FONT:
            self.hook_wide_font(container, argv[0])
        return EB_SUCCESS

    def handle_tags(self, book, appendix, container, code, argv):
        ##print "handle_tags: code=%d, argv=%s" % (code, repr(argv))
        if code == EB_HOOK_BEGIN_NARROW:
            self.hook_begin_narrow(container)
        elif code == EB_HOOK_END_NARROW:
            self.hook_end_narrow(container)
        elif code == EB_HOOK_BEGIN_SUBSCRIPT:
            self.hook_begin_subscript(container)
        elif code == EB_HOOK_END_SUBSCRIPT:
            self.hook_end_subscript(container)
        elif code == EB_HOOK_BEGIN_SUPERSCRIPT:
            self.hook_begin_superscript(container)
        elif code == EB_HOOK_END_SUPERSCRIPT:
            self.hook_end_superscript(container)
        elif code == EB_HOOK_BEGIN_NO_NEWLINE:
            self.hook_begin_no_newline(container)
        elif code == EB_HOOK_END_NO_NEWLINE:
            self.hook_end_no_newline(container)
        elif code == EB_HOOK_BEGIN_EMPHASIS:
            self.hook_begin_emphasis(container)
        elif code == EB_HOOK_END_EMPHASIS:
            self.hook_end_emphasis(container)
        elif code == EB_HOOK_BEGIN_REFERENCE:
            self.hook_begin_reference(container)
        elif code == EB_HOOK_END_REFERENCE:
            self.hook_end_reference(container, argv[1], argv[2])
        elif code == EB_HOOK_BEGIN_KEYWORD:
            self.hook_begin_keyword(container)
        elif code == EB_HOOK_END_KEYWORD:
            self.hook_end_keyword(container)
        return EB_SUCCESS

    def handle_stop_code(self, book, appendix, container, code, argv):
        ##print "handle_stop_code: code=%d, argv=%s" % (code, repr(argv))
        return eb_hook_stop_code(book, appendix, container, code, argv)

    def write_text(self, text):
        eb_write_text(self.book, text)

    def get_content(self, subbook, position, container, func):
        # save current subbook
        current_subbook = self.subbook()
        if current_subbook != subbook:
            self.set_subbook(subbook)
        else:
            current_subbook = None
        # get content at the specified subbook/position
        eb_seek_text(self.book, position)
        buffer = []
        while 1:
            data = func(self.book, self.appendix, self.hookset, container)
            if not data:
                break
            buffer.append(data)
        # restore current subbook
        if current_subbook is not None:
            self.set_subbook(current_subbook)
        return string.join(buffer, u''.encode('euc-jp'))

    ###########
    # callbacks
    ###########

    def hook_newline(self, container):
        self.write_text(u"\n".encode('euc-jp'))

    def hook_set_indent(self, container, indent):
        pass

    def hook_narrow_font(self, container, code):
        try:
            text = eb_narrow_alt_character_text(self.appendix, code)
        except EBError:
            text = u"❑".encode('euc-jp')
        self.write_text(text)

    def hook_wide_font(self, container, code):
        try:
            text = eb_wide_alt_character_text(self.appendix, code)
        except EBError:
            text = u"◎".encode('euc-jp')
        self.write_text(text)

    def hook_begin_narrow(self, container):
        pass

    def hook_end_narrow(self, container):
        pass

    def hook_begin_subscript(self, container):
        pass

    def hook_end_subscript(self, container):
        pass

    def hook_begin_superscript(self, container):
        pass

    def hook_end_superscript(self, container):
        pass

    def hook_begin_no_newline(self, container):
        pass

    def hook_end_no_newline(self, container):
        pass

    def hook_begin_emphasis(self, container):
        pass

    def hook_end_emphasis(self, container):
        pass

    def hook_begin_reference(self, container):
        pass

    def hook_end_reference(self, container, page, offset):
        pass

    def hook_begin_keyword(self, container):
        pass

    def hook_end_keyword(self, container):
        pass

    ###########
    # functions
    ###########

    def bind(self, dir):
        eb_bind(self.book, dir)

    def suspend(self):
        eb_suspend(self.book)

    def is_bound(self):
        return eb_is_bound(self.book)

    def path(self):
        return eb_path(self.book)

    def character_code(self):
        return eb_character_code(self.book)

    def disc_type(self):
        return eb_disc_type(self.book)

    def load_all_subbooks(self):
        eb_load_all_subbooks(self.book)

    def subbook_list(self):
        return eb_subbook_list(self.book)

    def set_subbook(self, subbook):
        eb_set_subbook(self.book, subbook)

    def unset_subbook(self):
        eb_unset_subbook(self.book)

    def subbook(self):
        return eb_subbook(self.book)

    def subbook_title(self, subbook=None):
        if subbook is None:
            return eb_subbook_title(self.book)
        return eb_subbook_title2(self.book, subbook)

    def subbook_directory(self, subbook=None):
        if subbook is None:
            return eb_subbook_directory(self.book)
        return eb_subbook_directory2(self.book, subbook)

    def copyright(self):
        if eb_have_copyright(self.book):
            return EB_Hit(self, None, eb_copyright(self.book))
        return None

    def menu(self):
        if eb_have_menu(self.book):
            return EB_Hit(self, None, eb_menu(self.book))
        return None

    def search(self, word_kanji):
        word_kanji = word_kanji.encode('euc-jp')
        eb_search_exactword(self.book, word_kanji)
        buffer = []
        while 1:
            hitlist = eb_hit_list(self.book)
            if not hitlist:
                break
            subbook = self.subbook()
            for hit in hitlist:
                buffer.append(EB_Hit(self, subbook, hit))
        return buffer


class EBTest(EB):
    def hook_narrow_font(self, container, code):
        self.write_text("<gaiji=h%s>" % code)
    def hook_wide_font(self, container, code):
        self.write_text("<gaiji=z%s>" % code)
    def hook_begin_reference(self, container):
        self.write_text("<reference>")
    def hook_end_reference(self, container, page, offset):
        self.write_text("</reference=%x:%x>" % (page, offset))
    def hook_begin_keyword(self, container):
        #self.write_text("<keyword>")
        pass
    def hook_end_keyword(self, container):
        #self.write_text("</keyword>")
        pass
    def hook_begin_subscript(self, container):
        self.write_text("<sub>")
    def hook_end_subscript(self, container):
        self.write_text("</sub>")
    def hook_begin_superscript(self, container):
        self.write_text("<sup>")
    def hook_end_superscript(self, container):
        self.write_text("</sup>")


class EpwingDictionary(Dictionary):

    def replace_gaiji(self, text):
        gaijis = re.findall(u'<gaiji=[hz][0-9]+>', text)
        gaijis = set(gaijis)

        for gai in gaijis:
            m = re.match(u'^<gaiji=([hz])([0-9]+)>$', gai)
            assert m and m.group(1) and m.group(2)
            gaiji_type = m.group(1)
            gaiji_code = int(m.group(2))

            if gaiji_type == 'h' and gaiji_code in self.narrow_gaiji_chars:
                text = text.replace(m.group(0),
                        self.narrow_gaiji_chars[gaiji_code].decode('utf8'))
            elif gaiji_type == 'z' and gaiji_code in self.wide_gaiji_chars:
                text = text.replace(m.group(0),
                        self.wide_gaiji_chars[gaiji_code].decode('utf8'))

        return text

    def _create_url(self, word_kanji, word_kana):
        """Returns a URL for the word/page we are trying to lookup."""
        return u'search for %s (%s) in %s' % (word_kanji, word_kana, self.short_dictionary_name)

    def parse_heading(self, text):
        """
        This needs to return kanji as a list because one heading may have
        multiple kanji.
        """
        raise NotImplementedError, "This needs to be overrode in a child class."

    def parse_definition(self, text):
        """
        Parses the main definition of the dictionary page and returns a
        a list of Definition objects.
        """
        raise NotImplementedError, "This needs to be overrode in a child class."

    def get_raw(self, word_kanji, word_kana):
        eb_initialize_library()

        eb = EBTest('/home/illabout/temp/jp-dicts/JE - KenKyuSha 5th')
        eb.set_subbook(0)
        hits = eb.search(u"%s" % word_kanji)
        if not hits:
            return ''

        # if we have multiple hits, then we need to parse all of them
        # and see which one is the one we want
        raw = ''
        for hit in hits:
            result_heading = hit.heading()
            result_heading = self.replace_gaiji(result_heading)
            result_text = hit.text()
            result_text = self.replace_gaiji(result_text)

            raw = result_heading + "\n" + result_text
            kanji, kana, _ = self.parse_heading(raw)

            if word_kanji == kanji and (kana == word_kana or kana == u'?????????'):
                # we've found our match
                eb_finalize_library()
                return raw

        # we didn't find our match
        eb_finalize_library()
        return ''

    def lookup(self, word_kanji, word_kana, raw=None):
        """
        Lookup a word in a dictionary.

        word_kanji (unicode): the kanji you want to lookup
        word_kana (unicode): the kanji for the word you want to lookup
        raw (unicode): the source of the page we will parse to lookup the defintion.
        If raw is None, then we will fetch the page from the dictionary (possible the
        internet).

        Returns a Result object.  If no result could be found, then it returns
        a Result object with everything blank ("").
        """

        if raw is None:
            raw = self.get_raw(word_kanji, word_kana)

        if not raw:
            return Result(self, word_kanji, word_kana, '')

        kanji, kana, _ = self.parse_heading(raw)
        defs = self.parse_definition(raw)

        return Result(self, word_kanji, word_kana, '', kanji, kana, u'', defs)
