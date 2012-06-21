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

from .ui.extrasentenceseditorui import Ui_ExtraSentencesEditor

class ExtraSentencesEditor(QtGui.QMainWindow):
    def __init__(self, accent, def_string, other_sents, word_kanji, word_kana,
            parent=None, factedit=None):
        assert(other_sents)
        assert(len(other_sents) >= 1)
        QtGui.QMainWindow.__init__(self, parent)
        self.accent = accent
        self.def_string = def_string
        self.other_sents = other_sents
        self.word_kanji = word_kanji
        self.word_kana = word_kana
        self.parent = parent
        self.factedit = factedit

        self.ui = Ui_ExtraSentencesEditor()
        self.ui.setupUi(self)

        self.fillin()

    def exit(self):
        reply = QtGui.QMessageBox.question(self, 'Message',
                "Are you sure you want to quit?", QtGui.QMessageBox.Yes |
                QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            self.close()

    def okay(self):
        sentence = unicode(self.ui.sentence_textEdit.toPlainText())
        sentenceenglish = unicode(self.ui.sentenceenglish_textEdit.toPlainText())
        notes = unicode(self.ui.notes_textEdit.toPlainText())

        self.addNewSentence(sentence, sentenceenglish, notes)
        self.close()

        if len(self.other_sents) > 1:
            self.extrasentenceseditorwindow = ExtraSentencesEditor(self.accent,
                    self.def_string, self.other_sents[1:], self.word_kanji, self.word_kana,
                    parent=self.parent, factedit=self.factedit)
            self.extrasentenceseditorwindow.show()


    def addNewSentence(self, sentence, sentenceenglish, notes):
        assert(isinstance(sentence, unicode))
        assert(isinstance(sentenceenglish, unicode))
        assert(isinstance(notes, unicode))

        action = anki.lang._(u'Add')
        ankiqt.mw.deck.setUndoStart(action)

        # get sentence model
        sentence_model = None
        for model in ankiqt.mw.deck.models:
            if model.name == u"Sentences":
                sentence_model = model
        assert(sentence_model is not None)

        fact = ankiqt.mw.deck.newFact(sentence_model)
        fact[u"Sentence"] = anki_host.fieldtoanki(sentence)
        fact[u"SentenceEnglish"] = anki_host.fieldtoanki(sentenceenglish)
        fact[u"Notes"] = anki_host.fieldtoanki(notes)

        ankiqt.mw.deck.addFact(fact)

        ankiqt.mw.deck.setUndoEnd(action)
        ankiqt.mw.deck.setModified()
        ankiqt.mw.deck.rebuildCounts()
        ankiqt.mw.deck.s.flush()
        ankiqt.mw.deck.rebuildCSS()
        ankiqt.mw.deck.save()
        ankiqt.mw.reset()

    def fillin(self):
        jap_sent, eng_sent = self.other_sents[0]

        self.ui.sentence_textEdit.setText(jap_sent)
        self.ui.sentenceenglish_textEdit.setText(eng_sent)

        notes_text = u'「%s（%s）〔%s〕」：%s' % \
                (self.word_kanji, self.word_kana, self.accent, self.def_string)

        self.ui.notes_textEdit.setText(notes_text)

