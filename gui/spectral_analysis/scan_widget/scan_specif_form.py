from PyQt4 import QtGui

from scan_specific_base import Ui_ScanSpecificBase


class ScanSpecificForm(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_ScanSpecificBase()
        self.ui.setupUi(self)
        self.ui.analysis_progress_bar.hide()
        self.ui.progress_label.hide()
