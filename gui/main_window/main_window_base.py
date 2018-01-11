# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window_base.ui'
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

class Ui_MainWindowBase(object):
    def setupUi(self, MainWindowBase):
        MainWindowBase.setObjectName(_fromUtf8("MainWindowBase"))
        MainWindowBase.resize(859, 676)
        self.centralwidget = QtGui.QWidget(MainWindowBase)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        MainWindowBase.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindowBase)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 859, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menu = QtGui.QMenu(self.menubar)
        self.menu.setObjectName(_fromUtf8("menu"))
        MainWindowBase.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindowBase)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindowBase.setStatusBar(self.statusbar)
        self.mode_choice_action = QtGui.QAction(MainWindowBase)
        self.mode_choice_action.setObjectName(_fromUtf8("mode_choice_action"))
        self.complex_analize_action = QtGui.QAction(MainWindowBase)
        self.complex_analize_action.setObjectName(_fromUtf8("complex_analize_action"))
        self.back_to_analyse_action = QtGui.QAction(MainWindowBase)
        self.back_to_analyse_action.setObjectName(_fromUtf8("back_to_analyse_action"))
        self.menu.addAction(self.mode_choice_action)
        self.menu.addAction(self.back_to_analyse_action)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindowBase)
        QtCore.QMetaObject.connectSlotsByName(MainWindowBase)

    def retranslateUi(self, MainWindowBase):
        MainWindowBase.setWindowTitle(_translate("MainWindowBase", "Analizator widma", None))
        self.menu.setTitle(_translate("MainWindowBase", "Nawigacja", None))
        self.mode_choice_action.setText(_translate("MainWindowBase", "Powrót do wyboru trybu", None))
        self.complex_analize_action.setText(_translate("MainWindowBase", "Dokładna analiza", None))
        self.back_to_analyse_action.setText(_translate("MainWindowBase", "Powrót do analizy", None))

