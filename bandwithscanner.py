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


class BandwithScanner(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "BandwithScanner")

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = 2e6
        self.probe_var = 0
        self.signal_buffer = []
        self.freq_vector = np.linspace(30e6, 1000e6, 970)
        self.freq_index = 0
        self.power_distribution = []

        ##################################################
        # Blocks
        ##################################################
        self.probe_signal = blocks.probe_signal_c()
        self.rtlsdr_source = osmosdr.source(args="numchan=" + str(1) + " " + '')
        self.rtlsdr_source.set_sample_rate(self.samp_rate)
        self.rtlsdr_source.set_center_freq(self.freq_vector[0], 0)
        self.rtlsdr_source.set_freq_corr(0, 0)
        self.rtlsdr_source.set_dc_offset_mode(0, 0)
        self.rtlsdr_source.set_iq_balance_mode(0, 0)
        self.rtlsdr_source.set_gain_mode(False, 0)
        self.rtlsdr_source.set_gain(10, 0)
        self.rtlsdr_source.set_if_gain(20, 0)
        self.rtlsdr_source.set_bb_gain(20, 0)
        self.rtlsdr_source.set_antenna('', 0)
        self.rtlsdr_source.set_bandwidth(1.5e6, 0)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1,self.samp_rate, True)

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

    def fast_analize(self):
        self.start()
        while self.freq_index < len(self.freq_vector):
            if len(self.signal_buffer) > 1000:
                power = self.calculate_power(self.signal_buffer)
                self.power_distribution.append(power)
                print 'power of signal around freq %(freq)2f [MHz] = %(power)f' \
                      % {'freq': self.freq_vector[self.freq_index] / 1e6, 'power': power}
                self.clear_signal_buffer()
                self.tune_to_freq(self.freq_vector[self.freq_index])
                self.freq_index += 1
                time.sleep(1.0 / 2e3)
            time.sleep(1.0 / 2e6)
        plt.plot([x / 1e6 for x in self.freq_vector], self.power_distribution)
        plt.xlabel('Frequency [MHz]')
        plt.ylabel('Power')
        plt.show()
        self.stop()

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

