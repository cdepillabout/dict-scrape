# -*- coding: UTF-8 -*-

from PyQt4 import QtGui, QtCore
from .ui.selectorui import Ui_MainWindowSelector

from dictscrape import DaijirinDictionary, DaijisenDictionary, \
        ProgressiveDictionary, NewCenturyDictionary

class MainWindowSelector(QtGui.QMainWindow):

    def __init__(self, word_kanji, word_kana, parent=None, factedit=None, fact=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.parent = parent
        self.factedit = factedit
        self.fact = fact
        self.ui = Ui_MainWindowSelector()
        self.ui.setupUi(self)
        self.fillin(word_kanji, word_kana)

    # pop up a dialog box asking if we are sure we want to quit
    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Message',
                "Are you sure you want to quit?", QtGui.QMessageBox.Yes |
                QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def reset(self, button):
        """
        This is the action for the reset button.
        It resets all the selected definition parts and sentences.
        """
        # this shows the sender (but in this case it will only be the reset button)
        #sender = self.mainwindowselector.sender()
        webviews = [self.ui.daijisendefwebview,
                self.ui.daijirindefwebview,
                self.ui.newcenturydefwebview,
                self.ui.progressdefwebview]
        for w in webviews:
            mainframe = w.page().mainFrame()
            mainframe.evaluateJavaScript(u"resetAll()")

    def okay(self):
        jap_webviews = [self.ui.daijisendefwebview, self.ui.daijirindefwebview]
        eng_webviews = [self.ui.newcenturydefwebview, self.ui.progressdefwebview]

        jap_defs = u''
        eng_defs = u''

        example_sentence_jap = u''
        example_sentence_eng = u''

        for w in jap_webviews:
            mainframe = w.page().mainFrame()
            def_parts = mainframe.findAllElements(u'span[class="defpart_selected"]')
            for elem in def_parts:
                jap_defs += u'%s。' % elem.toPlainText()

        for w in eng_webviews:
            mainframe = w.page().mainFrame()
            def_parts = mainframe.findAllElements(u'span[class="defpart_selected"]')
            for i, elem in enumerate(def_parts):
                if i + 1 == len(def_parts):
                    eng_defs += u'%s' % elem.toPlainText()
                else:
                    eng_defs += u'%s, ' % elem.toPlainText()

        print("Definition: %s%s" % (jap_defs, eng_defs))

    def addDefinition(self, defwebviewwidget, result):
        # add result definitions
        defwebviewwidget.setDefs(result.defs)

    def fillin(self, word_kanji, word_kana):
        daijirin = DaijirinDictionary()
        daijisen = DaijisenDictionary()
        progressive = ProgressiveDictionary()
        newcentury = NewCenturyDictionary()
        dicts = [
                (daijirin, self.ui.daijirindefwebview, self.ui.daijirinwebview, self.ui.daijirinresultwordlabel),
                (daijisen, self.ui.daijisendefwebview, self.ui.daijisenwebview, self.ui.daijisenresultwordlabel),
                (progressive, self.ui.progressdefwebview, self.ui.progresswebview, self.ui.progressresultwordlabel),
                (newcentury, self.ui.newcenturydefwebview, self.ui.newcentywebview, self.ui.newcenturyresultwordlabel),
                ]

        #self.ui.statusbar.showMessage('Adding defs for %s (%s)...' % (word_kanji, word_kana))

        for d, defwebviewwidget, webviewwidget, resultwordlabel in dicts:
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

            self.addDefinition(defwebviewwidget, result)
