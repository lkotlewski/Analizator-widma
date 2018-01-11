import os
from PyQt4 import QtCore, QtGui
from matplotlib import pyplot as plt

from spectral_analysis_form import SpectralAnalysisForm
from scan_specif_form import ScanSpecificForm
from analyser import Analyser
from bandwidthscanner import BandwidthScanner

WIDGET_STYLE = """
QProgressBar{
    border-radius: 5px;
    text-align: center;
}

QProgressBar::chunk{
    background-color: '#3ce234';
}

FigureCanvas{
    border : 1px solid black;
}


QSlider::add-page:qlineargradient {
background: lightgrey;
border-top-right-radius: 2px;
border-bottom-right-radius: 2px;
border-top-left-radius: 0px;
border-bottom-left-radius: 0px;
}

QSlider::sub-page:qlineargradient {
background: '#a4a6aa';
border-top-right-radius: 0px;
border-bottom-right-radius: 0px;
border-top-left-radius: 2px;
border-bottom-left-radius: 2px;
}

QSlider::handle:horizontal {
width: 15px;
}

QSlider::groove:horizontal {
border: 1px solid #999999;
height: 18px;

border-radius: 9px;
}
"""


class ScanSpectralAnalysisForm(SpectralAnalysisForm):
    def __init__(self, main_window, parent=None):
        SpectralAnalysisForm.__init__(self, main_window, parent)
        self.scan_specific_form = ScanSpecificForm()
        self.ui.type_specif_layout.addWidget(self.scan_specific_form)
        self.setStyleSheet(WIDGET_STYLE)

        QtCore.QObject.connect(self.ui.start_analysis_button, QtCore.SIGNAL("clicked()"), self.spectral_analysis)
        self.ui.gain_slider.valueChanged.connect(self.on_gain_slider_value_changed)

    def spectral_analysis(self):
        self.scan_specific_form.ui.info_plain_text_edit.hide()
        if self.chart_plotted:
            self.reset_figure()
        plt.close(self.figure)
        self.scan_specific_form.ui.analysis_progress_bar.show()
        self.scan_specific_form.ui.progress_label.show()
        tb = BandwidthScanner(window_size=self.ui.probes_number_box.value(), gain=self.ui.gain_slider.value())
        out_filepath = tb.scan_bandwidth(start_freq=self.ui.start_freq_box.value()*1e6,
                                         stop_freq=self.ui.finish_freq_box.value() * 1e6,
                                         measurements_place=str(self.ui.place_text_edit.toPlainText()),
                                         progress_bar=self.scan_specific_form.ui.analysis_progress_bar)
        self.scan_specific_form.ui.info_plain_text_edit.setPlainText(QtCore.QString('Pomiary zapisano w pliku : ')
                                                                     + out_filepath)
        self.scan_specific_form.ui.info_plain_text_edit.show()
        self.analyser = Analyser(os.path.join(out_filepath))
        self.analyser.print_loaded_file_info()
        self.analyser.spectral_analyse2(spectrum_axis=self.axis)
        self.canvas.draw()
        self.chart_plotted = True
        self.toolbar.setEnabled(True)
        self.scan_specific_form.ui.analysis_progress_bar.hide()
        self.scan_specific_form.ui.progress_label.hide()
        self.enable_classif_panel()

    def on_gain_slider_value_changed(self):
        self.ui.gain_lcdnumber.display(self.ui.gain_slider.value())
