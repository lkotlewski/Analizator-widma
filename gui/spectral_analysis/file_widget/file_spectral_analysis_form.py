#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from PyQt4 import QtGui, QtCore

from spectral_analysis_form import SpectralAnalysisForm
from file_specific_form import FileSpecificForm
from analyser import Analyser
from definitions import ROOT_DIR_PATH


class FileSpectralAnalysisForm(SpectralAnalysisForm):
    MEAS_DIR_REL_PATH = 'scanning/measurements'
    TITLE = QtCore.QString(u'Analiza plików pomiarowych')

    def __init__(self, main_window, parent=None):
        SpectralAnalysisForm.__init__(self, main_window, parent)
        self.file_specific_form = FileSpecificForm()
        self.ui.type_specif_layout.addWidget(self.file_specific_form)
        self.measurements_path = os.path.join(ROOT_DIR_PATH, self.MEAS_DIR_REL_PATH)
        self.ui.title_label.setText(self.TITLE)
        self.ui.title_label.move(QtCore.QPoint(310, 30))
        self.ui.start_freq_box.setDisabled(True)
        self.ui.finish_freq_box.setDisabled(True)
        self.ui.probes_number_box.setDisabled(True)
        self.ui.place_text_edit.setDisabled(True)
        self.ui.gain_slider.setDisabled(True)
        self.ui.start_analysis_button.setDisabled(True)


        QtCore.QObject.connect(self.ui.start_analysis_button, QtCore.SIGNAL("clicked()"), self.file_spectral_analysis)
        QtCore.QObject.connect(self.file_specific_form.ui.load_file_button,  QtCore.SIGNAL("clicked()"), self.load_measurements_file)

    def file_spectral_analysis(self):
        if self.chart_plotted:
            self.reset_figure()
        self.analyser.spectral_analyse2(spectrum_axis=self.axis)
        self.canvas.draw()
        self.chart_plotted = True
        self.toolbar.setEnabled(True)
        self.enable_classif_panel()

    def load_measurements_file(self):
        Qfile_path = QtGui.QFileDialog.getOpenFileName(caption='Wybierz plik do analizy',
                                  filter='Pliki pomiarowe (*.p *.bmr)', directory=self.measurements_path)
        self.file_path = str(Qfile_path)
        if self.file_path is not '':
            self.analyser = Analyser(self.file_path)
            self.analyser.print_loaded_file_info()
            self.ui.start_freq_box.setValue(self.analyser.freq_vector[0] / 1e6)
            self.ui.finish_freq_box.setValue(self.analyser.freq_vector[len(self.analyser.freq_vector)-1]/1e6)
            self.ui.probes_number_box.setValue(len(self.analyser.signals_on_all_freq[0]))
            self.ui.gain_slider.setValue(self.analyser.gain)
            self.ui.gain_lcdnumber.display(self.analyser.gain)
            if self.analyser.measurements_place is not None:
                self.ui.place_text_edit.setText(QtCore.QString(self.analyser.measurements_place))
            self.file_specific_form.ui.loaded_file_text_edit.setTextColor(QtGui.QColor(77, 196, 51))
            self.file_specific_form.ui.loaded_file_text_edit.setText(Qfile_path)
            self.ui.start_analysis_button.setEnabled(True)



