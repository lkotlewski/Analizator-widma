#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cPickle
import matplotlib.pyplot as plt
import scipy.signal as signal
import numpy as np
import os
import scipy.signal as sig
from scipy import fftpack
import modulation_classifier as mc


class Analyser:
    MEASUREMENTS_DIRECTORY_NAME = "measurements"

    def __init__(self, filename):
        file_to_load = open(filename, "r")
        if filename.endswith('.p'):
            self.strongest_signals_indices = cPickle.load(file_to_load)
            self.signals_on_all_freq = cPickle.load(file_to_load)
            self.signal_len = np.array(self.signals_on_all_freq).shape[1]
            self.power_distribution = cPickle.load(file_to_load)
            self.freq_vector = cPickle.load(file_to_load)
            if len(self.freq_vector) > 1:
                self.freq_step = self.freq_vector[1] - self.freq_vector[0]
            # configuration parameters
            self.samp_rate = cPickle.load(file_to_load)
            self.gain = cPickle.load(file_to_load)
            self.measurements_place = None
            self.file_loaded = True
        elif filename.endswith('.bmr'):
            params_dict = cPickle.load(file_to_load)
            self.strongest_signals_indices = params_dict['strongest_signals_indices']
            self.signals_on_all_freq = params_dict['signals_on_all_freq']
            self.power_distribution = params_dict['power_distribution']
            self.freq_vector = params_dict['freq_vector']
            self.samp_rate = params_dict['samp_rate']
            self.gain = params_dict['gain']
            self.measurements_place = params_dict['measurements_place']
            if len(self.freq_vector) > 1:
                self.freq_step = self.freq_vector[1] - self.freq_vector[0]
            self.file_loaded = True

    def spectral_analyse(self, spectrum_axis=None, use_overlap=True):
        n_per_seg_welch = len(self.signals_on_all_freq[0])/8
        unit_vector_len = n_per_seg_welch
        for idx, signal_on_freq in enumerate(self.signals_on_all_freq):
            signal_freq = self.freq_vector[idx]
            f, pxx = sig.welch(signal_on_freq, fs=self.samp_rate, window='blackman', nperseg=n_per_seg_welch)
            # f, pxx = sig.periodogram(signal_on_freq, fs=self.samp_rate, nfft=n_per_seg_welch)
            f_shifted, pxx_shifted = shift_negative_frequencies(f, pxx)
            f_scaled = f_shifted + signal_freq
            # plt.semilogy(f_scaled, pxx_shifted)
            # plt.show()
            if use_overlap:
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
                    pxx_accurate = np.concatenate((pxx_accurate, (pxx_to_be_averaged + pxx_shifted[:unit_vector_len/2]) / 2), axis=0)
                    pxx_to_be_averaged = pxx_shifted[unit_vector_len/2:]
            else:
                if idx == 0:
                    f_accurate = f_scaled[unit_vector_len/4: unit_vector_len - unit_vector_len/4]
                    pxx_accurate = pxx_shifted[unit_vector_len/4: unit_vector_len - unit_vector_len/4]

                else:
                    f_accurate = np.concatenate((f_accurate, f_scaled[unit_vector_len/4 - 1: unit_vector_len - unit_vector_len/4]), axis=0)
                    pxx_accurate = np.concatenate((pxx_accurate, pxx_shifted[unit_vector_len/4 - 1: unit_vector_len - unit_vector_len/4]), axis=0)

        if spectrum_axis is None:
            plt.semilogy([x / 1e6 for x in f_accurate], pxx_accurate, color='#00aa00ff')
            plt.xlabel(u'Częstotliwość [MHz]')
            plt.ylabel('Moc')
            plt.title(u'Rozkład mocy - rozdzielczość wysoka')
            plt.show()
        else:
            spectrum_axis.semilogy([x / 1e6 for x in f_accurate], pxx_accurate, color='#00aa00ff')
            spectrum_axis.set_xlabel(u'Częstotliwość [MHz]')
            spectrum_axis.set_ylabel('Moc')
            spectrum_axis.set_title(u'Rozkład mocy - rozdzielczość wysoka')
            spectrum_axis.grid(b=True)

    def spectral_analyse2(self, spectrum_axis=None):
        n_per_seg_welch = len(self.signals_on_all_freq[0])/8
        unit_vector_len = n_per_seg_welch
        kaiser_coef = signal.get_window(('kaiser', 8), unit_vector_len)
        for idx, signal_on_freq in enumerate(self.signals_on_all_freq):
            signal_freq = self.freq_vector[idx]
            # plt.plot(np.real(signal_on_freq))
            # plt.show()
            f, pxx = sig.welch(signal_on_freq, fs=self.samp_rate, window='blackman', nperseg=n_per_seg_welch, noverlap=0)
            f_shifted, pxx_shifted = shift_negative_frequencies(f, pxx)
            f_scaled = f_shifted + signal_freq
            # plt.semilogy(f_scaled, pxx_shifted)
            # plt.show()
            pxx_weighted = pxx_shifted*kaiser_coef
            if idx == 0:
                f_accurate = f_scaled[:unit_vector_len/2]
                pxx_accurate = pxx_shifted[:unit_vector_len/2]
                pxx_to_be_added = pxx_weighted[unit_vector_len/2:]
            elif idx == len(self.freq_vector)-1:
                f_accurate = np.concatenate((f_accurate, f_scaled), axis=0)
                pxx_accurate = np.concatenate((pxx_accurate, (pxx_to_be_added + pxx_weighted[:unit_vector_len / 2])), axis=0)
                pxx_accurate = np.concatenate((pxx_accurate, pxx_shifted[unit_vector_len/2:]), axis=0)
            else:
                f_accurate = np.concatenate((f_accurate, f_scaled[:unit_vector_len/2]), axis=0)
                pxx_accurate = np.concatenate((pxx_accurate, (pxx_to_be_added + pxx_weighted[:unit_vector_len/2])), axis=0)
                pxx_to_be_added = pxx_weighted[unit_vector_len/2:]

        if spectrum_axis is None:
            plt.plot([x / 1e6 for x in f_accurate], 10*np.log10(pxx_accurate/2.3e-5), color='#00aa00ff')
            plt.xlabel(u'Częstotliwość [MHz]')
            plt.ylabel(u'Widmowa gęstość mocy [dBFs]')
            plt.title(u'Rozkład mocy - rozdzielczość wysoka')
            plt.show()
        else:
            spectrum_axis.plot([x / 1e6 for x in f_accurate], 10*np.log10(pxx_accurate/2.3e-5), color='#00aa00ff')
            spectrum_axis.set_xlabel(u'Częstotliwość [MHz]')
            spectrum_axis.set_ylabel(u'Widmowa gęstość mocy [dBFs]')
            spectrum_axis.set_title(u'Rozkład mocy - rozdzielczość wysoka')
            spectrum_axis.grid(b=True)

    def single_analyse(self, idx):
        signal_freq = self.freq_vector[idx]
        f, pxx = sig.welch(self.signals_on_all_freq[idx], fs=self.samp_rate)
        f_shifted, pxx_shifted = shift_negative_frequencies(f, pxx)
        f_scaled = f_shifted + signal_freq
        plt.plot([x / 1e6 for x in f_scaled], 10*np.log10(pxx_shifted/2.3e-5))
        plt.xlabel(u'Częstotliwość [MHz]')
        plt.ylabel(u'Widmowa gęstość mocy [dBFs]')
        plt.title(u'Rozkład mocy - rozdzielczość wysoka')
        plt.show()

    def plot_illustrative_distribution(self):
        plt.semilogy([x / 1e6 for x in self.freq_vector], self.power_distribution)
        plt.xlabel('Czestotliwosc [MHz]')
        plt.ylabel('Moc')
        plt.title('Rozklad mocy - rozdzielczosc pogladowa')
        plt.show()

    def get_sig_from_bandwidth(self, low_cut_freq, high_cut_freq, window='boxcar'):
        freq_vector_len = len(self.freq_vector)
        if high_cut_freq - low_cut_freq > self.samp_rate/2:
            return None
        if low_cut_freq < self.freq_vector[0] - self.samp_rate/2 \
                or high_cut_freq > self.freq_vector[freq_vector_len - 1] + self.samp_rate/2:
            return None
        freq_index = int(round(((high_cut_freq + low_cut_freq)/2.0 - self.freq_vector[0])/self.freq_step))
        if freq_index == -1:
            freq_index = 0
        if freq_index == freq_vector_len:
            freq_index = freq_index - 1
        raw_signal = self.signals_on_all_freq[freq_index]
        filtered_signal = pass_selected_frequencies(raw_signal=raw_signal,
                                                    low_cut_freq=low_cut_freq-self.freq_vector[freq_index],
                                                    high_cut_freq=high_cut_freq-self.freq_vector[freq_index],
                                                    samp_rate=self.samp_rate, window=window,
                                                    center_freq=self.freq_vector[freq_index])
        print 'power before filtration = ' + str(np.sum(np.power(np.abs(np.array(raw_signal, 'D')), 2)))
        print 'power after filtration =' + str(np.sum(np.power(np.abs(filtered_signal), 2)))
        return filtered_signal


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
            # if self.measurements_place is not None:
                # print 'measurements_place: %(measurements_place)' % {'measurements_place': self.measurements_place}


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


def pass_selected_frequencies(raw_signal, low_cut_freq, high_cut_freq, samp_rate, window, center_freq=None):
    nyq = samp_rate / 2.0
    filter_order = 21
    h_symetric = sig.firwin(filter_order, [(high_cut_freq - low_cut_freq) / 2.0], nyq=nyq, window=window)

    freq_shift = (high_cut_freq + low_cut_freq) / 2.0
    h = [h_symetric[n] * np.exp(1j * 2 * np.pi * freq_shift / samp_rate * n) for n in range(len(h_symetric))]
    filtered_sig = sig.lfilter(h, [1], raw_signal)
    # freqs = fftpack.fftfreq(len(raw_signal), 1.0/samp_rate)
    # raw_sig_fft = np.fft.fft(raw_signal)
    # filtered_sig_fft = np.fft.fft(filtered_sig)
    # shifted_Mhz_freqs = fftpack.fftshift(freqs)/ 1e6
    # plt.plot(shifted_Mhz_freqs, fftpack.fftshift(raw_sig_fft))
    # plt.show()
    # plt.plot(shifted_Mhz_freqs, fftpack.fftshift(filtered_sig_fft))
    # plt.show()

    # b_symetric, a = sig.butter(5, Wn=((high_cut_freq - low_cut_freq) / 2.0) / nyq)
    # b = [b_symetric[n] * np.exp(1j * 2 * np.pi * freq_shift / samp_rate * n) for n in range(len(b_symetric))]
    #
    # z, p, k =zplane.zplane(b_symetric, a)
    # print p
    # z, p, k = zplane.zplane(b, a)
    # print p
    # filtered_sig = sig.lfilter(b, a, raw_signal)
    freqs = fftpack.fftfreq(len(raw_signal), 1.0 / samp_rate)
    raw_sig_fft = np.fft.fft(raw_signal)
    filtered_sig_fft = np.fft.fft(filtered_sig)
    shifted_Mhz_freqs = fftpack.fftshift(freqs) / 1e6
    if center_freq is not None:
        shifted_Mhz_freqs = shifted_Mhz_freqs + center_freq / 1e6
    plt.plot(shifted_Mhz_freqs, fftpack.fftshift(abs(raw_sig_fft)))
    plt.title('Widmo przed filtracja')
    plt.xlabel('Czestotliwosc [MHz]')
    plt.ylabel('Moc')
    plt.show()
    plt.plot(shifted_Mhz_freqs, fftpack.fftshift(abs(filtered_sig_fft)))
    plt.title('Widmo po filtracji')
    plt.xlabel('Czestotliwosc [MHz]')
    plt.ylabel('Moc')
    plt.show()
    return filtered_sig[filter_order:]


def plot_filter_amp_response(b, a):
    w, h = sig.freqs(b, a)
    plt.semilogx(w, 20 * np.log10(abs(h)))
    plt.xlabel('Czestotliowsc unormowana')
    plt.ylabel('Charakterystyka amplitudowa')
    plt.grid()
    plt.show()

def classify_modulation(signal_list):
    mc.classify(np.array(signal_list, 'D'))



if __name__ == "__main__":
    # a = Analyser(os.path.join(os.getcwd(), Analyser.MEASUREMENTS_DIRECTORY_NAME, '2017-12-03-23:46_ogolna_80-120.p'))
    #a = Analyser(os.path.join(os.getcwd(), Analyser.MEASUREMENTS_DIRECTORY_NAME, '2017-11-27-21:37_ogolna_80-1000.p'))
    a = Analyser(os.path.join(os.getcwd(), Analyser.MEASUREMENTS_DIRECTORY_NAME, '2018-01-10-16:11_politechnika_80-115.bmr'))
    a.spectral_analyse2()
    for sig in a.signals_on_all_freq:
        print len(sig)
    #a = Analyser(os.path.join(os.getcwd(), Analyser.MEASUREMENTS_DIRECTORY_NAME, '2017-12-22-12:16_fm_2k_dev75_m70dBm_109-111.bmr'))
    real_part_set = set()
    for j in range(len(a.signals_on_all_freq)):
        real_part =[a.signals_on_all_freq[j][i].real for i in range(len(a.signals_on_all_freq[0]))]
        subset = set(real_part)
        real_part_set = real_part_set.union(subset)
    print len(real_part_set)
    values_list = sorted(real_part_set)
    differences_list = [values_list[i+1] - values_list[i] for i in range(len(values_list)-1)]
    print values_list
    print differences_list
    print values_list[len(values_list)-1] + values_list[0]
    # filtered = a.get_sig_from_bandwidth(110.22e6, 110.26e6)
    # sig_par_calc = mc.SigParamsCalculator(filtered, do_plots=False)
    # sig_par_calc.calculate_all_params(print_params=False)

    # filtered = a.get_sig_from_bandwidth(96.0e6, 96.9e6)
    # sig_par_calc = mc.SigParamsCalculator(filtered, do_plots=True)
    # sig_par_calc.calculate_all_params(print_params=True)


    # t = np.arange(512)
    # complex_sin = np.cos(2*np.pi/5*t) + 1j*np.sin(2*np.pi/5*t)
    # sig_par_calc = mc.SigParamsCalculator(complex_sin, do_plots=False)
    # sig_par_calc.calculate_all_params(print_params=True)

    # a.print_loaded_file_info()
    #a.spectral_analyse()
    # WBFM_set_file = open('/home/ubuntu/Desktop/Analizator widma/Analizator-widma/'
    #                      'modulation datasets/separated_modulation_files/WBFM_18.dat', 'r')
    # generated_WBFM_set = cPickle.load(WBFM_set_file)
    # gen_sig = generated_WBFM_set[96]
    # raw_sig_fft = np.fft.fft(gen_sig)
    # plt.plot(fftpack.fftshift(raw_sig_fft))
    # plt.title('Wygenerowany sztucznie')
    # plt.show()
    # fm_freq_vector = np.array([94.0, 95.8, 105.6, 107.5])
    # fm_freq_vector = np.array([88.4, 89.0, 89.8, 91.0, 92.0, 92.4, 93.3, 94.0, 95.8, 96.5, 97.7, 98.3, 98.8, 100.1,
    #                            101.0, 105.6, 107.5])
    # fm_freq_vector = fm_freq_vector * 1e6
    # for freq in fm_freq_vector:
    #     print '\nfreq=' + str(freq/1e6)
    #     filtered = a.get_sig_from_bandwidth(freq-0.1e6, freq+0.1e6)
    #     sig_par_calc = mc.SigParamsCalculator(filtered, do_plots=True)
    #     sig_par_calc.calculate_all_params(print_params=True)

    # filtered = a.get_sig_from_bandwidth(88.3e6, 88.5e6)
    # sig_par_calc = mc.SigParamsCalculator(filtered)
    # sig_par_calc.calculate_all_params(print_params=True)
    #
    # filtered = a.get_sig_from_bandwidth(93.9e6, 94.1e6)
    # sig_par_calc = mc.SigParamsCalculator(filtered, do_plots=True)
    # sig_par_calc.calculate_all_params(print_params=True)
    #
    # filtered = a.get_sig_from_bandwidth(100.9e6, 101.1e6)
    # sig_par_calc = mc.SigParamsCalculator(filtered)
    # sig_par_calc.calculate_all_params(print_params=True)
    #
    # filtered = a.get_sig_from_bandwidth(181.1e6, 181.4e6)
    # sig_par_calc = mc.SigParamsCalculator(filtered)
    # sig_par_calc.calculate_all_params(print_params=True)
    #
    # filtered = a.get_sig_from_bandwidth(479.9e6, 480.1e6)
    # sig_par_calc = mc.SigParamsCalculator(filtered)
    # sig_par_calc.calculate_all_params(print_params=True)
    #
    # filtered = a.get_sig_from_bandwidth(519.6e6, 519.7e6)
    # sig_par_calc = mc.SigParamsCalculator(filtered)
    # sig_par_calc.calculate_all_params(print_params=True)
    #
    # filtered = a.get_sig_from_bandwidth(935.6e6, 935.9e6)
    # sig_par_calc = mc.SigParamsCalculator(filtered)
    # sig_par_calc.calculate_all_params(print_params=True)

    # sig_par_calc = mc.SigParamsCalculator()
    # classifier = mc.ModulationClassifier()
    # recognized_mod_type = classifier.classify(filtered_sig)
    # print str(recognized_mod_type)
