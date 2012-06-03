# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'defscreen.ui'
#
# Created: Sun Jun  3 06:55:00 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindowReader(object):
    def setupUi(self, mainwindowreader):
        mainwindowreader.setObjectName("mainwindowreader")
        mainwindowreader.resize(900, 650)
        mainwindowreader.setAcceptDrops(False)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../img/logo32x32.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        mainwindowreader.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(mainwindowreader)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.daijisenverticallayout = QtGui.QVBoxLayout()
        self.daijisenverticallayout.setObjectName("daijisenverticallayout")
        self.daijisenlabel = QtGui.QLabel(self.centralwidget)
        self.daijisenlabel.setObjectName("daijisenlabel")
        self.daijisenverticallayout.addWidget(self.daijisenlabel)
        self.daijisenlist = QtGui.QListWidget(self.centralwidget)
        self.daijisenlist.setAlternatingRowColors(True)
        self.daijisenlist.setProperty("isWrapping", True)
        self.daijisenlist.setSpacing(2)
        self.daijisenlist.setUniformItemSizes(False)
        self.daijisenlist.setWordWrap(True)
        self.daijisenlist.setObjectName("daijisenlist")
        self.daijisenverticallayout.addWidget(self.daijisenlist)
        self.horizontalLayout.addLayout(self.daijisenverticallayout)
        self.daijirinverticallayout = QtGui.QVBoxLayout()
        self.daijirinverticallayout.setObjectName("daijirinverticallayout")
        self.daijirinlabel = QtGui.QLabel(self.centralwidget)
        self.daijirinlabel.setObjectName("daijirinlabel")
        self.daijirinverticallayout.addWidget(self.daijirinlabel)
        self.daijirinlist = QtGui.QListWidget(self.centralwidget)
        self.daijirinlist.setAlternatingRowColors(True)
        self.daijirinlist.setProperty("isWrapping", True)
        self.daijirinlist.setSpacing(2)
        self.daijirinlist.setUniformItemSizes(False)
        self.daijirinlist.setWordWrap(True)
        self.daijirinlist.setObjectName("daijirinlist")
        self.daijirinverticallayout.addWidget(self.daijirinlist)
        self.horizontalLayout.addLayout(self.daijirinverticallayout)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.newcenturylabel = QtGui.QLabel(self.centralwidget)
        self.newcenturylabel.setObjectName("newcenturylabel")
        self.verticalLayout_2.addWidget(self.newcenturylabel)
        self.newcenturylist = QtGui.QListWidget(self.centralwidget)
        self.newcenturylist.setObjectName("newcenturylist")
        self.verticalLayout_2.addWidget(self.newcenturylist)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.progressivelabel = QtGui.QLabel(self.centralwidget)
        self.progressivelabel.setObjectName("progressivelabel")
        self.verticalLayout_3.addWidget(self.progressivelabel)
        self.progressivelist = QtGui.QListWidget(self.centralwidget)
        self.progressivelist.setObjectName("progressivelist")
        self.verticalLayout_3.addWidget(self.progressivelist)
        self.horizontalLayout_2.addLayout(self.verticalLayout_3)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout_4.addLayout(self.verticalLayout)
        mainwindowreader.setCentralWidget(self.centralwidget)

        mainwindowreader.setWindowTitle("JDicScrape")
        self.daijisenlabel.setText("大辞泉".decode("utf8"))
        self.daijirinlabel.setText("大辞林".decode("utf8"))
        self.newcenturylabel.setText("New Century")
        self.progressivelabel.setText("Progressive")

        QtCore.QMetaObject.connectSlotsByName(mainwindowreader)

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    mainwindowreader = QtGui.QMainWindow()
    ui = Ui_MainWindowReader()
    ui.setupUi(mainwindowreader)
    mainwindowreader.show()
    sys.exit(app.exec_())

