import sys
import numpy as np
from PyQt4 import QtGui, QtCore

from main_window_base import Ui_MainWindowBase
from mode_choice_form import ModeChoiceForm
from scan_spectral_analysis_form import ScanSpectralAnalysisForm
from file_spectral_analysis_form import FileSpectralAnalysisForm
from classif_form import ClassifForm


class MainWindow(QtGui.QMainWindow):
    MEASUREMENTS_DIRECTORY_REL_PATH = "scanning/measurements"

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindowBase()
        self.ui.setupUi(self)
        self.ui.menubar.setNativeMenuBar(False)
        self.ui.back_to_analyse_action.setDisabled(True)
        palette = self.palette()
        palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor('red'))
        #self.setStyleSheet("background-image: url(start_background.jpg)")
        #self.setStyleSheet("background-color: '#60ea7d'")
        self.scan_spectral_analysis_form = ScanSpectralAnalysisForm(main_window=self)
        self.file_spectral_analysis_form = FileSpectralAnalysisForm(main_window=self)
        self.classif_form = ClassifForm()
        self.mode_choice_form = ModeChoiceForm(main_window=self)
        self.stacked_layout = QtGui.QStackedLayout(self.ui.centralwidget)
        self.stacked_layout.addWidget(self.scan_spectral_analysis_form)
        self.stacked_layout.addWidget(self.file_spectral_analysis_form)
        self.stacked_layout.addWidget(self.classif_form)
        self.stacked_layout.addWidget(self.mode_choice_form)
        self.stacked_layout.setCurrentWidget(self.mode_choice_form)
        self.current_analyse_widget = None

        QtCore.QObject.connect(self.ui.mode_choice_action, QtCore.SIGNAL("triggered()"),
                               self.return_to_mode_choice_layout)
        QtCore.QObject.connect(self.ui.back_to_analyse_action, QtCore.SIGNAL("triggered()"), self.return_to_analyse)

    def show_spectrum_layout(self):
        self.ui.back_to_analyse_action.setDisabled(True)
        self.stacked_layout.setCurrentWidget(self.scan_spectral_analysis_form)
        self.current_analyse_widget = self.scan_spectral_analysis_form

    def show_file_spectrum_layout(self):
        self.ui.back_to_analyse_action.setDisabled(True)
        self.stacked_layout.setCurrentWidget(self.file_spectral_analysis_form)
        self.current_analyse_widget = self.file_spectral_analysis_form

    def show_classif_layout(self, signal, do_plots):
        self.ui.back_to_analyse_action.setEnabled(True)
        self.classif_form.generate_layout(signal, do_plots=do_plots)
        self.stacked_layout.setCurrentWidget(self.classif_form)

    def return_to_mode_choice_layout(self):
        self.clear_layouts()
        self.stacked_layout.setCurrentWidget(self.mode_choice_form)

    def return_to_analyse(self):
        self.stacked_layout.setCurrentWidget(self.current_analyse_widget)
        self.stacked_layout.removeWidget(self.classif_form)
        self.classif_form = ClassifForm()
        self.stacked_layout.addWidget(self.classif_form)

    def clear_layouts(self):
        self.ui.back_to_analyse_action.setDisabled(True)
        self.stacked_layout.removeWidget(self.file_spectral_analysis_form)
        self.stacked_layout.removeWidget(self.scan_spectral_analysis_form)
        self.stacked_layout.removeWidget(self.classif_form)
        self.scan_spectral_analysis_form = ScanSpectralAnalysisForm(main_window=self)
        self.file_spectral_analysis_form = FileSpectralAnalysisForm(main_window=self)
        self.classif_form = ClassifForm()
        self.stacked_layout.addWidget(self.scan_spectral_analysis_form)
        self.stacked_layout.addWidget(self.file_spectral_analysis_form)
        self.stacked_layout.addWidget(self.classif_form)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = MainWindow()
    myapp.show()
    sys.exit(app.exec_())

