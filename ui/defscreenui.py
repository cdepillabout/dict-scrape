# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'defscreen.ui'
#
# Created: Sun Jun  3 06:55:00 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindowReader(object):
    def setupUi(self, mainwindowreader):
        mainwindowreader.setObjectName(_fromUtf8("mainwindowreader"))
        mainwindowreader.resize(900, 650)
        mainwindowreader.setAcceptDrops(False)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("../img/logo32x32.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        mainwindowreader.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(mainwindowreader)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.daijisenverticallayout = QtGui.QVBoxLayout()
        self.daijisenverticallayout.setObjectName(_fromUtf8("daijisenverticallayout"))
        self.daijisenlabel = QtGui.QLabel(self.centralwidget)
        self.daijisenlabel.setObjectName(_fromUtf8("daijisenlabel"))
        self.daijisenverticallayout.addWidget(self.daijisenlabel)
        self.daijisenlist = QtGui.QListWidget(self.centralwidget)
        self.daijisenlist.setAlternatingRowColors(True)
        self.daijisenlist.setProperty("isWrapping", True)
        self.daijisenlist.setSpacing(2)
        self.daijisenlist.setUniformItemSizes(False)
        self.daijisenlist.setWordWrap(True)
        self.daijisenlist.setObjectName(_fromUtf8("daijisenlist"))
        self.daijisenverticallayout.addWidget(self.daijisenlist)
        self.horizontalLayout.addLayout(self.daijisenverticallayout)
        self.daijirinverticallayout = QtGui.QVBoxLayout()
        self.daijirinverticallayout.setObjectName(_fromUtf8("daijirinverticallayout"))
        self.daijirinlabel = QtGui.QLabel(self.centralwidget)
        self.daijirinlabel.setObjectName(_fromUtf8("daijirinlabel"))
        self.daijirinverticallayout.addWidget(self.daijirinlabel)
        self.daijirinlist = QtGui.QListWidget(self.centralwidget)
        self.daijirinlist.setAlternatingRowColors(True)
        self.daijirinlist.setProperty("isWrapping", True)
        self.daijirinlist.setSpacing(2)
        self.daijirinlist.setUniformItemSizes(False)
        self.daijirinlist.setWordWrap(True)
        self.daijirinlist.setObjectName(_fromUtf8("daijirinlist"))
        self.daijirinverticallayout.addWidget(self.daijirinlist)
        self.horizontalLayout.addLayout(self.daijirinverticallayout)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.newcenturylabel = QtGui.QLabel(self.centralwidget)
        self.newcenturylabel.setObjectName(_fromUtf8("newcenturylabel"))
        self.verticalLayout_2.addWidget(self.newcenturylabel)
        self.newcenturylist = QtGui.QListWidget(self.centralwidget)
        self.newcenturylist.setObjectName(_fromUtf8("newcenturylist"))
        self.verticalLayout_2.addWidget(self.newcenturylist)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.progressivelabel = QtGui.QLabel(self.centralwidget)
        self.progressivelabel.setObjectName(_fromUtf8("progressivelabel"))
        self.verticalLayout_3.addWidget(self.progressivelabel)
        self.progressivelist = QtGui.QListWidget(self.centralwidget)
        self.progressivelist.setObjectName(_fromUtf8("progressivelist"))
        self.verticalLayout_3.addWidget(self.progressivelist)
        self.horizontalLayout_2.addLayout(self.verticalLayout_3)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout_4.addLayout(self.verticalLayout)
        mainwindowreader.setCentralWidget(self.centralwidget)

        self.retranslateUi(mainwindowreader)
        QtCore.QMetaObject.connectSlotsByName(mainwindowreader)

    def retranslateUi(self, mainwindowreader):
        mainwindowreader.setWindowTitle(QtGui.QApplication.translate("mainwindowreader", "JDicScrape", None, QtGui.QApplication.UnicodeUTF8))
        self.daijisenlabel.setText(QtGui.QApplication.translate("mainwindowreader", "大辞泉", None, QtGui.QApplication.UnicodeUTF8))
        self.daijirinlabel.setText(QtGui.QApplication.translate("mainwindowreader", "大辞林", None, QtGui.QApplication.UnicodeUTF8))
        self.newcenturylabel.setText(QtGui.QApplication.translate("mainwindowreader", "New Century", None, QtGui.QApplication.UnicodeUTF8))
        self.progressivelabel.setText(QtGui.QApplication.translate("mainwindowreader", "Progressive", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    mainwindowreader = QtGui.QMainWindow()
    ui = Ui_MainWindowReader()
    ui.setupUi(mainwindowreader)
    mainwindowreader.show()
    sys.exit(app.exec_())

