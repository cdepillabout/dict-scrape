#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Copyright (c) 2008 Qtrac Ltd. All rights reserved.
# This program or module is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 2 of the License, or
# version 3 of the License, or (at your option) any later version. It is
# provided for educational purposes and is distributed in the hope that
# it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See
# the GNU General Public License for more details.

from PyQt4.QtCore import (QAbstractListModel, QDataStream, QFile,
        QIODevice, QModelIndex, QRegExp, QSize, QString, QVariant, Qt,
        SIGNAL, QRectF)
from PyQt4.QtGui import (QApplication, QColor, QComboBox, QLineEdit,
        QSpinBox, QStyle, QStyledItemDelegate, QTextDocument, QTextEdit,
        QTextOption, QLabel)



class DefListModel(QAbstractListModel):

    def __init__(self):
        super(DefListModel, self).__init__()
        self.defs = []

    def data(self, index, role=Qt.DisplayRole):
        if (not index.isValid() or not (0 <= index.row() < len(self.defs))):
            return QVariant()

        df = self.defs[index.row()]

        if role == Qt.DisplayRole:
            return QVariant(QString(df.definition))
        elif role == Qt.TextAlignmentRole:
            return QVariant(int(Qt.AlignLeft|Qt.AlignVCenter))
        elif role == Qt.TextColorRole:
            return QVariant(QColor(Qt.darkBlue))
        elif role == Qt.BackgroundColorRole:
            return QVariant(QColor(250, 230, 250))
        else:
            print("Called DefListModel.data() for undefined role: %s" % role)

        return QVariant()

    def rowCount(self, index=QModelIndex()):
        return len(self.defs)

    def loaddefs(self, defs):
        self.defs = defs

class DefListDelegate(QStyledItemDelegate):

    def __init__(self, parent=None):
        super(DefListDelegate, self).__init__(parent)

    def createNumberedDefinition(self, index, text):
        first = u'➀'
        ordinal = ord(first)

        print("TEXT!!! %d %d %s" % (index.row(), ord(first), text))
        text = u'%s %s' % (unichr(ordinal + index.row()), text)
        return text


    def paint(self, painter, option, index):
        text = index.model().data(index).toString()
        text = self.createNumberedDefinition(index, text)
        palette = QApplication.palette()
        textoption = QTextOption()
        textoption.setWrapMode(QTextOption.WrapAnywhere)
        document = QTextDocument()
        document.setDefaultTextOption(textoption)
        document.setDefaultFont(option.font)
        # change this in order to change how something is displayed
        # when selected
        if option.state & QStyle.State_Selected:
            document.setHtml(QString("<font color=%1>%2</font>")
                    .arg(palette.highlightedText().color().name())
                    .arg(text))
        else:
            #document = QLabel(text)
            document.setHtml(text)
        color = (palette.highlight().color()
                    if option.state & QStyle.State_Selected
                    else QColor(index.model().data(index,
                                Qt.BackgroundColorRole)))
        painter.save()
        painter.fillRect(option.rect, color)
        painter.translate(option.rect.x(), option.rect.y())
        document.drawContents(painter)
        painter.restore()

    def sizeHint(self, option, index):
        fm = option.fontMetrics
        text = index.model().data(index).toString()
        text = self.createNumberedDefinition(index, text)
        document = QTextDocument()
        textoption = QTextOption()
        textoption.setWrapMode(QTextOption.WrapAnywhere)
        document.setDefaultTextOption(textoption)
        document.setDefaultFont(option.font)
        document.setHtml(text)
        return QSize(document.idealWidth() + 5, fm.height() + 10)
        #return QStyledItemDelegate.sizeHint(self, option, index)

    """
    def sizeHint(self, option, index):
        model = index.model()
        record = model.data(index)
        doc = QTextDocument(self)
        doc.setHtml(record.toString())
        doc.setTextWidth(option.rect.width())
        return QSize(doc.idealWidth(), doc.size().height())
    """



