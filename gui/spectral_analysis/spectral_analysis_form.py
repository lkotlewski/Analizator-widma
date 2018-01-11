#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt4 import QtGui, QtCore
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
from enum import Enum

from spectral_analysis_base import Ui_SpectralAnalysisFormBase

CURSORS_ACTIVE_STYLE = """
QAction{
font-weight : bold;
}
"""
CURSORS_INACTIVE_STYLE = """
QAction{
font-weight : normal;
}
"""


class SpectralAnalysisForm(QtGui.QWidget):
    ACTIVATE_CURSORS_TEXT = QtCore.QString(u'Włącz kursory')
    INACTIVATE_CURSORS_TEXT = QtCore.QString(u'Wyłącz kursory')
    windows = ['boxcar', 'blackman', 'hamming', 'hann', 'bartlett', 'flattop', 'parzen', 'bohman', 'blackmanharris',
               'nuttall', 'barthann']
    STYLE = 'QSlider{color:green;}'

    def __init__(self, main_window, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_SpectralAnalysisFormBase()
        self.ui.setupUi(self)
        self.main_window = main_window
        self.setStyleSheet(SpectralAnalysisForm.STYLE)

        self.figure = Figure()
        self.figure.subplots_adjust(bottom=0.15, left=0.15)
        self.axis = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.toolbar.setDisabled(True)
        self.ui.figure_layout.addWidget(self.canvas)
        self.ui.figure_layout.addWidget(self.toolbar)

        self.cursors_active = False
        self.cursors_action = QtGui.QAction(self.ACTIVATE_CURSORS_TEXT, self.toolbar)
        self.cursor_one = self.axis.axvline(None, color='b', picker=3)
        self.cursor_two = self.axis.axvline(None, color='r', picker=3)
        self.toolbar.addAction(self.cursors_action)
        self.selected_cursor = SelectedCursor.NONE

        self.analyser = None

        self.chart_plotted = False
        self.ui.low_cut_freq_edit.setDisabled(True)
        self.ui.high_cut_freq_edit.setDisabled(True)
        self.ui.classif_button.setDisabled(True)
        self.ui.window_combo_box.setDisabled(True)
        self.ui.window_combo_box.addItems(QtCore.QStringList(self.windows))
        self.ui.plots_check_box.setDisabled(True)

        QtCore.QObject.connect(self.cursors_action, QtCore.SIGNAL("triggered()"), self.cursors_action_triggered)
        QtCore.QObject.connect(self.ui.classif_button, QtCore.SIGNAL("clicked()"), self.classif_button_clicked)

    def on_figure_clicked(self, event):
        if not (self.toolbar._active == "ZOOM" or self.toolbar._active == "PAN"):
            if self.selected_cursor == SelectedCursor.FIRST:
                self.cursor_one.set_xdata(event.xdata)
            if self.selected_cursor == SelectedCursor.SECOND:
                self.cursor_two.set_xdata(event.xdata)
            self.canvas.draw()
            self.low_cut_freq = min(self.cursor_one.get_xdata(), self.cursor_two.get_xdata())
            self.high_cut_freq = max(self.cursor_one.get_xdata(), self.cursor_two.get_xdata())
            self.ui.low_cut_freq_edit.setText('{0:.2f}'.format(self.low_cut_freq))
            self.ui.high_cut_freq_edit.setText('{0:.2f}'.format(self.high_cut_freq))

    def cursors_action_triggered(self):
        self.cursors_active = not self.cursors_active
        if self.cursors_active:
            self.cid = self.canvas.mpl_connect('button_press_event', self.on_figure_clicked)
            self.cid_2 = self.canvas.mpl_connect('pick_event', self.cursor_pick)
            axis_lower_bound = self.axis.get_xbound()[0]
            axis_upper_bound = self.axis.get_xbound()[1]
            cursor_x_value = axis_lower_bound + (axis_upper_bound - axis_lower_bound)/10
            self.cursor_one.set_xdata(cursor_x_value)
            self.cursor_two.set_xdata(cursor_x_value)
            self.setStyleSheet(CURSORS_ACTIVE_STYLE)
            self.cursors_action.setText(self.INACTIVATE_CURSORS_TEXT)
        else:
            self.canvas.mpl_disconnect(self.cid)
            self.canvas.mpl_disconnect(self.cid_2)
            self.setStyleSheet(CURSORS_INACTIVE_STYLE)
            self.cursors_action.setText(self.ACTIVATE_CURSORS_TEXT)

        self.selected_cursor = SelectedCursor.FIRST

    def cursor_pick(self, event):
        line_color = event.artist.get_color()
        if line_color == 'b':
            self.selected_cursor = SelectedCursor.FIRST
        elif line_color == 'r':
            self.selected_cursor = SelectedCursor.SECOND
        else:
            self.selected_cursor = SelectedCursor.NONE

    def reset_figure(self):
        self.figure.clf()
        self.axis = self.figure.add_subplot(111)
        if self.cursors_active:
            self.cursors_active = False
            self.canvas.mpl_disconnect(self.cid)
            self.canvas.mpl_disconnect(self.cid_2)
        self.selected_cursor = SelectedCursor.NONE
        self.cursors_action.setText(self.ACTIVATE_CURSORS_TEXT)
        self.cursor_one = self.axis.axvline(None, color='b', picker=3)
        self.cursor_two = self.axis.axvline(None, color='r', picker=3)

    def enable_classif_panel(self):
        self.ui.low_cut_freq_edit.setEnabled(True)
        self.ui.high_cut_freq_edit.setEnabled(True)
        self.ui.classif_button.setEnabled(True)
        self.ui.window_combo_box.setEnabled(True)
        self.ui.plots_check_box.setEnabled(True)

    def classif_button_clicked(self):
        signal = self.analyser.get_sig_from_bandwidth(low_cut_freq=float(str(self.ui.low_cut_freq_edit.text())) * 1e6,
                                                      high_cut_freq=float(str(self.ui.high_cut_freq_edit.text())) * 1e6,
                                                      window=str(self.ui.window_combo_box.currentText()))
        self.main_window.show_classif_layout(signal, do_plots=self.ui.plots_check_box.isChecked())


class SelectedCursor(Enum):
    NONE = 0
    FIRST = 1
    SECOND = 2


