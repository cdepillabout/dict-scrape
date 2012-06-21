# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

class Ui_MainFactEditor(object):
    def setupUi(self, defeditor):
        defeditor.setObjectName(u"defeditor")
        defeditor.resize(900, 650)

        self.centralwidget = QtGui.QWidget(defeditor)
        self.centralwidget.setObjectName(u"centralwidget")
        defeditor.setCentralWidget(self.centralwidget)

        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")

        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setFormAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout.addLayout(self.formLayout, 1)

        self.vocab_lineEdit = QtGui.QLineEdit(self.centralwidget)
        self.vocab_lineEdit.setObjectName(u"vocab_lineEdit")
        self.formLayout.addRow(u"Vocab:", self.vocab_lineEdit)

        self.vocabkana_lineEdit = QtGui.QLineEdit(self.centralwidget)
        self.vocabkana_lineEdit.setObjectName(u"vocabkana_lineEdit")
        self.formLayout.addRow(u"Vocab Kana:", self.vocabkana_lineEdit)

        self.vocabenglish_textEdit = QtGui.QTextEdit(self.centralwidget)
        self.vocabenglish_textEdit.setObjectName(u"vocabenglish_textEdit")
        self.formLayout.addRow(u"Vocab English:", self.vocabenglish_textEdit)

        self.sentence_textEdit = QtGui.QTextEdit(self.centralwidget)
        self.sentence_textEdit.setObjectName(u"sentence_textEdit")
        self.formLayout.addRow(u"Sentence:", self.sentence_textEdit)

        self.sentenceenglish_textEdit = QtGui.QTextEdit(self.centralwidget)
        self.sentenceenglish_textEdit.setObjectName(u"sentenceenglish_textEdit")
        self.formLayout.addRow(u"Sentence English:", self.sentenceenglish_textEdit)

        self.notes_textEdit = QtGui.QTextEdit(self.centralwidget)
        self.notes_textEdit.setObjectName(u"notes_textEdit")
        self.formLayout.addRow(u"Notes:", self.notes_textEdit)

        self.buttonBox = QtGui.QDialogButtonBox(self.centralwidget)
        self.buttonBox.setStandardButtons(
                QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(u"buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.buttonBox.accepted.connect(defeditor.okay)
        self.buttonBox.rejected.connect(defeditor.exit)

        QtCore.QMetaObject.connectSlotsByName(defeditor)

