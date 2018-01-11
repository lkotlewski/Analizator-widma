# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'classif_base.ui'
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

class Ui_ClassifBase(object):
    def setupUi(self, ClassifBase):
        ClassifBase.setObjectName(_fromUtf8("ClassifBase"))
        ClassifBase.resize(861, 636)
        self.title_label = QtGui.QLabel(ClassifBase)
        self.title_label.setGeometry(QtCore.QRect(320, 40, 271, 20))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.title_label.setFont(font)
        self.title_label.setObjectName(_fromUtf8("title_label"))
        self.verticalLayoutWidget = QtGui.QWidget(ClassifBase)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(30, 140, 801, 421))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.bar_charts_layout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.bar_charts_layout.setObjectName(_fromUtf8("bar_charts_layout"))
        self.subtitle_label = QtGui.QLabel(ClassifBase)
        self.subtitle_label.setGeometry(QtCore.QRect(280, 80, 341, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.subtitle_label.setFont(font)
        self.subtitle_label.setAlignment(QtCore.Qt.AlignCenter)
        self.subtitle_label.setWordWrap(True)
        self.subtitle_label.setObjectName(_fromUtf8("subtitle_label"))
        self.recognized_mod_label = QtGui.QLabel(ClassifBase)
        self.recognized_mod_label.setGeometry(QtCore.QRect(30, 590, 501, 20))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 170, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 170, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(159, 158, 158))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.recognized_mod_label.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.recognized_mod_label.setFont(font)
        self.recognized_mod_label.setText(_fromUtf8(""))
        self.recognized_mod_label.setObjectName(_fromUtf8("recognized_mod_label"))

        self.retranslateUi(ClassifBase)
        QtCore.QMetaObject.connectSlotsByName(ClassifBase)

    def retranslateUi(self, ClassifBase):
        ClassifBase.setWindowTitle(_translate("ClassifBase", "Form", None))
        self.title_label.setText(_translate("ClassifBase", "Ekstrakcja cech i klasyfikacja", None))
        self.subtitle_label.setText(_translate("ClassifBase", "Porównanie wartości cech sygnału ze średnimi wartościami cech dla rozpoznanej modulacji", None))

