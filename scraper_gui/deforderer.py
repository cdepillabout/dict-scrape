# -*- coding: UTF-8 -*-

import ankiqt
import anki.lang

from PyQt4 import QtGui, QtCore
from .ui.defordererui import Ui_DefOrderer
from .defeditor import DefEditor

class DefOrderer(QtGui.QMainWindow):
    def __init__(self, accent, jap_defs, eng_defs, example_sentences, word_kanji, word_kana,
            standalone=True, parent=None, factedit=None, fact=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.accent = accent
        self.jap_defs = jap_defs
        self.eng_defs = eng_defs
        self.example_sentences = example_sentences
        self.word_kanji = word_kanji
        self.word_kana = word_kana
        self.standalone = standalone
        self.parent = parent
        self.factedit = factedit
        self.fact = fact

        self.ui = Ui_DefOrderer()
        self.ui.setupUi(self)

        self.fillin(jap_defs, eng_defs, example_sentences)

    def exit(self):
        reply = QtGui.QMessageBox.question(self, 'Message',
                "Are you sure you want to quit?", QtGui.QMessageBox.Yes |
                QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            self.close()

    def okay(self):

        count = self.ui.deforder_listWidget.count()
        defs = []
        for i in range(count):
            item = self.ui.deforder_listWidget.item(i)
            # deftype should be either "japdef" or "engdef"
            deftype, df = item.data(QtCore.Qt.UserRole).toPyObject()
            deftype = unicode(deftype)
            df = unicode(df)
            defs.append([deftype, df])

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

        self.close()
        self.defeditorwindow = DefEditor(self.accent, defs, selected_sent, other_sents,
                self.word_kanji, self.word_kana, standalone=self.standalone,
                parent=self.parent, factedit=self.factedit, fact=self.fact)
        self.defeditorwindow.show()

    def fillin(self, jap_defs, eng_defs, example_sentences):
        for shortdef in jap_defs:
            item = QtGui.QListWidgetItem()
            item.setData(QtCore.Qt.UserRole, ["japdef", shortdef])
            item.setText(shortdef)
            self.ui.deforder_listWidget.addItem(item)

        for shortdef in eng_defs:
            item = QtGui.QListWidgetItem()
            item.setData(QtCore.Qt.UserRole, ["engdef", shortdef])
            item.setText(shortdef)
            self.ui.deforder_listWidget.addItem(item)

        for i, (jap_sent, eng_sent) in enumerate(example_sentences):
            item = QtGui.QListWidgetItem()
            item.setData(QtCore.Qt.UserRole, [jap_sent, eng_sent])
            item.setText(jap_sent)
            self.ui.sentencepicker_listWidget.addItem(item)

            # set the first item as selected
            if i == 0:
                self.ui.sentencepicker_listWidget.setItemSelected(item, True)
