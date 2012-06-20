# -*- coding: UTF-8 -*-

import ankiqt

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
        self.close()

    def fillin(self, jap_def, eng_def, example_sentences):
        self.ui.japdef_textEdit.setText(jap_def)
        self.ui.engdef_textEdit.setText(eng_def)
        for jap_sent, eng_sent in example_sentences:
            #self.ui.sentencepicker_comboBox.addItem(jap_sent, [jap_sent, eng_sent])
            item = QtGui.QListWidgetItem()
            item.setData(QtCore.Qt.UserRole, [jap_sent, eng_sent])
            item.setText(jap_sent)
            self.ui.sentencepicker_listWidget.addItem(item)
