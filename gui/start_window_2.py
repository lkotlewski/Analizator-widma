import sys
from PyQt4 import QtGui, uic

class StartWindow2(QtGui.QMainWindow):
    def __init__(self):
        super(StartWindow2, self).__init__()
        uic.loadUi('start_window_base.ui', self)
        self.show()

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = StartWindow2()
    sys.exit(app.exec_())
