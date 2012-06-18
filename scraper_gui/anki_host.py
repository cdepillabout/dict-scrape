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


def addFact(fields, tags=unicode()):
    fact = createFact(fields, tags)
    if not fact:
        return None

    action = lang._('Add')

    deck = deck()
    deck.setUndoStart(action)
    deck.addFact(fact, False)
    deck.setUndoEnd(action)
    deck.rebuildCounts()

    ankiqt.mw.updateTitleBar()
    ankiqt.mw.statusView.redraw()

    return fact.id

def canAddFact(fields):
    return bool(createFact(fields))

def createFact(fields, tags=unicode()):
    deck = deck()
    fact = deck.newFact()
    fact.tags = cleanupTags(tags)

    try:
        for field in fact.fields:
            field.value = fields.get(field.getName()) or unicode()
            if not fact.fieldValid(field) or not fact.fieldUnique(field, deck.s):
                return None
    except KeyError:
        return None

    return fact

def browseFact(factId):
    browser = ankiqt.ui.dialogs.get('CardList', window())
    browser.dialog.filterEdit.setText('fid:' + str(factId))
    browser.updateSearch()
    browser.onFact()

def cleanupTags(tags):
    return re.sub('[;,]', unicode(), tags).strip()

def fields():
    return [
        (field.name, field.required, field.unique) for field in model().fieldModels
    ]

def deck():
    return window().deck

def model():
    return deck().currentModel

def window():
    return ankiqt.mw

def toolsMenu():
    return window().mainWin.menuTools

def toolBar():
    return window().mainWin.toolBar

def addHook(name, callback):
    hooks.addHook(name, callback)

def removeHook(name, callback):
    hooks.removeHook(name, callback)
