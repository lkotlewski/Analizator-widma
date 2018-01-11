#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import os
import graphviz
from sklearn import linear_model
from sklearn import tree
from scipy import fftpack
from enum import Enum
import cPickle
from matplotlib import pyplot as plt

from definitions import ROOT_DIR_PATH

PARAM_TABLE_PATH ='modulation datasets/mod_params_tables.dat'
THRESHOLDS_PATH = 'modulation classification/thresholds.dat'
TREE_CLASSIFIER_REL_PATH = 'modulation classification/tree_classifier.dat'



class ModulationClassifier:

    def __init__(self):
        mod_clf_file = open(os.path.join(ROOT_DIR_PATH, TREE_CLASSIFIER_REL_PATH), 'r')
        self.tree_clf = cPickle.load(mod_clf_file)

    def classify(self, signal, do_plots=False):
        sig_par_calc = SigParamsCalculator(signal, do_plots=do_plots)
        params_vector = sig_par_calc.calculate_all_params()
        params_vector_reshaped = params_vector.reshape(1, -1)
        return self.tree_clf.predict(params_vector_reshaped)[0], params_vector, \
               self.tree_clf.predict_proba(params_vector_reshaped)


class SigParamsCalculator:
    def __init__(self, signal, f_s=None, f_c=0, do_plots=False):
        self.signal = signal
        self.f_s = f_s
        self.f_c = f_c
        self.do_plots = do_plots
        self.amp_vector = abs(self.signal)
        self.phase_vector = phase_vector = np.angle(signal)
        self.phase_unwr_vector = phase_unwr_vector = np.unwrap(phase_vector)

        self.N = N = len(phase_unwr_vector)
        self.x = np.arange(N)
        self.X = self.x.reshape(-1, 1)
        self.A_cn = self.normalize_and_center_amp()
        # self.f = np.array([(phase_unwr_vector[i + 1] - phase_unwr_vector[i]) * self.f_s / (2.0 * np.pi)
        #                    for i in self.x[:-1]])
        self.f = np.array([(phase_unwr_vector[i + 1] - phase_unwr_vector[i]) / (2.0 * np.pi)
                           for i in self.x[:-1]])
        self.f_N = self.normalize_and_center_freq()

    def calculate_all_params(self, print_params=False):
        threshold = 0.2
        gamma_max = self.calc_gamma_max()
        sigma_ap, sigma_dp = self.calc_sigma_ap_and_sigma_dp(threshold)
        sigma_aa = self.calc_sigma_aa()
        sigma_af = self.calc_sigma_af(threshold)
        sigma_a = self.calc_sigma_a(threshold)
        mi_a_42 = self.calc_mi_a_42()
        mi_f_42 = self.calc_mi_f_42()
        if print_params:
            print "\n"
            print 'gamma_max=' + str(gamma_max)
            print 'sigma_ap=' + str(sigma_ap)
            print 'sigma_dp=' + str(sigma_dp)
            print 'sigma_aa=' + str(sigma_aa)
            print 'sigma_af=' + str(sigma_af)
            print 'sigma_a=' + str(sigma_a)
            print 'mi_a_42=' + str(mi_a_42)
            print 'mi_f_42=' + str(mi_f_42)
        if self.f_s is not None:
            P = self.calc_P()
            return np.array([gamma_max, sigma_ap, sigma_dp, sigma_aa, sigma_af, sigma_a, mi_a_42, mi_f_42, P])
        else:
            return np.array([gamma_max, sigma_ap, sigma_dp, sigma_aa, sigma_af, sigma_a, mi_a_42, mi_f_42])

    def calc_gamma_max(self):
        abs_fft = abs(np.fft.fft(self.A_cn))
        if self.do_plots:
            plt.plot(abs_fft)
            plt.title('abs_fft')
            plt.show()
        gamma_max = np.max(np.power(abs_fft, 2)) / self.N
        return gamma_max

    def normalize_and_center_amp(self):
        mean_value = np.mean(self.amp_vector)
        self.A_n = self.amp_vector / mean_value
        A_cn = self.A_n - 1
        if self.do_plots:
            plt.plot(A_cn)
            plt.title('A_cn')
            plt.show()
        return A_cn

    def normalize_and_center_freq(self):
        mean_value = np.mean(self.f)
        f_m = self.f - mean_value
        #f_N = f_m / self.f_s
        f_N = f_m
        if self.do_plots:
            plt.plot(f_N)
            plt.title('f_N')
            plt.show()
        return f_N

    def calc_sigma_ap_and_sigma_dp(self, threshold):
        fi_NL = self.filter_out_lin_comp()
        high_amp_fi_NL = np.array([fi_NL[i] for i in self.x if self.A_n[i] > threshold])
        sigma_ap = np.std(abs(high_amp_fi_NL))
        sigma_dp = np.std(high_amp_fi_NL)
        return sigma_ap, sigma_dp

    def filter_out_lin_comp(self):
        lin_regr = linear_model.LinearRegression()
        phase_unwr_vector = self.phase_unwr_vector.reshape(-1, 1)
        lin_regr.fit(X=self.X, y=phase_unwr_vector)
        phase_lin_comp = lin_regr.predict(self.X)
        fi_NL = phase_unwr_vector - phase_lin_comp
        if self.do_plots:
            plt.plot(self.phase_unwr_vector)
            plt.title('before filtration')
            plt.show()
            plt.plot(fi_NL)
            plt.title('after filtration - fi_NL')
            plt.show()
        return fi_NL

    def calc_P(self):
        X = fftpack.fftshift(np.fft.fft(self.signal))
        N = len(X)
        carrier_idx = int(np.round((self.f_c + 0.5) / self.f_s * N))
        # nr_of_probes_one_side
        nr_os = carrier_idx if carrier_idx < N / 2 else N - carrier_idx - 1
        P_l = sum(np.power(abs(X[carrier_idx - nr_os:carrier_idx]), 2))
        P_u = sum(np.power(abs(X[carrier_idx + 1:carrier_idx + nr_os + 1]), 2))
        P = (P_l - P_u) / (P_l + P_u)
        return P

    def calc_sigma_aa(self):
        sigma_aa = np.std(abs(self.A_cn))
        return sigma_aa

    def calc_sigma_af(self, threshold):
        high_amp_f_N = np.array([self.f_N[i-1] for i in self.x[1:] if self.A_n[i-1] > threshold
                                  and self.A_n[i] > threshold])
        if self.do_plots:
            plt.plot(high_amp_f_N)
            plt.title('high_amp_f_N')
            plt.show()
        sigma_af = np.std(abs(high_amp_f_N))
        return sigma_af

    def calc_sigma_a(self, threshold):
        high_amp_A_cn = np.array([[self.A_cn[i] for i in self.x if self.A_n[i] > threshold]])
        sigma_a = np.std(high_amp_A_cn)
        return sigma_a

    def calc_mi_a_42(self):
        m4 = np.mean(np.power(self.A_cn, 4))
        m2 = np.mean(np.power(self.A_cn, 2))
        mi_a_42 = m4/m2**2
        return mi_a_42

    def calc_mi_f_42(self):
        m4 = np.mean(np.power(self.f_N, 4))
        m2 = np.mean(np.power(self.f_N, 2))
        mi_f_42 = m4 / m2**2
        return mi_f_42


def get_columns_names():
    return ['gamma_max', 'sigma_ap', 'sigma_dp', 'sigma_aa', 'sigma_af', 'sigma_a', 'mi_a_42', 'mi_f_42']


def get_modulations_names():
    return['WBFM', 'BPSK', 'M_PSK', 'M_QAM', 'CPFSK', 'GFSK', 'M_PAM']


def generate_decision_tree_classifier(training_data_file_path):
    training_data_file = open(training_data_file_path, 'r')
    feature_vectors = cPickle.load(training_data_file)
    labels = cPickle.load(training_data_file)
    mod_clf = tree.DecisionTreeClassifier(max_depth=4, min_samples_leaf=100)
    mod_clf.fit(feature_vectors, labels)
    mod_clf_file = open(os.path.join(ROOT_DIR_PATH, TREE_CLASSIFIER_REL_PATH), 'w')
    cPickle.dump(mod_clf, mod_clf_file)


def generate_decision_tree_diagram(pdf_file_name):
    mod_clf_file = open(os.path.join(ROOT_DIR_PATH, TREE_CLASSIFIER_REL_PATH), 'r')
    mod_clf = cPickle.load(mod_clf_file)
    dot_data = tree.export_graphviz(mod_clf, out_file=None, feature_names=get_columns_names(),
                                    class_names=get_modulations_names(), filled=True, rounded=True)
    graph = graphviz.Source(dot_data)
    graph.render(pdf_file_name)


class ModTypes(Enum):

    WBFM = 0
    BPSK = 1
    M_PSK = 2
    M_QAM = 3
    CPFSK = 4
    GFSK = 5
    M_PAM = 6
    # AM_DSB = 7
    # AM_SSB = 8

    def get_string(self):
        return MOD_TYPES_DICT[self.value]


MOD_TYPES_DICT = {
    ModTypes.WBFM.value: 'WFM',
    ModTypes.BPSK.value: 'BPSK',
    ModTypes.M_PSK.value: 'M_PSK',
    ModTypes.M_QAM.value: 'M_QAM',
    ModTypes.CPFSK.value: 'CPFSK',
    ModTypes.GFSK.value: 'GFSK',
    ModTypes.M_PAM.value: 'M_PAM'
}

expected_decisions_dict = {
                           'CPFSK': ModTypes.CPFSK.value,'GFSK': ModTypes.GFSK.value, 'PAM4': ModTypes.M_PAM.value,
                           'BPSK': ModTypes.BPSK.value, 'WBFM': ModTypes.WBFM.value, 'QAM16': ModTypes.M_QAM.value,
                           'QAM64': ModTypes.M_QAM.value, 'QPSK': ModTypes.M_PSK.value, '8PSK': ModTypes.M_PSK.value}


class ParamsIndexes(Enum):
    gamma_max = 0
    sigma_ap = 1
    sigma_dp = 2
    sigma_aa = 3
    sigma_af = 4
    sigma_a = 5
    mi_a_42 = 6
    mi_f_42 = 7


PARAMS_NAMES = ['gamma_max', 'sigma_ap', 'sigma_dp', 'sigma_aa', 'sigma_af', 'sigma_a', 'mi_a_42', 'mi_f_42']


if __name__ == '__main__':
    generate_decision_tree_classifier('/home/ubuntu/Desktop/Analizator widma/modulation datasets/training_data.dat')
    generate_decision_tree_diagram('modulation_decision_tree')
