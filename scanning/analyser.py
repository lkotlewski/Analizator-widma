#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cPickle
import numpy as np
import scipy.signal as sig
import matplotlib.pyplot as plt
from enum import Enum
import os


class Analyser:
    MEASUREMENTS_DIRECTORY_NAME = "measurements"

    def __init__(self):
        pass

    def load_measurements(self, filename):
        file_to_load = open(filename, "r")
        self.strongest_signals_indices = cPickle.load(file_to_load)
        self.signals_on_all_freq = cPickle.load(file_to_load)
        self.power_distribution = cPickle.load(file_to_load)
        self.freq_vector = cPickle.load(file_to_load)
        # configuration parameters
        self.samp_rate = cPickle.load(file_to_load)
        self.gain = cPickle.load(file_to_load)
        self.use_filter = cPickle.load(file_to_load)
        if self.use_filter:
            # filter configuration params
            self.filter_gain = cPickle.load(file_to_load)
            self.low_cutoff_freq = cPickle.load(file_to_load)
            self.high_cutoff_freq = cPickle.load(file_to_load)
            self.transition_width = cPickle.load(file_to_load)
            self.filter_win = cPickle.load(file_to_load)
        self.file_loaded = True

    def analyse(self):
        n_per_seg_welch = 256
        unit_vector_len = n_per_seg_welch
        for idx, signal_on_freq in enumerate(self.signals_on_all_freq):
            signal_freq = self.freq_vector[idx]
            f, pxx = sig.welch(signal_on_freq, fs=self.samp_rate, nperseg=n_per_seg_welch)
            f_shifted, pxx_shifted = shift_negative_frequencies(f, pxx)
            f_scaled = f_shifted + signal_freq
            if idx == 0:
                f_accurate = f_scaled[:unit_vector_len/2]
                pxx_accurate = pxx_shifted[:unit_vector_len/2]
                pxx_to_be_averaged = pxx_shifted[unit_vector_len/2:]
            elif idx == len(self.freq_vector)-1:
                f_accurate = np.concatenate((f_accurate, f_scaled), axis=0)
                pxx_accurate = np.concatenate((pxx_accurate, (pxx_to_be_averaged + pxx_shifted[:unit_vector_len / 2]) / 2), axis=0)
                pxx_accurate = np.concatenate((pxx_accurate, pxx_shifted[unit_vector_len/2:]), axis=0)
            else:
                f_accurate = np.concatenate((f_accurate, f_scaled[:unit_vector_len/2]), axis=0)
                pxx_accurate = np.concatenate((pxx_accurate, (pxx_to_be_averaged+ pxx_shifted[:unit_vector_len/2]) / 2), axis=0)
                pxx_to_be_averaged = pxx_shifted[unit_vector_len/2:]

        plt.semilogy([x / 1e6 for x in f_accurate], pxx_accurate)
        plt.xlabel('Czestotliwosc [MHz]')
        plt.ylabel('Moc')
        plt.title('Rozklad mocy - rozdzielczosc wysoka')
        plt.show()

    def single_analyse(self, idx):
        signal_freq = self.freq_vector[idx]
        f, pxx = sig.welch(self.signals_on_all_freq[idx], fs=self.samp_rate)
        f_shifted, pxx_shifted = shift_negative_frequencies(f, pxx)
        f_scaled = f_shifted + signal_freq
        plt.semilogy([x / 1e6 for x in f_scaled], pxx_shifted)
        plt.xlabel('Czestotliwosc [MHz]')
        plt.ylabel('Moc')
        plt.title('Rozklad mocy - rozdzielczosc wysoka')
        plt.show()

    def plot_illustrative_distribution(self):
        plt.semilogy([x / 1e6 for x in self.freq_vector], self.power_distribution)
        plt.xlabel('Czestotliwosc [MHz]')
        plt.ylabel('Moc')
        plt.title('Rozklad mocy - rozdzielczosc pogladowa')
        plt.show()

    def print_strongest_freq_info(self):
        print "\n Czestotliwosci, na ktorych sygnal jest najsilniejszy:"
        for idx, signal_idx in enumerate(reversed(self.strongest_signals_indices)):
            print '%(idx)d. freq = %(freq).2f [MHz]  power = %(power)f' \
                  % {'idx': idx + 1, 'freq': self.freq_vector[signal_idx] / 1e6,
                     'power': self.power_distribution[signal_idx]}

    def print_loaded_file_info(self):
        if not self.file_loaded:
            print 'no file loaded'
        else:
            print 'samp_rate: %(samp_rate).2f [MHz]' % {'samp_rate': self.samp_rate / 1e6}
            print 'gain: %(gain)2f ' % {'gain': self.gain}
            print 'start_freq: %(start_freq).2f [MHz]' % {'start_freq': self.freq_vector[0] / 1e6}
            print 'finish_freq: %(finish_freq)2f [MHz]' % {
                'finish_freq': self.freq_vector[len(self.freq_vector) - 1] / 1e6}
            print 'resolution: %(resolution).2f[MHz]' % {'resolution': (self.freq_vector[1] - self.freq_vector[0]) / 1e6}
            print 'filter used: %(filter_used)r' % {'filter_used': self.use_filter}
            if self.use_filter:
                print 'filter_gain %(filter_gain).2f' % {'filter_gain': self.filter_gain}
                print 'low_cutoff_freq: %(low_cutoff_freq)d [Hz]' % {'low_cutoff_freq': self.low_cutoff_freq}
                print 'high_cutoff_freq: %(high_cutoff_freq)d [Hz]' % {'high_cutoff_freq': self.high_cutoff_freq}
                print 'transition_width: %(transition_width)d [Hz]' % {'transition_width': self.transition_width}
                print 'filter_win: %(filter_win)s' % {'filter_win': FilterTypes(self.filter_win).name}


def shift_negative_frequencies(f, pxx):
    vector_size = len(f)
    if vector_size % 2 == 0:
        f_shifted = np.concatenate((f[vector_size / 2:], f[:vector_size / 2]), axis=0)
        pxx_shifted = np.concatenate((pxx[vector_size / 2:], pxx[:vector_size / 2]), axis=0)
        return f_shifted, pxx_shifted
    else:
        f_shifted = np.concatenate((f[(vector_size+1) / 2:], f[:(vector_size+1) / 2]), axis=0)
        pxx_shifted = np.concatenate((pxx[(vector_size+1) / 2:], pxx[:(vector_size+1) / 2]), axis=0)
        return f_shifted, pxx_shifted


class FilterTypes(Enum):
    WIN_BARTLETT = 6
    WIN_BLACKMAN = 2
    WIN_BLACKMAN_HARRIS = 5
    WIN_FLATTOP = 7
    WIN_HAMMING = 0
    WIN_HANN = 1
    WIN_KAISER = 4
    WIN_NONE = -1
    WIN_RECTANGULAR = 3


if __name__ == "__main__":
    a = Analyser()
    a.load_measurements(os.path.join(os.getcwd(), Analyser.MEASUREMENTS_DIRECTORY_NAME, '2017-11-04-13:54_ogolna_88-89.p'))
    a.print_loaded_file_info()
    a.analyse()
