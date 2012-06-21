# -*- coding: UTF-8 -*-

import ankiqt
import anki.lang

from PyQt4 import QtGui, QtCore
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

        #self.addNewSentence(sentence, sentenceenglish, notes)
        self.close()

        if len(self.other_sents) > 1:
            self.extrasentenceseditorwindow = ExtraSentencesEditor(self.accent,
                    self.def_string, self.other_sents[1:], self.word_kanji, self.word_kana,
                    parent=self.parent, factedit=self.factedit)
            self.extrasentenceseditorwindow.show()


    def addNewSentence(self, definition, sentence, sentenceenglish, notes):
        return

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

        self.fact["VocabEnglish"] = u"%s" % definition
        self.fact["Sentence"] = u"%s" % sentence
        self.fact["SentenceEnglish"] = u"%s" % sentenceenglish

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
        jap_sent, eng_sent = self.other_sents[0]

        self.ui.sentence_textEdit.setText(jap_sent)
        self.ui.sentenceenglish_textEdit.setText(eng_sent)

        notes_text = u'「%s（%s）〔%s〕」：%s' % \
                (self.word_kanji, self.word_kana, self.accent, self.def_string)

        self.ui.notes_textEdit.setText(notes_text)

