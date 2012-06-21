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

import ankiqt
import anki.lang

from PyQt4 import QtGui, QtCore

from . import anki_host

from .ui.mainfacteditorui import Ui_MainFactEditor
from .extrasentenceseditor import ExtraSentencesEditor

class MainFactEditor(QtGui.QMainWindow):

    def __init__(self, accent, def_string, main_sent, other_sents, word_kanji, word_kana,
            parent=None, factedit=None, fact=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.accent = accent
        self.def_string = def_string
        self.main_sent = main_sent
        self.other_sents = other_sents
        self.word_kanji = word_kanji
        self.word_kana = word_kana
        self.parent = parent
        self.factedit = factedit
        self.fact = fact

        self.ui = Ui_MainFactEditor()
        self.ui.setupUi(self)

        self.fillin()

    def exit(self):
        reply = QtGui.QMessageBox.question(self, 'Message',
                "Are you sure you want to quit?", QtGui.QMessageBox.Yes |
                QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            self.close()

    def okay(self):
        vocab = unicode(self.ui.vocab_lineEdit.text())
        vocabkana = unicode(self.ui.vocabkana_lineEdit.text())
        vocabenglish = unicode(self.ui.vocabenglish_textEdit.toPlainText())
        sentence = unicode(self.ui.sentence_textEdit.toPlainText())
        sentenceenglish = unicode(self.ui.sentenceenglish_textEdit.toPlainText())
        notes = unicode(self.ui.notes_textEdit.toPlainText())

        self.updatefact(vocabenglish, sentence, sentenceenglish, notes)
        self.close()

        if self.other_sents:
            self.extrasentenceseditorwindow = ExtraSentencesEditor(self.accent,
                    self.def_string, self.other_sents, self.word_kanji, self.word_kana,
                    parent=self.parent, factedit=self.factedit)
            self.extrasentenceseditorwindow.show()

    def updatefact(self, definition, sentence, sentenceenglish, notes):
        assert(isinstance(definition, unicode))
        assert(isinstance(sentence, unicode))
        assert(isinstance(sentenceenglish, unicode))
        assert(isinstance(notes, unicode))
        assert(isinstance(self.accent, unicode))
        assert(isinstance(self.word_kanji, unicode))
        assert(isinstance(self.word_kana, unicode))
        for jap_sent, eng_sent in self.other_sents:
            assert(isinstance(jap_sent, unicode))
            assert(isinstance(eng_sent, unicode))

        action = anki.lang._('Add')
        ankiqt.mw.deck.setUndoStart(action)

        self.factedit.saveFieldsNow()

        self.fact["VocabEnglish"] = u"%s" % anki_host.fieldtoanki(definition)
        self.fact["Sentence"] = u"%s" % anki_host.fieldtoanki(sentence)
        self.fact["SentenceEnglish"] = u"%s" % anki_host.fieldtoanki(sentenceenglish)
        self.fact["Notes"] = u"%s" % anki_host.fieldtoanki(notes)

        if self.accent != u"NO ACCENT":
            self.fact["Intonation"] = self.accent

        self.fact.setModified(textChanged=True, deck=ankiqt.mw.deck)
        ankiqt.mw.deck.setModified()
        self.factedit.loadFields()
        #ankiqt.mw.deck.flushMod()
        #ankiqt.mw.deck.save()
        #self.factedit.updateAfterCardChange()
        #self.factedit.saveFieldsNow()

        """
        for jap_sent, eng_sent in other_sentences:
            # get sentence model
            sentence_model = None
            for model in ankiqt.mw.deck.models:
                if model.name == "Sentences":
                    sentence_model = model
            assert(sentence_model is not None)

            fact = ankiqt.mw.deck.newFact(sentence_model)
            fact["Sentence"] = jap_sent
            fact["SentenceEnglish"] = eng_sent
            fact["Notes"] = u"「%s（%s）〔%s〕」：%s%s" % \
                    (self.word_kanji, self.word_kana, self.accent, jap_def, eng_def)

            ankiqt.mw.deck.addFact(fact)
        """

        ankiqt.mw.deck.setUndoEnd(action)
        ankiqt.mw.deck.rebuildCounts()
        ankiqt.mw.deck.s.flush()
        ankiqt.mw.deck.rebuildCSS()
        ankiqt.mw.deck.save()
        ankiqt.mw.reset()

    def fillin(self):
        self.ui.vocab_lineEdit.setText(self.word_kanji)
        self.ui.vocabkana_lineEdit.setText(self.word_kana)
        self.ui.vocabenglish_textEdit.setText(self.def_string)

        if self.main_sent:
            self.ui.sentence_textEdit.setText(self.main_sent[0])
            self.ui.sentenceenglish_textEdit.setText(self.main_sent[1])
        else:
            self.ui.sentence_textEdit.setText(u'')
            self.ui.sentenceenglish_textEdit.setText(u'')

        self.ui.notes_textEdit.setText(u'')
