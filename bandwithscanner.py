#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Sampling
# Generated: Sat Jun 17 20:15:31 2017
##################################################

from gnuradio import blocks
from gnuradio import gr
import osmosdr
import threading
import time
import numpy as np
import matplotlib.pyplot as plt
import cPickle


class BandwithScanner(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "BandwithScanner")

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = 2e6
        self.probe_var = 0
        self.signal_buffer = []
        self.signals_on_all_freq = []
        self.power_distribution = []
        self.strongest_signals_indices = []
        self.number_of_indices_to_remember = 5
        self.btr_rate = 1.2

        ##################################################
        # Blocks
        ##################################################
        self.probe_signal = blocks.probe_signal_c()
        self.rtlsdr_source = osmosdr.source(args="numchan=" + str(1) + " " + '')
        self.rtlsdr_source.set_sample_rate(self.samp_rate)
        self.rtlsdr_source.set_center_freq(100e6, 0)
        self.rtlsdr_source.set_freq_corr(0, 0)
        self.rtlsdr_source.set_dc_offset_mode(0, 0)
        self.rtlsdr_source.set_iq_balance_mode(0, 0)
        self.rtlsdr_source.set_antenna('', 0)
        self.rtlsdr_source.set_bandwidth(1.5e6, 0)
        self.rtlsdr_source.set_gain_mode(False, 0)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, self.samp_rate, True)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_throttle_0, 0), (self.probe_signal, 0))
        self.connect((self.rtlsdr_source, 0), (self.blocks_throttle_0, 0))

        def _probe_sdr_output():
            while True:
                val = self.probe_signal.level()
                try:
                    self.set_probe_var(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / 2e6)
                self.signal_buffer.append(val)
        _probe_var_thread = threading.Thread(target=_probe_sdr_output)
        _probe_var_thread.daemon = True
        _probe_var_thread.start()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.rtlsdr_source.set_sample_rate(self.samp_rate)
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)

    def get_probe_var(self):
        return self.probe_var

    def set_probe_var(self, probe_var):
        self.probe_var = probe_var

    def fast_analize(self, start_freq=10e6, finish_freq=1000e6, resolution=10e6, probes_on_one_freq=1000):
        freq_vector = np.linspace(start_freq, finish_freq, round((finish_freq-start_freq)/resolution), 0)
        freq_index = 0
        self.rtlsdr_source.set_bandwidth(resolution*1.2, 0)
        self.start()
        while freq_index < len(freq_vector):
            if len(self.signal_buffer) >= probes_on_one_freq:
                self.signals_on_all_freq.append(self.signal_buffer)
                power = self.calculate_power(self.signal_buffer[0: probes_on_one_freq])
                self.power_distribution.append(power)
                self.remember_strongest_signals_indices(power, freq_index)
                print 'power of signal around freq %(freq)2f [MHz] = %(power)f' \
                      % {'freq': freq_vector[freq_index] / 1e6, 'power': power}
                self.clear_signal_buffer()
                self.tune_to_freq(freq_vector[freq_index])
                freq_index += 1
                time.sleep(1.0 / (self.samp_rate/probes_on_one_freq))
            time.sleep(1.0 / self.samp_rate)
        self.stop()
        plt.plot([x / 1e6 for x in freq_vector], self.power_distribution)
        plt.xlabel('Frequency [MHz]')
        plt.ylabel('Power')
        plt.show()
        self.save_measurements(freq_vector)

    def tune_to_freq(self, freq):
            self.rtlsdr_source.set_center_freq(freq, 0)

    def calculate_power(self, signal):
        power_sum = 0
        for probe in signal:
            power_sum += probe.real**2 + probe.imag**2
        power = power_sum / len(signal)
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

    def save_measurements(self, freq_vector):
        out_file = open("save.p", "w")
        cPickle.dump(self.strongest_signals_indices, out_file)
        cPickle.dump(self.signals_on_all_freq, out_file)
        cPickle.dump(self.power_distribution, out_file)
        cPickle.dump(freq_vector, out_file)
        # configuration parameters
        cPickle.dump(self.samp_rate, out_file)
        cPickle.dump(self.btr_rate, out_file)




if __name__ == "__main__":
    tb = BandwithScanner()
    tb.fast_analize()

