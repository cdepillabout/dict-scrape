# -*- coding: utf-8 -*-

# Copyright (C) 2012  Dennis Gosnell
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from PyQt4 import QtCore, QtGui, QtWebKit

from .defwebviewui import DefWebView

class Ui_MainWindowSelector(object):

    def createlist(self, verticallayoutobjectname, horizontallayoutobjectname,
            dictlabelobjectname, resultwordlabelobjectname, webviewobjectname, labeltext):
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

        webview = DefWebView(self.centralwidget)
        webview.setObjectName(webviewobjectname)
        webview.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        dictlabel.setBuddy(webview)
        verticallayout.addWidget(webview)

        #textedit.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        #textedit.customContextMenuRequested.connect(textedit.lalalala)

        # don't return the horizontal layout
        return verticallayout, dictlabel, resultwordlabel, webview

    def create_debug_tab(self, tabobjectname, layoutobjectname, webviewobjectname):
        tab = QtGui.QWidget()
        tab.setObjectName(tabobjectname)
        tabvertlayout = QtGui.QVBoxLayout(tab)
        tabvertlayout.setObjectName(layoutobjectname)
        webview = QtWebKit.QWebView(tab)
        webview.setUrl(QtCore.QUrl("about:blank"))
        webview.setObjectName(webviewobjectname)
        tabvertlayout.addWidget(webview)

        return tab, tabvertlayout, webview

    def create_accent_box(self, mainvertlayout):
        # horizontal layout that holds the accent and OKAY/CANCEL buttons
        self.bottomhorizlayout = QtGui.QHBoxLayout()
        self.bottomhorizlayout.setObjectName("bottomhorizlayout")
        mainvertlayout.addLayout(self.bottomhorizlayout)

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


    def create_yahoo_tab(self, yahoo_dics_tab):
        # main vertical layout for tab one
        self.yahoo_dics_tab_vert_layout = QtGui.QVBoxLayout(yahoo_dics_tab)
        self.yahoo_dics_tab_vert_layout.setObjectName("yahoo_dics_tab_vert_layout")


        # this is the horizontal layout that holds the two japanese dictionaries
        self.yahoo_jap_dic_horiz_layout = QtGui.QHBoxLayout()
        self.yahoo_jap_dic_horiz_layout.setObjectName("yahoo_jap_dic_horiz_layout")

        self.daijisenverticallayout, self.daijisenlabel, self.daijisenresultwordlabel, \
                self.daijisendefwebview = self.createlist("daijisenverticallayout",
                        "daijisenhorizontallayout", "daijisenresultwordlabel",
                        "daijisenlabel", "daijisentextedit", u'大辞泉')
        self.yahoo_jap_dic_horiz_layout.addLayout(self.daijisenverticallayout)
        self.daijirinverticallayout, self.daijirinlabel, self.daijirinresultwordlabel, \
                self.daijirindefwebview = self.createlist("daijirinverticallayout",
                        "daijirinhorizontallayout", "daijirinresultwordlabel",
                        "daijirinlabel", "daijirintextedit", u'大辞林')
        self.yahoo_jap_dic_horiz_layout.addLayout(self.daijirinverticallayout)
        self.yahoo_dics_tab_vert_layout.addLayout(self.yahoo_jap_dic_horiz_layout, 2)

        # this is the horizontal layout that holds the two english dictionaries
        self.yahoo_eng_dic_horiz_layout = QtGui.QHBoxLayout()
        self.yahoo_eng_dic_horiz_layout.setObjectName("yahoo_eng_dic_horiz_layout")

        self.newcenturyvertlayout, self.newcenturylabel, self.newcenturyresultwordlabel, \
                self.newcenturydefwebview = self.createlist("newcenturyvertlayout",
                        "newcenturyhorizontallayout", "newcenturyresultwordlabel",
                        "newcenturylabel", "newcenturytextedit", "New Century")
        self.yahoo_eng_dic_horiz_layout.addLayout(self.newcenturyvertlayout)
        self.progressvertlayout, self.progresslabel, self.progressresultwordlabel, \
                self.progressdefwebview = self.createlist("progressvertlayout",
                        "progresshorizontallayout", "progressresultwordlabel",
                        "progresslabel", "progresstextedit", "Progressive")
        self.yahoo_eng_dic_horiz_layout.addLayout(self.progressvertlayout)
        self.yahoo_dics_tab_vert_layout.addLayout(self.yahoo_eng_dic_horiz_layout, 3)

    def create_epwing_tab(self, epwing_dics_tab):
        # main vertical layout for tab two
        self.epwing_dics_tab_vert_layout = QtGui.QVBoxLayout(epwing_dics_tab)
        self.epwing_dics_tab_vert_layout.setObjectName("vertlayout")

        # this is the horizontal layout that holds the upper two dictionaries
        self.epwing_upper_dic_horiz_layout = QtGui.QHBoxLayout()
        self.epwing_upper_dic_horiz_layout.setObjectName("epwing_upper_dic_horiz_layout")

        self.kenkyuuverticallayout, self.kenkyuulabel, self.kenkyuuresultwordlabel, \
                self.kenkyuudefwebview = self.createlist("kenkyuuverticallayout",
                        "kenkyuuhorizontallayout", "kenkyuuresultwordlabel",
                        "kenkyuulabel", "kenkyuutextedit", u'研究者')
        self.epwing_upper_dic_horiz_layout.addLayout(self.kenkyuuverticallayout)
        #self.daijirinverticallayout, self.daijirinlabel, self.daijirinresultwordlabel, \
        #        self.daijirindefwebview = self.createlist("daijirinverticallayout",
        #                "daijirinhorizontallayout", "daijirinresultwordlabel",
        #                "daijirinlabel", "daijirintextedit", u'大辞林')
        #self.epwing_upper_dic_horiz_layout.addLayout(self.daijirinverticallayout)
        self.epwing_dics_tab_vert_layout.addLayout(self.epwing_upper_dic_horiz_layout, 2)

        return

        # this is the horizontal layout that holds the lower two dictionaries
        self.epwing_lower_dic_horiz_layout = QtGui.QHBoxLayout()
        self.epwing_lower_dic_horiz_layout.setObjectName("epwing_lower_dic_horiz_layout")

        self.newcenturyvertlayout, self.newcenturylabel, self.newcenturyresultwordlabel, \
                self.newcenturydefwebview = self.createlist("newcenturyvertlayout",
                        "newcenturyhorizontallayout", "newcenturyresultwordlabel",
                        "newcenturylabel", "newcenturytextedit", "New Century")
        self.epwing_lower_dic_horiz_layout.addLayout(self.newcenturyvertlayout)
        self.progressvertlayout, self.progresslabel, self.progressresultwordlabel, \
                self.progressdefwebview = self.createlist("progressvertlayout",
                        "progresshorizontallayout", "progressresultwordlabel",
                        "progresslabel", "progresstextedit", "Progressive")
        self.epwing_lower_dic_horiz_layout.addLayout(self.progressvertlayout)
        self.epwing_dics_tab_vert_layout.addLayout(self.epwing_lower_dic_horiz_layout, 3)

    def setupUi(self, mainwindowselector):
        self.mainwindowselector = mainwindowselector
        mainwindowselector.setObjectName("mainwindowselector")
        mainwindowselector.resize(900, 650)
        #mainwindowselector.setAcceptDrops(False)
        #icon = QtGui.QIcon()
        #pixmap = QtGui.QPixmap("../img/logo32x32.png")
        #icon.addPixmap(pixmap, QtGui.QIcon.Normal, QtGui.QIcon.Off)
        #mainwindowselector.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(mainwindowselector)
        self.centralwidget.setObjectName("centralwidget")

        # main vertical layout that holds the tabwidget
        self.mainverticallayout = QtGui.QVBoxLayout(self.centralwidget)
        self.mainverticallayout.setObjectName("mainverticallayout")

        # tab widget
        self.tabwidget = QtGui.QTabWidget(self.centralwidget)
        self.tabwidget.setTabShape(QtGui.QTabWidget.Rounded)
        self.tabwidget.setObjectName("tabwidget")
        self.mainverticallayout.addWidget(self.tabwidget)

        # yahoo tab
        self.yahoo_dics_tab = QtGui.QWidget()
        self.yahoo_dics_tab.setObjectName("yahoo_dics_tab")
        self.tabwidget.addTab(self.yahoo_dics_tab, u"Yahoo Dics")
        self.create_yahoo_tab(self.yahoo_dics_tab)

        # epwing tab
        self.epwing_dics_tab = QtGui.QWidget()
        self.epwing_dics_tab.setObjectName("epwing_dics_tab")
        self.tabwidget.addTab(self.epwing_dics_tab, u"Epwing Dics")
        self.create_epwing_tab(self.epwing_dics_tab)

        # create the accent box at the bottom of the screen
        self.create_accent_box(self.mainverticallayout)

        # status bar
        self.statusbar = QtGui.QStatusBar(mainwindowselector)
        self.statusbar.setObjectName("statusbar")
        mainwindowselector.setStatusBar(self.statusbar)

        # menubar
        self.menuBar = QtGui.QMenuBar(mainwindowselector)
        self.menuBar.setObjectName("menuBar")
        self.menuFile = QtGui.QMenu(self.menuBar)
        self.menuFile.setObjectName("menuFile")
        self.menuFile.setTitle("File")
        mainwindowselector.setMenuBar(self.menuBar)

        self.actionExit = QtGui.QAction(mainwindowselector)
        self.actionExit.setEnabled(True)
        self.actionExit.setObjectName("actionExit")
        self.actionExit.setText("Exit")
        self.menuFile.addAction(self.actionExit)
        self.menuBar.addAction(self.menuFile.menuAction())

        # four additional tabs for debugging pages
        self.daijisentab, self.daijisentabvertlayout, self.daijisenwebview = \
                self.create_debug_tab("daijisentab", "daijisentabvertlayout", "daijisenwebview")
        self.tabwidget.addTab(self.daijisentab, u'大辞泉')

        self.daijirintab, self.daijirintabvertlayout, self.daijirinwebview = \
                self.create_debug_tab("daijirintab", "daijirintabvertlayout", "daijirinwebview")
        self.tabwidget.addTab(self.daijirintab, u'大辞林')

        self.newcentytab, self.newcentytabvertlayout, self.newcentywebview = \
                self.create_debug_tab("newcentytab", "newcentytabvertlayout", "newcentywebview")
        self.tabwidget.addTab(self.newcentytab, "New Century")

        self.progresstab, self.progresstabvertlayout, self.progresswebview = \
                self.create_debug_tab("progresstab", "progresstabvertlayout", "progresswebview")
        self.tabwidget.addTab(self.progresstab, "Progressive")

        self.kenkyuutab, self.kenkyuutabvertlayout, self.kenkyuuwebview = \
                self.create_debug_tab("kenkyuutab", "kenkyuutabvertlayout", "kenkyuuwebview")
        self.tabwidget.addTab(self.kenkyuutab, u"研究者")


        mainwindowselector.setCentralWidget(self.centralwidget)
        mainwindowselector.setWindowTitle("JDicScrape")

        def go_to_tab(t):
            import sys
            return lambda: self.tabwidget.setCurrentIndex(t)

        for t in range(self.tabwidget.count()):
            action = QtGui.QAction(QtGui.QIcon(), "Go to tab %d" % (t+1), mainwindowselector)
            action.setShortcut("Alt+%d" % (t+1))
            #action.triggered.connect(lambda: self.tabwidget.setCurrentIndex(t))
            action.triggered.connect(go_to_tab(t))
            mainwindowselector.addAction(action)

        # okay button (new style signals)
        self.buttonBox.accepted.connect(mainwindowselector.okay)
        # cancel button (old style signals)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"),
                mainwindowselector.exit)

        # reset form
        self.buttonBox.button(QtGui.QDialogButtonBox.Reset).clicked.connect(
                mainwindowselector.reset)

        # close window from menubar
        self.actionExit.triggered.connect(mainwindowselector.exit)

        QtCore.QMetaObject.connectSlotsByName(mainwindowselector)
