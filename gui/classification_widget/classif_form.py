# -*- coding: utf-8 -*
import cPickle
from PyQt4 import QtGui
from matplotlib.gridspec import GridSpec
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from os import path

from definitions import ROOT_DIR_PATH
from classif_base import Ui_ClassifBase
from modulation_classifier import ModulationClassifier, MOD_TYPES_DICT, PARAMS_NAMES


class ClassifForm(QtGui.QWidget):
    RECOGNIZE_BEGIN_TEXT = u'Modulacja sygnału została rozpoznana jako : '
    MI_VECTORS_REL_PATH = 'modulation datasets/mapped_mod_mi_vectors.dat'

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_ClassifBase()
        self.ui.setupUi(self)
        self.figure = Figure()
        self.grid = GridSpec(2, 4)
        self.canvas = FigureCanvas(self.figure)
        self.ui.bar_charts_layout.addWidget(self.canvas)
        mi_vectors_file = open(path.join(ROOT_DIR_PATH, self.MI_VECTORS_REL_PATH), 'r')
        self.mi_vectors_dict = cPickle.load(mi_vectors_file)

    def generate_layout(self, signal, do_plots=False):
        mod_clf = ModulationClassifier()
        decision, params_vector, mods_proba = mod_clf.classify(signal, do_plots=do_plots)
        print mods_proba
        decision_str_repr = MOD_TYPES_DICT[decision]
        self.ui.recognized_mod_label.setText(self.RECOGNIZE_BEGIN_TEXT + decision_str_repr)
        self._generate_bar_charts(params_vector, self.mi_vectors_dict[decision_str_repr], PARAMS_NAMES,
                                  'bad.', 'sr.' + decision_str_repr)

    def _generate_bar_charts(self, features_a, features_b, features_names, a_name, b_name):
        for idx, feature in enumerate(features_names):
            axis = self.figure.add_subplot(self.grid[idx])
            bar_pos = [1, 3]
            values = [features_a[idx], features_b[idx]]
            bar_list = axis.bar(bar_pos, values , align='center')
            bar_list[0].set_color('#40e854')
            bar_list[1].set_color('#aa43ef')
            axis.set_ylabel(u"Wartość parametru")
            axis.set_xticks(bar_pos)
            axis.set_xticklabels([a_name, b_name])
            axis.set_title(feature)

            bars = axis.patches
            labels = ["{0:.2g}".format(values[i]) for i in range(len(bars))]
            for bar, label in zip(bars, labels):
                height = bar.get_height()
                axis.text(bar.get_x() + bar.get_width() / 2, height/2, label, ha='center', va='bottom')

        self.figure.tight_layout()
        self.canvas.draw()



