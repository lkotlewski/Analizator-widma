import sys
import os
from analyser import Analyser
from PyQt4 import QtGui, QtCore

from start_window_base import Ui_StartWindowBase

from bandwidthscanner import BandwidthScanner


class StartWindow(QtGui.QMainWindow):
    MEASUREMENTS_DIRECTORY_REL_PATH = "scanning/measurements"

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_StartWindowBase()
        self.ui.setupUi(self)
        self.ui.menubar.setNativeMenuBar(False)
        self.setStyleSheet("background-image: url(start_window/start_background.jpg)")

        QtCore.QObject.connect(self.ui.fast_analize_action, QtCore.SIGNAL("triggered()"), self.fast_analize)

    def fast_analize(self):
        tb = BandwidthScanner()
        tb.fast_analize(start_freq=88e6, finish_freq=89e6, resolution=1e6)
        a = Analyser()
        current_directory = os.getcwd()
        current_parent = os.path.abspath(os.path.join(current_directory, os.pardir))
        a.load_measurements(os.path.join(current_parent, StartWindow.MEASUREMENTS_DIRECTORY_REL_PATH, tb.out_filename))
        a.print_loaded_file_info()
        a.analyse()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = StartWindow()
    myapp.show()
    sys.exit(app.exec_())

