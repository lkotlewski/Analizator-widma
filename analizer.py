import cPickle


class Analizer():
    def __init__(self):
        pass

    def load_measurements(self, filename):
        file_to_load = open(filename, "r")
        strongest_signals_indices = cPickle.load(file_to_load)
        signals_on_all_freq = cPickle.load(file_to_load)
        power_distribution = cPickle.load(file_to_load)
        freq_vector = cPickle.load(file_to_load)
        # configuration parameters
        samp_rate = cPickle.load(file_to_load)
        btr_rate = cPickle.load(file_to_load)
        print strongest_signals_indices
        print power_distribution
        print btr_rate

if __name__ == "__main__":
    a = Analizer()
    a.load_measurements('save.p')

