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
        #mainwindowreader.setAcceptDrops(False)
        #icon = QtGui.QIcon()
        #pixmap = QtGui.QPixmap("../img/logo32x32.png")
        #icon.addPixmap(pixmap, QtGui.QIcon.Normal, QtGui.QIcon.Off)
        #mainwindowreader.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(mainwindowreader)
        self.centralwidget.setObjectName("centralwidget")

        self.mainverticallayout = QtGui.QVBoxLayout()
        self.mainverticallayout.setObjectName("mainverticallayout")

        # this is the horizontal layout that holds the two japanese dictionaries
        self.japdichorizlayout = QtGui.QHBoxLayout()
        self.japdichorizlayout.setObjectName("japdichorizlayout")
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
        self.japdichorizlayout.addLayout(self.daijisenverticallayout)
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
        self.japdichorizlayout.addLayout(self.daijirinverticallayout)
        self.mainverticallayout.addLayout(self.japdichorizlayout)


        # this is the horizontal layout that holds the two english dictionaries
        self.engdichorizlayout = QtGui.QHBoxLayout()
        self.engdichorizlayout.setObjectName("engdichorizlayout")
        self.newcenturyvertlayout = QtGui.QVBoxLayout()
        self.newcenturyvertlayout.setObjectName("newcenturyvertlayout")
        self.newcenturylabel = QtGui.QLabel(self.centralwidget)
        self.newcenturylabel.setObjectName("newcenturylabel")
        self.newcenturyvertlayout.addWidget(self.newcenturylabel)
        self.newcenturylist = QtGui.QListWidget(self.centralwidget)
        self.newcenturylist.setObjectName("newcenturylist")
        self.newcenturyvertlayout.addWidget(self.newcenturylist)
        self.engdichorizlayout.addLayout(self.newcenturyvertlayout)
        self.progressivevertlayout = QtGui.QVBoxLayout()
        self.progressivevertlayout.setObjectName("progressivevertlayout")
        self.progressivelabel = QtGui.QLabel(self.centralwidget)
        self.progressivelabel.setObjectName("progressivelabel")
        self.progressivevertlayout.addWidget(self.progressivelabel)
        self.progressivelist = QtGui.QListWidget(self.centralwidget)
        self.progressivelist.setObjectName("progressivelist")
        self.progressivevertlayout.addWidget(self.progressivelist)
        self.engdichorizlayout.addLayout(self.progressivevertlayout)
        self.mainverticallayout.addLayout(self.engdichorizlayout)


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

