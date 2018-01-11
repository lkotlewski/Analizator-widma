# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'file_specific_base.ui'
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

class Ui_FileSpecificBase(object):
    def setupUi(self, FileSpecificBase):
        FileSpecificBase.setObjectName(_fromUtf8("FileSpecificBase"))
        FileSpecificBase.resize(289, 151)
        self.label_6 = QtGui.QLabel(FileSpecificBase)
        self.label_6.setGeometry(QtCore.QRect(0, 0, 111, 21))
        self.label_6.setWordWrap(True)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.loaded_file_text_edit = QtGui.QTextEdit(FileSpecificBase)
        self.loaded_file_text_edit.setEnabled(False)
        self.loaded_file_text_edit.setGeometry(QtCore.QRect(0, 30, 281, 71))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.loaded_file_text_edit.setFont(font)
        self.loaded_file_text_edit.setObjectName(_fromUtf8("loaded_file_text_edit"))
        self.load_file_button = QtGui.QPushButton(FileSpecificBase)
        self.load_file_button.setGeometry(QtCore.QRect(130, 110, 131, 27))
        self.load_file_button.setObjectName(_fromUtf8("load_file_button"))

        self.retranslateUi(FileSpecificBase)
        QtCore.QMetaObject.connectSlotsByName(FileSpecificBase)

    def retranslateUi(self, FileSpecificBase):
        FileSpecificBase.setWindowTitle(_translate("FileSpecificBase", "Form", None))
        self.label_6.setText(_translate("FileSpecificBase", "Wczytany plik:", None))
        self.load_file_button.setText(_translate("FileSpecificBase", "Wczytaj plik", None))

