# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

class Ui_DefOrderer(object):
    def setupUi(self, defeditor):
        defeditor.setObjectName(u"deforderer")
        defeditor.resize(900, 650)

        self.centralwidget = QtGui.QWidget(defeditor)
        self.centralwidget.setObjectName(u"centralwidget")
        defeditor.setCentralWidget(self.centralwidget)

        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        #self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(u"verticalLayout")

        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setFormAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout.addLayout(self.formLayout)

        self.deforder_listWidget = QtGui.QListWidget(self.centralwidget)
        self.deforder_listWidget.setObjectName("deforder_listWidget")
        #self.deforder_listWidget.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.deforder_listWidget.setDragDropMode(QtGui.QListWidget.InternalMove)
        self.formLayout.addRow(u"Def Order:", self.deforder_listWidget)

        self.sentencepicker_listWidget = QtGui.QListWidget(self.centralwidget)
        self.sentencepicker_listWidget.setObjectName("sentencepicker_listWidget")
        self.sentencepicker_listWidget.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
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

