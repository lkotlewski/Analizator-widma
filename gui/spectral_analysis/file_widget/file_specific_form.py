from PyQt4 import QtGui

from file_specific_base import Ui_FileSpecificBase


class FileSpecificForm(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_FileSpecificBase()
        self.ui.setupUi(self)
