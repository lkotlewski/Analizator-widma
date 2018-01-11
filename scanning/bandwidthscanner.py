#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Sampling
# Generated: Sat Jun 17 20:15:31 2017
##################################################

from gnuradio import blocks
from gnuradio import gr
from analyser import Analyser
import osmosdr
import time
import numpy as np
import cPickle
import datetime
import os
from PyQt4 import QtGui


class BandwidthScanner(gr.top_block):

    def __init__(self,  samp_rate=2.4e6, gain=40.2, window_size=512, number_of_indices_to_remember=20):
        gr.top_block.__init__(self, "BandwithScanner")

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate
        self.gain = gain
        self.window_size = window_size
        self.raw_signal = []
        self.fft_mag = []
        self.signals_on_all_freq = []
        self.fft_mag_on_all_freq = []
        self.power_distribution = []
        self.strongest_signals_indices = []
        self.number_of_indices_to_remember = number_of_indices_to_remember
        self.sleep_time_for_tuning = 0.18

        ##################################################dow
        # Blocks
        ##################################################
        self.rtlsdr_source = osmosdr.source(args="numchan=" + str(1) + " " + '')
        self.rtlsdr_source.set_sample_rate(self.samp_rate)
        self.rtlsdr_source.set_center_freq(100e6, 0)
        self.rtlsdr_source.set_freq_corr(0, 0)
        self.rtlsdr_source.set_gain_mode(False, 0)
        self.rtlsdr_source.set_gain(gain)
        self.rtlsdr_source.set_antenna('', 0)

        self.block_stream_to_vector = blocks.stream_to_vector(gr.sizeof_gr_complex * 1, self.window_size)
        self.block_probe_raw_signal = blocks.probe_signal_vc(self.window_size)

        ##################################################
        # Connections
        ##################################################

        self.connect((self.rtlsdr_source, 0), (self.block_stream_to_vector, 0))
        self.connect((self.block_stream_to_vector, 0), (self.block_probe_raw_signal, 0))

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

    def scan_bandwidth(self, start_freq=88e6, stop_freq=120e6, measurements_place ='',
                       progress_bar=None):
        freq_vector = np.arange(start=start_freq, stop=stop_freq, step=self.samp_rate / 2)
        freq_index = 0
        self.start()
        time.sleep(1)  # time for hardware to init
        freq_count = len(freq_vector)
        while freq_index < freq_count:
            self.tune_to_freq(freq_vector[freq_index])
            time.sleep(self.sleep_time_for_tuning)
            signal_on_current_freq = self.block_probe_raw_signal.level()
            self.signals_on_all_freq.append(signal_on_current_freq)
            power = self.calculate_power(signal_on_current_freq)
            self.power_distribution.append(power)
            self.remember_strongest_signals_indices(power, freq_index)
            print 'Moc sygnału wokół częstotliwości %(freq)2f [MHz] = %(power)f' \
                  % {'freq': freq_vector[freq_index] / 1e6, 'power': power}
            if progress_bar is not None:
                assert (isinstance(progress_bar, QtGui.QProgressBar))
                progress_bar.setValue(round(float(freq_index+1)/freq_count * 100))
            freq_index += 1
        self.stop()
        print self.strongest_signals_indices
        out_filepath = self.save_measurements_dict(freq_vector, measurements_place)
        return out_filepath

    def tune_to_freq(self, freq):
        if self.rtlsdr_source.get_center_freq() == freq:
            pass
        else:
            self.rtlsdr_source.set_center_freq(freq, 0)

    def calculate_power(self, signal):
        sig_fft = np.fft.fft(signal)
        power = np.sum(np.power(np.abs(sig_fft), 2))/len(signal)
        return power

    def clear_signal_buffer(self):
        self.signal_buffer = []

    def remember_strongest_signals_indices(self, new_power, new_idx_power_distribution):
        number_of_remember_indices = len(self.strongest_signals_indices)
        list_full = number_of_remember_indices == self.number_of_indices_to_remember
        add_new_idx = not list_full
        if number_of_remember_indices > 0:
            for idx, idx_power_distribution in enumerate(self.strongest_signals_indices):
                if self.power_distribution[idx_power_distribution] < new_power:
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

    def save_measurements(self, freq_vector, measurements_place):
        current_time = datetime.datetime.now()
        current_time_str = current_time.strftime("%Y-%m-%d-%H:%M")
        dir_path = os.path.dirname(os.path.realpath(__file__))
        out_filename = current_time_str + '_' + measurements_place
        out_filename += '_' + str(int(round(freq_vector[0]/1e6))) + '-' +\
                        str(int(round(freq_vector[len(freq_vector)-1]/1e6))) + '.p'
        out_filepath = os.path.join(dir_path, Analyser.MEASUREMENTS_DIRECTORY_NAME, out_filename)
        out_file = open(out_filepath, "w")
        cPickle.dump(self.strongest_signals_indices, out_file)
        cPickle.dump(self.signals_on_all_freq, out_file)
        cPickle.dump(self.power_distribution, out_file)
        cPickle.dump(freq_vector, out_file)
        # configuration parameters
        cPickle.dump(self.samp_rate, out_file)
        cPickle.dump(self.gain, out_file)
        return out_filepath

    def save_measurements_dict(self, freq_vector, measurements_place):
        current_time = datetime.datetime.now()
        current_time_str = current_time.strftime("%Y-%m-%d-%H:%M")
        dir_path = os.path.dirname(os.path.realpath(__file__))
        out_filename = current_time_str + '_' + measurements_place
        out_filename += '_' + str(int(round(freq_vector[0] / 1e6))) + '-' + \
                        str(int(round(freq_vector[len(freq_vector) - 1] / 1e6))) + '.bmr'
        out_filepath = os.path.join(dir_path, Analyser.MEASUREMENTS_DIRECTORY_NAME, out_filename)
        out_file = open(out_filepath, "w")
        params_dict = {}
        params_dict['strongest_signals_indices'] = self.strongest_signals_indices
        params_dict['signals_on_all_freq'] = self.signals_on_all_freq
        params_dict['power_distribution'] = self.power_distribution
        params_dict['freq_vector'] = freq_vector
        params_dict['samp_rate'] = self.samp_rate
        params_dict['gain'] = self.gain
        params_dict['measurements_place'] = measurements_place
        cPickle.dump(params_dict, out_file)
        return out_filepath


if __name__ == "__main__":
    tb = BandwidthScanner(samp_rate=2e6, gain=40, window_size=512, number_of_indices_to_remember=20, use_filter=False)
    tb.scan_bandwidth(start_freq=80e6, stop_freq=1000e6, resolution=1e6, measurements_place='ogolna')
    a = Analyser(os.path.join(os.getcwd(), Analyser.MEASUREMENTS_DIRECTORY_NAME, tb.out_filename))
    a.print_loaded_file_info()
    a.spectral_analyse()

