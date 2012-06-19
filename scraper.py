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

import sys
from PyQt4 import QtCore, QtGui

from scraper_gui.selector import MainWindowSelector

from ankiqt.ui import facteditor
import ankiqt
import anki.hooks

class DictScraper(object):
    def __init__(self):
        pass

class DictScraperStandalone(DictScraper):
    def __init__(self, word_kanji, word_kana):
        super(DictScraperStandalone, self).__init__()
        self.application = QtGui.QApplication(sys.argv)
        self.window = MainWindowSelector(word_kanji, word_kana)
        self.window.show()
        self.application.exec_()

class DictScraperPlugin(DictScraper):
    def __init__(self):
        super(DictScraperPlugin, self).__init__()
        self.window = None

        facteditor.FactEditor.setupFields = anki.hooks.wrap(facteditor.FactEditor.setupFields,
                self.newsetupfields, "after")

    def launchGUI(self, factedit):
        print("from launchGUI: factedit = %s (%s)" % (factedit, type(factedit)))
        factedit.saveFieldsNow()
        kanji = factedit.fact["Vocab"]
        kana = factedit.fact["VocabKana"]

        self.window = MainWindowSelector(kanji, kana, factedit.widget, factedit, fact)
        self.window.show()
        print("HELLO")
        """
        if self.window:
            self.window.setVisible(True)
            self.window.activateWindow()
        else:
            self.window = MainWindowReader(self.parent, kanji, kana)
            self.window.show()
            """

    def newsetupfields(self, factedit):
        s = QtGui.QShortcut(QtGui.QKeySequence(_("Ctrl+j")), factedit.parent)
        s.connect(s, QtCore.SIGNAL("activated()"),
                lambda factedit=factedit: self.launchGUI(factedit))

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("ERROR! Need 2 args")
        sys.exit(1)
    instance = DictScraperStandalone(sys.argv[1].decode("utf8"), sys.argv[2].decode("utf8"))
else:
    from scraper_gui import anki_host
    instance = DictScraperPlugin()
