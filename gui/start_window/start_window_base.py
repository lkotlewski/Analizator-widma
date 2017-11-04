# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'start_window_base.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_StartWindowBase(object):
    def setupUi(self, StartWindowBase):
        StartWindowBase.setObjectName(_fromUtf8("StartWindowBase"))
        StartWindowBase.resize(800, 600)
        self.centralwidget = QtGui.QWidget(StartWindowBase)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        StartWindowBase.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(StartWindowBase)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menu_analize = QtGui.QMenu(self.menubar)
        self.menu_analize.setObjectName(_fromUtf8("menu_analize"))
        StartWindowBase.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(StartWindowBase)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        StartWindowBase.setStatusBar(self.statusbar)
        self.fast_analize_action = QtGui.QAction(StartWindowBase)
        self.fast_analize_action.setObjectName(_fromUtf8("fast_analize_action"))
        self.complex_analize_action = QtGui.QAction(StartWindowBase)
        self.complex_analize_action.setObjectName(_fromUtf8("complex_analize_action"))
        self.menu_analize.addAction(self.fast_analize_action)
        self.menu_analize.addAction(self.complex_analize_action)
        self.menubar.addAction(self.menu_analize.menuAction())

        self.retranslateUi(StartWindowBase)
        QtCore.QMetaObject.connectSlotsByName(StartWindowBase)

    def retranslateUi(self, StartWindowBase):
        StartWindowBase.setWindowTitle(_translate("StartWindowBase", "Analizator widma", None))
        self.menu_analize.setTitle(_translate("StartWindowBase", "Analiza widmowa", None))
        self.fast_analize_action.setText(_translate("StartWindowBase", "Szybka analiza", None))
        self.complex_analize_action.setText(_translate("StartWindowBase", "Dokładna analiza", None))

