# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui, QtWebKit

DEF_LIST_HTML_BEGINNING = """
<html>
    <head>
        <style type="text/css">
            body {
                font-family: arial, sans-serif;
                font-size: 120%;
            }
            div.ex_sent_selected, span.defpart_selected {
                background-color: #dddddd;
            }
            div.ex_sent_notselected, span.defpart_notselected {
                background-color: #ffffff;
            }
            span.jap_sentence {
                color: #004400;
                font-weight: bold;
            }
            span.eng_trans {
                font-style: italic;
            }

            div.ex_sent_list {
                padding-left: 10%;
            }
        </style>
        <script language="javascript" type="text/javascript">
            function changeBackgroundColor(objDivID)
            {
                elem = document.getElementById(objDivID);
                attr = elem.getAttribute("class");
                if(attr == "defpart_selected") {
                    elem.setAttribute("class", "defpart_notselected");
                }
                else if (attr == "defpart_notselected") {
                    elem.setAttribute("class", "defpart_selected");
                }
                else if (attr == "ex_sent_selected") {
                    elem.setAttribute("class", "ex_sent_notselected");
                }
                else if (attr == "ex_sent_notselected") {
                    elem.setAttribute("class", "ex_sent_selected");
                }
            }
        </script>
    </head>

    <body onmousedown="return false;">
"""

class DefWebView(QtWebKit.QWebView):
    def __init__(self, parent=None, defs=[]):
        super(DefWebView, self).__init__(parent)
        self.defs = defs

    def setDefs(self, defs):
        first = u'➀'
        ordinal = ord(first)

        html = DEF_LIST_HTML_BEGINNING
        self.defs = defs
        for i, d in enumerate(defs):
            # add definitions
            html += u"\n<div class='definition'>%s " % unichr(ordinal + i)
            for j, p in enumerate(d.parts):
                idattr = u"id='defpart_%s_%s'" % (i, j)
                classattr = u"class='defpart_notselected'"
                onclickattr = u"onclick='changeBackgroundColor(\"defpart_%s_%s\");'" % (i, j)
                html += u'\n<span %s %s %s>%s</span>。' % \
                        (idattr, classattr, onclickattr, p.part)
            html += u"</div>"

            # add example sentences
            html += u"\n<div class='ex_sent_list'>"
            for j, e in enumerate(d.example_sentences):
                idattr = u"id='ex_sent_%s_%s'" % (i, j)
                classattr = u"class='ex_sent_notselected'"
                onclickattr = u"onclick='changeBackgroundColor(\"ex_sent_%s_%s\");'" % (i, j)
                html += u'\n<div %s %s %s><span class="jap_sentence">%s</span>' % \
                        (idattr, classattr, onclickattr, e.jap_sentence)
                if e.eng_trans:
                    html += u'<br/><span class="eng_trans">%s</span>' % e.eng_trans
                html += u'</div>'
            html += u"</div>"

        html += u"\n</body></html>"

        self.setHtml(html)
