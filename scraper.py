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
from PyQt4 import QtGui

from scraper_gui.selector import MainWindowSelector


class DictScraper(object):
    def __init__(self):
        pass

class DictScraperStandalone(DictScraper):
    def __init__(self, word_kanji, word_kana):
        super(DictScraperStandalone, self).__init__()
        self.application = QtGui.QApplication(sys.argv)
        self.window = MainWindowSelector(None, word_kanji, word_kana)
        self.window.show()
        self.application.exec_()

class DictScraperPlugin(DictScraper):
    def __init__(self):
        super(DictScraperPlugin, self).__init__()

        """
        self.toolIconVisible = False
        self.window = None
        self.anki = anki_host.Anki()
        self.parent = self.anki.window()
        self.separator = QtGui.QAction(self.parent)
        self.separator.setSeparator(True)
        self.action = QtGui.QAction(QtGui.QIcon(buildResPath('img/logo32x32.png')), '&Yomichan...', self.parent)
        self.action.setIconVisibleInMenu(True)
        self.action.triggered.connect(self.onShowRequest)

        self.anki.addHook('loadDeck', self.onDeckLoad)
        self.anki.addHook('deckClosed', self.onDeckClose)
        """


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("ERROR! Need 2 args")
        sys.exit(1)
    instance = DictScraperStandalone(sys.argv[1].decode("utf8"), sys.argv[2].decode("utf8"))
else:
    from scraper_gui import anki_host
    instance = DictScraperPlugin()
