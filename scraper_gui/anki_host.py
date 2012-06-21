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


import ankiqt
from anki import hooks, lang
import re

def fieldtoanki(string):
    string = unicode.replace(string, u'\n', u'<br>')
    return string

def browseFact(factId):
    browser = ankiqt.ui.dialogs.get('CardList', ankiqt.mw)
    browser.dialog.filterEdit.setText('fid:' + str(factId))
    browser.updateSearch()
    browser.onFact()

def cleanupTags(tags):
    return re.sub('[;,]', unicode(), tags).strip()

def addHook(name, callback):
    hooks.addHook(name, callback)

def removeHook(name, callback):
    hooks.removeHook(name, callback)
