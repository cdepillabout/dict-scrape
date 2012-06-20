# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

class Ui_DefEditor(object):
    def setupUi(self, defeditor):
        defeditor.setObjectName(u"defeditor")
        defeditor.resize(800, 600)

        self.centralwidget = QtGui.QWidget(defeditor)
        self.centralwidget.setObjectName(u"centralwidget")
        defeditor.setCentralWidget(self.centralwidget)

        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        #self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(u"verticalLayout")

        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.verticalLayout.addLayout(self.formLayout)

        self.japdef_textEdit = QtGui.QTextEdit(self.centralwidget)
        self.japdef_textEdit.setObjectName(u"japdef_textEdit")
        self.formLayout.addRow(u"Edit Jap Def:", self.japdef_textEdit)

        self.engdef_textEdit = QtGui.QTextEdit(self.centralwidget)
        self.engdef_textEdit.setObjectName(u"engdef_textEdit")
        self.formLayout.addRow(u"Edit Eng Def:", self.engdef_textEdit)

        #self.sentencepicker_comboBox = QtGui.QComboBox(self.centralwidget)
        #self.sentencepicker_comboBox.setObjectName(u"sentencepicker_comboBox")
        #self.formLayout.addRow(u"Main Sentence:", self.sentencepicker_comboBox)

        self.sentencepicker_listWidget = QtGui.QListWidget(self.centralwidget)
        self.sentencepicker_listWidget.setObjectName("sentencepicker_listWidget")
        self.formLayout.addRow(u"Main Sentence:", self.sentencepicker_listWidget)

        self.buttonBox = QtGui.QDialogButtonBox(self.centralwidget)
        self.buttonBox.setStandardButtons(
                QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(u"buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        # okay button (new style signals)
        self.buttonBox.accepted.connect(defeditor.okay)
        self.buttonBox.rejected.connect(defeditor.exit)

        QtCore.QMetaObject.connectSlotsByName(defeditor)
