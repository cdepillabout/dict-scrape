#!/usr/bin/env python2
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

import os
import sys
from PyQt4 import QtGui, QtCore, uic
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

    def addDefinition(self, qtlist, item_text):
        item = QtGui.QListWidgetItem()
        text = "（%s）%s".decode("utf8") % (qtlist.count() + 1, item_text)
        item.setText(text)

        if qtlist.count() % 2 == 1:
            #item.setBackground(QtGui.QColor('#e5e5e5'))
            pass

        qtlist.addItem(item)

    def __init__(self, parent, word_kanji, word_kana):
        QtGui.QMainWindow.__init__(self, parent)
        uic.loadUi(buildResPath('ui/defscreen.ui'), self)

        daijirin = DaijirinDictionary()
        daijisen = DaijisenDictionary()
        progressive = ProgressiveDictionary()
        newcentury = NewCenturyDictionary()
        dicts = [
                (daijirin, self.daijirinlist),
                (daijisen, self.daijisenlist),
                (progressive, self.progressivelist),
                (newcentury, self.newcenturylist),
                ]

        for d, l in dicts:
            result = d.lookup(word_kanji, word_kana)
            #print result

            if not result:
                l.addItem("NO RESULT")
            else:
                for result_def in result.defs:
                    if result_def.definition:
                        item_text = result_def.definition
                    else:
                        item_text = "NO DEFINITION AVAILABLE"

                    self.addDefinition(l, item_text)



if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("ERROR! Need 2 args")
        sys.exit(1)
    instance = JDicScrapeStandalone(sys.argv[1], sys.argv[2])
#else:
#    from yomi_base import anki_host
#    instance = YomichanPlugin()
