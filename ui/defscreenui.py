# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'defscreen.ui'
#
# Created: Sun Jun  3 06:55:00 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui, QtWebKit
import diclist

class Ui_MainWindowReader(object):

    def createlist(self, verticallayoutobjectname, horizontallayoutobjectname,
            dictlabelobjectname, resultwordlabelobjectname, listobjectname, labeltext):
        verticallayout = QtGui.QVBoxLayout()
        verticallayout.setObjectName(verticallayoutobjectname)

        horizontallayout = QtGui.QHBoxLayout()
        horizontallayout.setObjectName(horizontallayoutobjectname)
        verticallayout.addLayout(horizontallayout)

        dictlabel = QtGui.QLabel(self.centralwidget)
        dictlabel.setObjectName(dictlabelobjectname)
        dictlabel.setText('<b>%s</b>' % labeltext)
        horizontallayout.addWidget(dictlabel)

        horizontallayout.addStretch()

        resultwordlabel = QtGui.QLabel(self.centralwidget)
        resultwordlabel.setObjectName(resultwordlabelobjectname)
        resultwordlabel.setText("")
        horizontallayout.addWidget(resultwordlabel)

        model = QtGui.QStandardItemModel()

        listwidget = QtGui.QListWidget(self.centralwidget)
        listwidget.setAlternatingRowColors(True)
        listwidget.setProperty("isWrapping", True)
        listwidget.setSpacing(2)
        listwidget.setUniformItemSizes(False)
        listwidget.setWordWrap(True)
        listwidget.setObjectName(listobjectname)
        listwidget.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        listwidget.setItemDelegate(diclist.DefListDelegate())
        dictlabel.setBuddy(listwidget)
        verticallayout.addWidget(listwidget)

        # don't return the horizontal layout
        return verticallayout, dictlabel, resultwordlabel, model, listwidget

    def createtab(self, tabobjectname, layoutobjectname, webviewobjectname):
        tab = QtGui.QWidget()
        tab.setObjectName(tabobjectname)
        tabvertlayout = QtGui.QVBoxLayout(tab)
        tabvertlayout.setObjectName(layoutobjectname)
        webview = QtWebKit.QWebView(tab)
        webview.setUrl(QtCore.QUrl("about:blank"))
        webview.setObjectName(webviewobjectname)
        tabvertlayout.addWidget(webview)

        return tab, tabvertlayout, webview

    def setupUi(self, mainwindowreader):
        self.mainwindowreader = mainwindowreader
        mainwindowreader.setObjectName("mainwindowreader")
        #mainwindowreader.resize(900, 650)
        #mainwindowreader.setAcceptDrops(False)
        #icon = QtGui.QIcon()
        #pixmap = QtGui.QPixmap("../img/logo32x32.png")
        #icon.addPixmap(pixmap, QtGui.QIcon.Normal, QtGui.QIcon.Off)
        #mainwindowreader.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(mainwindowreader)
        self.centralwidget.setObjectName("centralwidget")

        # main vertical layout that holds the tabwidget
        self.mainverticallayout = QtGui.QHBoxLayout(self.centralwidget)
        self.mainverticallayout.setObjectName("mainverticallayout")

        # tab widget
        self.tabwidget = QtGui.QTabWidget(self.centralwidget)
        self.tabwidget.setTabShape(QtGui.QTabWidget.Rounded)
        self.tabwidget.setObjectName("tabwidget")
        self.mainverticallayout.addWidget(self.tabwidget)

        # tab one.  this is our main definition page
        self.tabone = QtGui.QWidget()
        self.tabone.setObjectName("tabone")
        self.tabwidget.addTab(self.tabone, "Dictionary Results")

        # main vertical layout for tab one
        self.tabonevertlayout = QtGui.QVBoxLayout(self.tabone)
        self.tabonevertlayout.setObjectName("tabonevertlayout")


        # this is the horizontal layout that holds the two japanese dictionaries
        self.japdichorizlayout = QtGui.QHBoxLayout()
        self.japdichorizlayout.setObjectName("japdichorizlayout")

        self.daijisenverticallayout, self.daijisenlabel, self.daijisenresultwordlabel, \
                self.daijisenlistmodel, self.daijisenlist = self.createlist(
                        "daijisenverticallayout",
                        "daijisenhorizontallayout", "daijisenresultwordlabel",
                        "daijisenlabel", "daijisenlist", u'大辞泉')
        self.japdichorizlayout.addLayout(self.daijisenverticallayout)
        self.daijirinverticallayout, self.daijirinlabel, self.daijirinresultwordlabel, \
                self.daijirinlistmodel, self.daijirinlist = self.createlist(
                        "daijirinverticallayout",
                        "daijirinhorizontallayout", "daijirinresultwordlabel",
                        "daijirinlabel", "daijirinlist", u'大辞林')
        self.japdichorizlayout.addLayout(self.daijirinverticallayout)
        self.tabonevertlayout.addLayout(self.japdichorizlayout, 2)

        # this is the horizontal layout that holds the two english dictionaries
        self.engdichorizlayout = QtGui.QHBoxLayout()
        self.engdichorizlayout.setObjectName("engdichorizlayout")

        self.newcenturyvertlayout, self.newcenturylabel, self.newcenturyresultwordlabel, \
                self.newcenturylistmodel, self.newcenturylist = self.createlist(
                        "newcenturyvertlayout",
                        "newcenturyhorizontallayout", "newcenturyresultwordlabel",
                        "newcenturylabel", "newcenturylist", "New Century")
        self.engdichorizlayout.addLayout(self.newcenturyvertlayout)
        self.progressvertlayout, self.progresslabel, self.progressresultwordlabel, \
                self.progresslistmodel, self.progresslist = self.createlist(
                        "progressvertlayout",
                        "progresshorizontallayout", "progressresultwordlabel",
                        "progresslabel", "progresslist", "Progressive")
        self.engdichorizlayout.addLayout(self.progressvertlayout)
        self.tabonevertlayout.addLayout(self.engdichorizlayout, 3)

        # horizontal layout that holds the accent and OKAY/CANCEL buttons
        self.bottomhorizlayout = QtGui.QHBoxLayout()
        self.bottomhorizlayout.setObjectName("bottomhorizlayout")
        self.tabonevertlayout.addLayout(self.bottomhorizlayout)

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

        # four additional tabs for additional pages
        self.daijisentab, self.daijisentabvertlayout, self.daijisenwebview = self.createtab(
                "daijisentab", "daijisentabvertlayout", "daijisenwebview")
        self.tabwidget.addTab(self.daijisentab, u'大辞泉')
        self.daijirintab, self.daijirintabvertlayout, self.daijirinwebview = self.createtab(
                "daijirintab", "daijirintabvertlayout", "daijirinwebview")
        self.tabwidget.addTab(self.daijirintab, u'大辞林')
        self.newcentytab, self.newcentytabvertlayout, self.newcentywebview = self.createtab(
                "newcentytab", "newcentytabvertlayout", "newcentywebview")
        self.tabwidget.addTab(self.newcentytab, "New Century")
        self.progresstab, self.progresstabvertlayout, self.progresswebview = self.createtab(
                "progresstab", "progresstabvertlayout", "progresswebview")
        self.tabwidget.addTab(self.progresstab, "Progressive")

        mainwindowreader.setCentralWidget(self.centralwidget)
        mainwindowreader.setWindowTitle("JDicScrape")

        # new style signals
        self.buttonBox.accepted.connect(mainwindowreader.close)
        # old style signals
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"),
                mainwindowreader.close)

        # reset form
        self.buttonBox.button(QtGui.QDialogButtonBox.Reset).clicked.connect(self.resetclicked)

        # close window from menubar
        self.actionExit.triggered.connect(mainwindowreader.close)

        QtCore.QMetaObject.connectSlotsByName(mainwindowreader)

    def resetclicked(self, button):
        # this shows the sender (but in this case it will only be the reset button)
        #sender = self.mainwindowreader.sender()
        pass



if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    mainwindowreader = QtGui.QMainWindow()
    ui = Ui_MainWindowReader()
    ui.setupUi(mainwindowreader)
    mainwindowreader.show()
    sys.exit(app.exec_())

