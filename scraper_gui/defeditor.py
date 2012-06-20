# -*- coding: UTF-8 -*-

import ankiqt
import anki.lang

from PyQt4 import QtGui, QtCore
from .ui.defeditorui import Ui_DefEditor

class DefEditor(QtGui.QMainWindow):
    def __init__(self, accent, jap_def, eng_def, example_sentences, word_kanji, word_kana,
            standalone=True, parent=None, factedit=None, fact=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.accent = accent
        self.jap_def = jap_def
        self.eng_def = eng_def
        self.example_sentences = example_sentences
        self.word_kanji = word_kanji
        self.word_kana = word_kana
        self.standalone = standalone
        self.parent = parent
        self.factedit = factedit
        self.fact = fact
        self.ui = Ui_DefEditor()
        self.ui.setupUi(self)

        self.fillin(jap_def, eng_def, example_sentences)

    def exit(self):
        reply = QtGui.QMessageBox.question(self, 'Message',
                "Are you sure you want to quit?", QtGui.QMessageBox.Yes |
                QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            self.close()

    def okay(self):
        jap_def = unicode(self.ui.japdef_textEdit.toPlainText())
        eng_def = unicode(self.ui.engdef_textEdit.toPlainText())

        selected_sent = None
        other_sents = []
        count = self.ui.sentencepicker_listWidget.count()
        for i in range(count):
            item = self.ui.sentencepicker_listWidget.item(i)
            jap_sent, eng_sent = item.data(QtCore.Qt.UserRole).toPyObject()
            jap_sent = unicode(jap_sent)
            eng_sent = unicode(eng_sent)
            if item.isSelected():
                assert(selected_sent is None)
                selected_sent = [jap_sent, eng_sent]
            else:
                other_sents.append([jap_sent, eng_sent])

        # make sure there are no other sentences if we don't have a selected sentence
        if other_sents:
            assert(selected_sent)

        if self.standalone:
            print("Definition: (%s) %s%s" % (self.accent, jap_def, eng_def))
            if selected_sent:
                jp_sent, eng_sent = selected_sent
                print("\nMAIN SENTENCE:\n%s\n%s" % (jp_sent, eng_sent))
            if other_sents:
                print("\nOTHER SENTENCES:")
                for jp_sent, eng_sent in other_sents:
                    print("%s\n%s" % (jp_sent, eng_sent))
        else:
            self.updatefact(jap_def, eng_def, selected_sent, other_sents)

        self.close()

    def updatefact(self, jap_def, eng_def="", main_sentence=[], other_sentences=[]):
        if main_sentence:
            main_jap_sent, main_eng_sent = main_sentence
        else:
            main_jap_sent = u""
            main_eng_sent = u""

        assert(isinstance(self.accent, unicode))
        assert(isinstance(self.word_kanji, unicode))
        assert(isinstance(self.word_kana, unicode))
        assert(isinstance(jap_def, unicode))
        assert(isinstance(eng_def, unicode))
        assert(isinstance(main_jap_sent, unicode))
        assert(isinstance(main_eng_sent, unicode))
        for jap_sent, eng_sent in other_sentences:
            assert(isinstance(jap_sent, unicode))
            assert(isinstance(eng_sent, unicode))

        action = anki.lang._('Add')
        ankiqt.mw.deck.setUndoStart(action)

        self.factedit.saveFieldsNow()

        self.fact["VocabEnglish"] = u"%s%s" % (jap_def, eng_def)
        if main_sentence:
            self.fact["Sentence"] = u"%s" % main_jap_sent
            self.fact["SentenceEnglish"] = u"%s" % main_eng_sent

        if self.accent != u"NO ACCENT":
            self.fact["Intonation"] = self.accent

        self.fact.setModified(textChanged=True, deck=ankiqt.mw.deck)
        ankiqt.mw.deck.setModified()
        self.factedit.loadFields()
        #ankiqt.mw.deck.flushMod()
        #ankiqt.mw.deck.save()
        #self.factedit.updateAfterCardChange()
        #self.factedit.saveFieldsNow()

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

        ankiqt.mw.deck.setUndoEnd(action)
        ankiqt.mw.deck.rebuildCounts()
        ankiqt.mw.deck.s.flush()
        ankiqt.mw.deck.rebuildCSS()
        ankiqt.mw.deck.save()
        ankiqt.mw.reset()


    def fillin(self, jap_def, eng_def, example_sentences):
        self.ui.japdef_textEdit.setText(jap_def)
        self.ui.engdef_textEdit.setText(eng_def)

        for i, (jap_sent, eng_sent) in enumerate(example_sentences):
            item = QtGui.QListWidgetItem()
            item.setData(QtCore.Qt.UserRole, [jap_sent, eng_sent])
            item.setText(jap_sent)
            self.ui.sentencepicker_listWidget.addItem(item)

            # set the first item as selected
            if i == 0:
                self.ui.sentencepicker_listWidget.setItemSelected(item, True)
