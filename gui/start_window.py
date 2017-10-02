import sys
from bandwithscanner import BandwithScanner
from PyQt4 import QtGui, QtCore

from start_window_base import Ui_StartWindowBase


class StartWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_StartWindowBase()
        self.ui.setupUi(self)

        QtCore.QObject.connect(self.ui.fast_analize_action, QtCore.SIGNAL("triggered()"), self.fast_analize)

    def fast_analize(self):
        tb = BandwithScanner()
        tb.fast_analize()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = StartWindow()
    myapp.show()
    sys.exit(app.exec_())

