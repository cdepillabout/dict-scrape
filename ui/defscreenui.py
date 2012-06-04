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
        #mainwindowreader.resize(900, 650)
        #mainwindowreader.setAcceptDrops(False)
        #icon = QtGui.QIcon()
        #pixmap = QtGui.QPixmap("../img/logo32x32.png")
        #icon.addPixmap(pixmap, QtGui.QIcon.Normal, QtGui.QIcon.Off)
        #mainwindowreader.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(mainwindowreader)
        self.centralwidget.setObjectName("centralwidget")

        self.mainverticallayout = QtGui.QVBoxLayout(self.centralwidget)
        self.mainverticallayout.setObjectName("mainverticallayout")

        # this is the horizontal layout that holds the two japanese dictionaries
        self.japdichorizlayout = QtGui.QHBoxLayout()
        self.japdichorizlayout.setObjectName("japdichorizlayout")
        self.daijisenverticallayout = QtGui.QVBoxLayout()
        self.daijisenverticallayout.setObjectName("daijisenverticallayout")
        self.daijisenlabel = QtGui.QLabel(self.centralwidget)
        self.daijisenlabel.setObjectName("daijisenlabel")
        self.daijisenlabel.setText("大辞泉".decode("utf8"))
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
        self.daijirinlabel.setText("大辞林".decode("utf8"))
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
        self.mainverticallayout.addLayout(self.japdichorizlayout, 2)


        # this is the horizontal layout that holds the two english dictionaries
        self.engdichorizlayout = QtGui.QHBoxLayout()
        self.engdichorizlayout.setObjectName("engdichorizlayout")
        self.newcenturyvertlayout = QtGui.QVBoxLayout()
        self.newcenturyvertlayout.setObjectName("newcenturyvertlayout")
        self.newcenturylabel = QtGui.QLabel(self.centralwidget)
        self.newcenturylabel.setObjectName("newcenturylabel")
        self.newcenturylabel.setText("New Century")
        self.newcenturyvertlayout.addWidget(self.newcenturylabel)
        self.newcenturylist = QtGui.QListWidget(self.centralwidget)
        self.newcenturylist.setObjectName("newcenturylist")
        self.newcenturyvertlayout.addWidget(self.newcenturylist)
        self.engdichorizlayout.addLayout(self.newcenturyvertlayout)
        self.progressivevertlayout = QtGui.QVBoxLayout()
        self.progressivevertlayout.setObjectName("progressivevertlayout")
        self.progressivelabel = QtGui.QLabel(self.centralwidget)
        self.progressivelabel.setObjectName("progressivelabel")
        self.progressivelabel.setText("Progressive")
        self.progressivevertlayout.addWidget(self.progressivelabel)
        self.progressivelist = QtGui.QListWidget(self.centralwidget)
        self.progressivelist.setObjectName("progressivelist")
        self.progressivevertlayout.addWidget(self.progressivelist)
        self.engdichorizlayout.addLayout(self.progressivevertlayout)
        self.mainverticallayout.addLayout(self.engdichorizlayout, 3)

        # horizontal layout that holds the accent and OKAY/CANCEL buttons
        self.bottomhorizlayout = QtGui.QHBoxLayout()
        self.bottomhorizlayout.setObjectName("bottomhorizlayout")
        self.mainverticallayout.addLayout(self.bottomhorizlayout)

        # accent stuff
        self.accentlabel = QtGui.QLabel(self.centralwidget)
        self.accentlabel.setObjectName("accentlabel")
        self.accentlabel.setText("Accent")
        self.bottomhorizlayout.addWidget(self.accentlabel)
        self.accentlineedit = QtGui.QLineEdit(self.centralwidget)
        self.accentlineedit.setObjectName("accentlineedit")
        self.accentlineedit.setReadOnly(True)
        self.bottomhorizlayout.addWidget(self.accentlineedit)
        self.useaccentcheckbox = QtGui.QCheckBox(self.centralwidget)
        self.useaccentcheckbox.setObjectName("useaccentcheckbox")
        self.useaccentcheckbox.setText("Use Accent")
        self.bottomhorizlayout.addWidget(self.useaccentcheckbox)

        # spacer
        self.bottomhorizlayout.addStretch()

        # button box
        self.buttonBox = QtGui.QDialogButtonBox(self.centralwidget)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok|QtGui.QDialogButtonBox.Reset)
        self.buttonBox.setObjectName("buttonBox")
        self.bottomhorizlayout.addWidget(self.buttonBox)


        # status bar
        self.statusbar = QtGui.QStatusBar(mainwindowreader)
        self.statusbar.setObjectName("statusbar")
        mainwindowreader.setStatusBar(self.statusbar)

        # menubar
        self.menuBar = QtGui.QMenuBar(mainwindowreader)
        self.menuBar.setObjectName("menuBar")
        self.menuFile = QtGui.QMenu(self.menuBar)
        self.menuFile.setObjectName("menuFile")
        self.menuFile.setTitle("File")
        mainwindowreader.setMenuBar(self.menuBar)

        self.actionExit = QtGui.QAction(mainwindowreader)
        self.actionExit.setEnabled(True)
        self.actionExit.setObjectName("actionExit")
        self.actionExit.setText("Exit")
        self.menuFile.addAction(self.actionExit)
        self.menuBar.addAction(self.menuFile.menuAction())


        mainwindowreader.setCentralWidget(self.centralwidget)
        mainwindowreader.setWindowTitle("JDicScrape")

        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"),
                mainwindowreader.close)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"),
                mainwindowreader.showFullScreen)
        QtCore.QMetaObject.connectSlotsByName(mainwindowreader)


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    mainwindowreader = QtGui.QMainWindow()
    ui = Ui_MainWindowReader()
    ui.setupUi(mainwindowreader)
    mainwindowreader.show()
    sys.exit(app.exec_())

