# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mode_choice_base.ui'
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

class Ui_ModeChoiceFormBase(object):
    def setupUi(self, ModeChoiceFormBase):
        ModeChoiceFormBase.setObjectName(_fromUtf8("ModeChoiceFormBase"))
        ModeChoiceFormBase.resize(850, 425)
        self.label = QtGui.QLabel(ModeChoiceFormBase)
        self.label.setGeometry(QtCore.QRect(260, 140, 371, 59))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(ModeChoiceFormBase)
        self.label_2.setGeometry(QtCore.QRect(260, 230, 364, 31))
        self.label_2.setWordWrap(False)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.choose_file_button = QtGui.QPushButton(ModeChoiceFormBase)
        self.choose_file_button.setGeometry(QtCore.QRect(320, 360, 260, 27))
        self.choose_file_button.setObjectName(_fromUtf8("choose_file_button"))
        self.scan_bandwidth_button = QtGui.QPushButton(ModeChoiceFormBase)
        self.scan_bandwidth_button.setGeometry(QtCore.QRect(320, 300, 260, 27))
        self.scan_bandwidth_button.setAutoFillBackground(False)
        self.scan_bandwidth_button.setObjectName(_fromUtf8("scan_bandwidth_button"))

        self.retranslateUi(ModeChoiceFormBase)
        QtCore.QMetaObject.connectSlotsByName(ModeChoiceFormBase)

    def retranslateUi(self, ModeChoiceFormBase):
        ModeChoiceFormBase.setWindowTitle(_translate("ModeChoiceFormBase", "Form", None))
        self.label.setText(_translate("ModeChoiceFormBase", "Witaj w programie Analizator Widma!", None))
        self.label_2.setText(_translate("ModeChoiceFormBase", "Wybierz tryb:", None))
        self.choose_file_button.setText(_translate("ModeChoiceFormBase", "Analiza pliku z pomiarami", None))
        self.scan_bandwidth_button.setText(_translate("ModeChoiceFormBase", "Skanowanie wybranego pasma", None))

