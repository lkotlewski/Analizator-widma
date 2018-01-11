# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'scan_specific_base.ui'
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

class Ui_ScanSpecificBase(object):
    def setupUi(self, ScanSpecificBase):
        ScanSpecificBase.setObjectName(_fromUtf8("ScanSpecificBase"))
        ScanSpecificBase.resize(348, 151)
        self.progress_label = QtGui.QLabel(ScanSpecificBase)
        self.progress_label.setGeometry(QtCore.QRect(0, 0, 201, 17))
        self.progress_label.setObjectName(_fromUtf8("progress_label"))
        self.analysis_progress_bar = QtGui.QProgressBar(ScanSpecificBase)
        self.analysis_progress_bar.setGeometry(QtCore.QRect(0, 30, 151, 25))
        self.analysis_progress_bar.setProperty("value", 0)
        self.analysis_progress_bar.setObjectName(_fromUtf8("analysis_progress_bar"))
        self.info_plain_text_edit = QtGui.QPlainTextEdit(ScanSpecificBase)
        self.info_plain_text_edit.setGeometry(QtCore.QRect(4, 30, 288, 111))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 194, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 194, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(159, 158, 158))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        self.info_plain_text_edit.setPalette(palette)
        self.info_plain_text_edit.setAutoFillBackground(False)
        self.info_plain_text_edit.setReadOnly(True)
        self.info_plain_text_edit.setBackgroundVisible(False)
        self.info_plain_text_edit.setObjectName(_fromUtf8("info_plain_text_edit"))

        self.retranslateUi(ScanSpecificBase)
        QtCore.QMetaObject.connectSlotsByName(ScanSpecificBase)

    def retranslateUi(self, ScanSpecificBase):
        ScanSpecificBase.setWindowTitle(_translate("ScanSpecificBase", "Form", None))
        self.progress_label.setText(_translate("ScanSpecificBase", "Przeskanowana część pasma:", None))

