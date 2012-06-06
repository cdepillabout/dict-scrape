#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

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

import os
import sys
from PyQt4 import QtGui, QtCore, uic
from ui.defscreenui import Ui_MainWindowReader
from jdicscrape import DaijirinDictionary, DaijisenDictionary, \
        ProgressiveDictionary, NewCenturyDictionary


def buildResPath(relative):
    directory = os.path.split(__file__)[0]
    return os.path.join(directory, relative)

class JDicScrapeStandalone(object):
    def __init__(self, word_kanji, word_kana):
        self.application = QtGui.QApplication(sys.argv)
        self.window = MainWindowReader(None, word_kanji, word_kana)
        self.window.show()
        self.application.exec_()

class MainWindowReader(QtGui.QMainWindow):

    def fillin(self, word_kanji, word_kana):
        daijirin = DaijirinDictionary()
        daijisen = DaijisenDictionary()
        progressive = ProgressiveDictionary()
        newcentury = NewCenturyDictionary()
        dicts = [
                (daijirin, self.ui.daijirinlist, self.ui.daijirinlistmodel, self.ui.daijirinwebview, self.ui.daijirinresultwordlabel),
                (daijisen, self.ui.daijisenlist, self.ui.daijisenlistmodel, self.ui.daijisenwebview, self.ui.daijisenresultwordlabel),
                (progressive, self.ui.progresslist, self.ui.progresslistmodel, self.ui.progresswebview, self.ui.progressresultwordlabel),
                (newcentury, self.ui.newcenturylist, self.ui.newcenturylistmodel, self.ui.newcentywebview, self.ui.newcenturyresultwordlabel),
                ]

        #self.ui.statusbar.showMessage('Adding defs for %s (%s)...' % (word_kanji, word_kana))

        for d, listwidget, model, webviewwidget, resultwordlabel in dicts:
            result = d.lookup(word_kanji, word_kana)
            if d == daijirin:
                if result.accent:
                    self.ui.accentlineedit.setText(result.accent)
                    self.ui.accentlineedit.setEnabled(True)
                    self.ui.useaccentcheckbox.setEnabled(True)
                else:
                    self.ui.accentlineedit.setText("NO ACCENT")
                    self.ui.accentlineedit.setEnabled(False)
                    self.ui.useaccentcheckbox.setEnabled(False)

            # add webview
            webviewwidget.setUrl(QtCore.QUrl.fromEncoded(result.url))

            # add the resulting word
            resultwordlabeltext = ""
            if result.definition_found():
                if result.kanji == result.kana:
                    resultwordlabeltext = "%s" % result.kanji
                else:
                    resultwordlabeltext = "%s (%s)" % (result.kanji, result.kana)
            else:
                resultwordlabeltext = "NO DEFINITION FOUND"
            resultwordlabel.setText(u'<font color="#555555">%s</font>' % resultwordlabeltext)

            self.addDefinition(listwidget, model, result)



    def __init__(self, parent, word_kanji, word_kana):
        QtGui.QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindowReader()
        self.ui.setupUi(self)
        self.fillin(word_kanji, word_kana)

    # pop up a dialog box asking if we are sure we want to quit
    def closeEvent(self, event):
        """
        reply = QtGui.QMessageBox.question(self, 'Message',
                "Are you sure you want to quit?", QtGui.QMessageBox.Yes |
                QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
        """
        pass

    def addDefinition(self, listwidget, model, result):
        # add result definitions
        for d in result.defs:
            model.addData(d.definition)
            """
            textedit = QtGui.QLabel(d.definition)
            item = QtGui.QListWidgetItem()
            #item.setSizeHint(QtCore.QSize(200,200))
            listwidget.addItem(item)
            listwidget.setItemWidget(item, textedit)
            """


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("ERROR! Need 2 args")
        sys.exit(1)
    instance = JDicScrapeStandalone(sys.argv[1].decode("utf8"), sys.argv[2].decode("utf8"))
#else:
#    from yomi_base import anki_host
#    instance = YomichanPlugin()
