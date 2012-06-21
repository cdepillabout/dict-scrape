# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

class Ui_ExtraSentencesEditor(object):
    def setupUi(self, extrasentenceseditor):
        extrasentenceseditor.setObjectName(u"extrasentenceseditor")
        extrasentenceseditor.resize(900, 650)

        self.centralwidget = QtGui.QWidget(extrasentenceseditor)
        self.centralwidget.setObjectName(u"centralwidget")
        extrasentenceseditor.setCentralWidget(self.centralwidget)

        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")

        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setFormAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout.addLayout(self.formLayout, 1)

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

        self.buttonBox.accepted.connect(extrasentenceseditor.okay)
        self.buttonBox.rejected.connect(extrasentenceseditor.exit)

        QtCore.QMetaObject.connectSlotsByName(extrasentenceseditor)


