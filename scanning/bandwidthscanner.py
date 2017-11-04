#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Sampling
# Generated: Sat Jun 17 20:15:31 2017
##################################################

from gnuradio import blocks
from gnuradio import fft
from gnuradio import filter
from gnuradio import gr
from gnuradio.fft import window
from gnuradio.filter import firdes
from analyser import Analyser
import osmosdr
import time
import numpy as np
import cPickle
import datetime
import os


class BandwidthScanner(gr.top_block):

    def __init__(self,  samp_rate=2e6, gain=40, window_size=4096, number_of_indices_to_remember=20, use_filter=False,
                 low_cutoff_freq=70, high_cutoff_freq=100e3, transition_width=70e3, filter_win=firdes.WIN_HAMMING):
        gr.top_block.__init__(self, "BandwithScanner")

        ##################################################
        # Variables
        ##################################################
        self.use_filter = use_filter
        self.samp_rate = samp_rate
        self.gain = gain
        self.window_size = window_size
        self.raw_signal = []
        self.fft_mag = []
        self.signals_on_all_freq = []
        self.fft_mag_on_all_freq = []
        self.power_distribution = []
        self.power_distribution2 = []
        self.strongest_signals_indices = []
        self.number_of_indices_to_remember = number_of_indices_to_remember
        self.sleep_time_after_tuning = 0.2
        # filter params
        self.filter_gain = filter_gain = 50
        self.low_cutoff_freq = low_cutoff_freq
        self.high_cutoff_freq = high_cutoff_freq
        self.transition_width = transition_width
        self.filter_win = filter_win

        ##################################################dow
        # Blocks
        ##################################################
        self.rtlsdr_source = osmosdr.source(args="numchan=" + str(1) + " " + '')
        self.rtlsdr_source.set_sample_rate(self.samp_rate)
        self.rtlsdr_source.set_center_freq(100e6, 0)
        self.rtlsdr_source.set_freq_corr(0, 0)
        self.rtlsdr_source.set_iq_balance_mode(False, 0)
        self.rtlsdr_source.set_gain_mode(False, 0)
        self.rtlsdr_source.set_gain(gain)
        self.rtlsdr_source.set_antenna('', 0)

        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex * 1, self.window_size)
        self.blocks_probe_raw_signal = blocks.probe_signal_vc(self.window_size)
        self.blocks_probe_fft_mag = blocks.probe_signal_vf(self.window_size)
        self.fft_vxx_0 = fft.fft_vcc(self.window_size, True, (window.blackmanharris(self.window_size)), True, 1)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(self.window_size)
        self.band_pass_filter_0 = filter.fir_filter_ccf(1, firdes.band_pass(
            gain=filter_gain, sampling_freq=samp_rate, low_cutoff_freq=low_cutoff_freq, high_cutoff_freq=high_cutoff_freq,
            transition_width=transition_width, window=filter_win))

        ##################################################
        # Connections
        ##################################################

        if use_filter:
            self.connect((self.rtlsdr_source, 0), (self.band_pass_filter_0, 0))
            self.connect((self.band_pass_filter_0, 0), (self.blocks_stream_to_vector_0, 0))
        else:
            self.connect((self.rtlsdr_source, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.blocks_probe_raw_signal, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.fft_vxx_0, 0))
        self.connect((self.fft_vxx_0, 0), (self.blocks_complex_to_mag_squared_0, 0))
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.blocks_probe_fft_mag, 0))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.rtlsdr_source.set_sample_rate(self.samp_rate)
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)

    def get_raw_signal(self):
        return self.raw_signal

    def set_raw_signal(self, raw_signal):
        self.raw_signal = raw_signal

    def get_fft_mag(self):
        return self.fft_mag

    def set_fft_mag(self, fft_mag):
        self.fft_mag = fft_mag

    def fast_analize(self, start_freq=88e6, finish_freq=120e6, resolution=1e6):
        freq_vector = np.linspace(start_freq, finish_freq, round((finish_freq-start_freq)/resolution)+1)
        # freq_array= np.empty(16)
        # freq_array.fill(94.8e6)
        # freq_vector= freq_array.tolist()
        freq_index = 0
        self.start()
        time.sleep(1)  # time for hardware to init
        while freq_index < len(freq_vector):
            self.tune_to_freq(freq_vector[freq_index])
            time.sleep(self.sleep_time_after_tuning)
            signal_on_current_freq = self.blocks_probe_raw_signal.level()
            fft_mag_on_current_freq = self.blocks_probe_fft_mag.level()
            self.signals_on_all_freq.append(signal_on_current_freq)
            power = self.calculate_power(signal_on_current_freq)
            power2 = self.calculate_power_from_fft_mag(fft_mag_on_current_freq)
            self.power_distribution.append(power)
            self.power_distribution2.append(power2)
            self.remember_strongest_signals_indices(power2, freq_index)
            print 'Moc sygnału wokół częstotliwości %(freq)2f [MHz] = %(power)f, %(power2)f' \
                  % {'freq': freq_vector[freq_index] / 1e6, 'power': power, 'power2': power2}
            freq_index += 1
        self.stop()
        self.save_measurements(freq_vector)

    def tune_to_freq(self, freq):
        if self.rtlsdr_source.get_center_freq() == freq:
            pass
        else:
            self.rtlsdr_source.set_center_freq(freq, 0)

    def calculate_power(self, signal):
        power_sum = 0
        for probe in signal:
            power_sum += probe.real**2 + probe.imag**2
        power = power_sum / len(signal)
        return power

    def calculate_power_from_fft_mag(self, fft_magt):
        power_sum = 0
        for probe in fft_magt:
            power_sum += probe
        power = power_sum / len(fft_magt)
        return power

    def clear_signal_buffer(self):
        self.signal_buffer = []

    def remember_strongest_signals_indices(self, new_power, new_idx_power_distribution):
        number_of_remember_indices = len(self.strongest_signals_indices)
        list_full = number_of_remember_indices == self.number_of_indices_to_remember
        add_new_idx = not list_full
        if number_of_remember_indices > 0:
            for idx, idx_power_distribution in enumerate(self.strongest_signals_indices):
                if self.power_distribution2[idx_power_distribution] < new_power:
                    add_new_idx = True
                    if idx == number_of_remember_indices - 1:  # all values checked
                        self.strongest_signals_indices.insert(idx + 1, new_idx_power_distribution)
                        if list_full:
                            self.strongest_signals_indices.pop(0)
                        break                                  # if no break, next iteration, with just added value
                else:
                    if add_new_idx:
                        self.strongest_signals_indices.insert(idx, new_idx_power_distribution)
                        if list_full:
                            self.strongest_signals_indices.pop(0)
                        break
        else:
            self.strongest_signals_indices.insert(0, new_idx_power_distribution)

    def save_measurements(self, freq_vector):
        measurements_place = 'ogolna'
        current_time = datetime.datetime.now()
        current_time_str = current_time.strftime("%Y-%m-%d-%H:%M")
        current_directory = os.getcwd()
        self.out_filename = current_time_str + '_' + measurements_place
        self.out_filename += '_' + str(int(round(freq_vector[0]/1e6))) + '-' + str(int(round(freq_vector[len(freq_vector)-1]/1e6))) + '.p'
        out_file = open(os.path.join(current_directory, Analyser.MEASUREMENTS_DIRECTORY_NAME, self.out_filename), "w")
        cPickle.dump(self.strongest_signals_indices, out_file)
        cPickle.dump(self.signals_on_all_freq, out_file)
        cPickle.dump(self.power_distribution2, out_file)
        cPickle.dump(freq_vector, out_file)
        # configuration parameters
        cPickle.dump(self.samp_rate, out_file)
        cPickle.dump(self.gain, out_file)
        cPickle.dump(self.use_filter, out_file)
        if self.use_filter:
            # filter configuration params
            cPickle.dump(self.filter_gain, out_file)
            cPickle.dump(self.low_cutoff_freq, out_file)
            cPickle.dump(self.high_cutoff_freq, out_file)
            cPickle.dump(self.transition_width, out_file)
            cPickle.dump(self.filter_win, out_file)




if __name__ == "__main__":
    tb = BandwidthScanner(samp_rate=2e6, gain=40, window_size=4096, number_of_indices_to_remember=20, use_filter=False,
                          low_cutoff_freq=70, high_cutoff_freq=100e3, transition_width=70e3, filter_win=firdes.WIN_HAMMING)
    tb.fast_analize(start_freq=88e6, finish_freq=120e6, resolution=1e6)
    a = Analyser()
    a.load_measurements(os.path.join(os.getcwd(), Analyser.MEASUREMENTS_DIRECTORY_NAME, tb.out_filename))
    a.print_loaded_file_info()
    a.analyse()

