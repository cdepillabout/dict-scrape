# -*- coding: UTF-8 -*-

import ankiqt
import anki.lang

from PyQt4 import QtGui, QtCore
from .ui.defeditorui import Ui_DefEditor
from .mainfacteditor import MainFactEditor

class DefEditor(QtGui.QMainWindow):
    def __init__(self, accent, defs, main_sent, other_sents, word_kanji, word_kana,
            standalone=True, parent=None, factedit=None, fact=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.accent = accent
        self.defs = defs
        self.main_sent = main_sent
        self.other_sents = other_sents
        self.word_kanji = word_kanji
        self.word_kana = word_kana
        self.standalone = standalone
        self.parent = parent
        self.factedit = factedit
        self.fact = fact

        self.ui = Ui_DefEditor()
        self.ui.setupUi(self)

        self.fillin(defs)

    def exit(self):
        reply = QtGui.QMessageBox.question(self, 'Message',
                "Are you sure you want to quit?", QtGui.QMessageBox.Yes |
                QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            self.close()

    def okay(self):
        editeddef = unicode(self.ui.def_textEdit.toPlainText())

        if self.standalone:
            print(u"Definition: (%s) %s" % (self.accent, editeddef))
            if self.main_sent:
                jp_sent, eng_sent = self.main_sent
                print(u"\nMAIN SENTENCE:\n%s\n%s" % (jp_sent, eng_sent))
            if self.other_sents:
                print(u"\nOTHER SENTENCES:")
                for jp_sent, eng_sent in self.other_sents:
                    print("%s\n%s" % (jp_sent, eng_sent))
            self.close()
        else:
            self.close()
            self.mainfacteditorwindow = MainFactEditor(self.accent, editeddef, self.main_sent,
                    self.other_sents, self.word_kanji, self.word_kana,
                    parent=self.parent, factedit=self.factedit, fact=self.fact)
            self.mainfacteditorwindow.show()

    def fillin(self, defs):

        def_text = u""

        previous_def_type = None
        for def_type, df in defs:
            if def_type == u"japdef" and previous_def_type == u"japdef":
                def_text += u"。%s" % df
            elif def_type == u"japdef" and previous_def_type == u"engdef":
                def_text += u"。%s" % df
            elif def_type == u"engdef" and previous_def_type == u"japdef":
                def_text += u"。%s" % df
            elif def_type == u"engdef" and previous_def_type == u"engdef":
                def_text += u", %s" % df
            else:
                # This is when there is no previous def_type
                def_text += u"%s" % df

            previous_def_type = def_type

        if previous_def_type == u"japdef":
            def_text += u"。"

        self.ui.def_textEdit.setText(def_text)
