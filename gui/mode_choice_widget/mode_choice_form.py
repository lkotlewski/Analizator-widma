from PyQt4 import QtGui, QtCore
from mode_choice_base import Ui_ModeChoiceFormBase


class ModeChoiceForm(QtGui.QWidget):
    def __init__(self, main_window, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_ModeChoiceFormBase()
        self.ui.setupUi(self)
        self.main_window = main_window

        QtCore.QObject.connect(self.ui.scan_bandwidth_button, QtCore.SIGNAL("clicked()"),
                               self.main_window.show_spectrum_layout)
        QtCore.QObject.connect(self.ui.choose_file_button, QtCore.SIGNAL("clicked()"),
                               self.main_window.show_file_spectrum_layout)


