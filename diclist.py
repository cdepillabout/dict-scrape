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

class DefListDelegate(QStyledItemDelegate):

    def __init__(self, parent=None):
        super(DefListDelegate, self).__init__(parent)

    """
    def sizeHint(self, option, index):
        textedit = index.data()
        print(textedit.toString())
        if isinstance(textedit, QTextEdit):
            if option.state & QStyle.State_Selected:
                painter.fillRect(option.rect, option.palette.highlight())
            return rating.sizeHint()
        return super(DefListDelegate, self).sizeHint(option, index)
    """

    def paint(self, painter, option, index):
        print(index.data(Qt.UserRole).toPyObject())
        textedit = index.data(Qt.UserRole).toPyObject()
        print(dir(textedit))
        if isinstance(textedit, QLabel):
            if option.state & QStyle.State_Selected:
                painter.fillRect(option.rect, option.palette.highlight())

            textedit.paint(painter, option.rect, option.palette)
        else:
            super(DefListDelegate, self).paint(painter, option, index)



