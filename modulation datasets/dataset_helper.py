import cPickle
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats.mstats
import os
import modulation_classifier
from modulation_classifier import SigParamsCalculator, ModTypes


SEP_MOD_DIR_NAME = 'separated_modulation_files'
MOD_PAR_TAB_DIR_NAME = 'mod_params_tables'
MOD_MI_VEC_DIR_NAME = 'mod_mi_vectors'
CHARTS_DIR_NAME = 'charts'
MEANS_DIR_NAME = 'means'
STD_DIR_NAME = 'std'

expected_decisions_dict = {
                           'CPFSK': ModTypes.CPFSK.value,'GFSK': ModTypes.GFSK.value, 'PAM4': ModTypes.M_PAM.value,
                           'BPSK': ModTypes.BPSK.value, 'WBFM': ModTypes.WBFM.value, 'QAM16': ModTypes.M_QAM.value,
                           'QAM64': ModTypes.M_QAM.value, 'QPSK': ModTypes.M_PSK.value, '8PSK': ModTypes.M_PSK.value}


def make_separated_mod_stats(data_file_name):
    file_to_load = open(data_file_name, 'r')
    subset = cPickle.load(file_to_load)
    make_subset_stats(subset, data_file_name)


def make_modulations_stats(data_file_name, params_table_file_name, mi_vector_file_name, std_vector_file_name):
    file_to_load = open(data_file_name, 'r')
    params_table_file = open(params_table_file_name, 'w')
    mi_vector_file = open(mi_vector_file_name, 'w')
    std_vector_file = open(std_vector_file_name, 'w')
    dataset = cPickle.load(file_to_load)
    params_table_dict = {}
    mi_vector_dict = {}
    std_vector_dict = {}
    assert isinstance(dataset, dict)
    keys = dataset.keys()
    filtered_keys = [key for key in keys if key[1] == 16 or key[1] == 12 or key[1] == 8]
    for key in filtered_keys:
        params_table, mi_vector, std_vector = make_subset_stats(dataset[key], key[0])
        params_table_dict[key] = params_table
        mi_vector_dict[key] = mi_vector
        std_vector_dict[key] = std_vector
    cPickle.dump(params_table_dict, params_table_file)
    cPickle.dump(mi_vector_dict, mi_vector_file)
    cPickle.dump(std_vector_dict, std_vector_file)

def make_mapped_stats(params_table_file_name, mapped_params_table_file_name,
                      mapped_mi_vector_file_name, mapped_std_vector_file_name):
    params_table_file = open(params_table_file_name, 'r')
    mapped_params_table_file = open(mapped_params_table_file_name, 'w')
    mapped_mi_vector_file = open(mapped_mi_vector_file_name, 'w')
    mapped_std_vector_file = open(mapped_std_vector_file_name, 'w')
    params_table_dict = cPickle.load(params_table_file)
    mapped_params_table_dict = {}
    mapped_mi_vector_dict = {}
    mapped_std_vector_dict = {}
    dataset_keys = params_table_dict.keys()
    recognized_mods = [mod_type for mod_type in ModTypes]
    for recognized_mod in recognized_mods:
        mapped_params_table = np.array([]).reshape(0, 8)
        recognized_mod_str = recognized_mod.get_string()
        mapped_mods_keys = [dataset_key for dataset_key in dataset_keys if expected_decisions_dict.get(dataset_key[0]) ==
                            recognized_mod.value]
        list_of_params_tables = [params_table_dict[dataset_key] for dataset_key in mapped_mods_keys]
        for params_table in list_of_params_tables:
            mapped_params_table = np.concatenate([mapped_params_table, params_table])
        mapped_mi_vector, mapped_std_vector = calculate_columns_mean_and_std(mapped_params_table)
        mapped_params_table_dict[recognized_mod_str] = mapped_params_table
        mapped_mi_vector_dict[recognized_mod_str] = mapped_mi_vector
        mapped_std_vector_dict[recognized_mod_str] = mapped_std_vector
    cPickle.dump(mapped_params_table_dict, mapped_params_table_file)
    cPickle.dump(mapped_mi_vector_dict, mapped_mi_vector_file)
    cPickle.dump(mapped_std_vector_dict, mapped_std_vector_file)


def calculate_columns_mean_and_std(array):
    columns_nr = array.shape[1]
    mi_vector = np.empty(columns_nr)
    std_vector = np.empty(columns_nr)
    for idx, column in enumerate(array.T):
        mi_vector[idx] = np.mean(column)
        std_vector[idx] = np.mean(column)
    return mi_vector, std_vector


def make_subset_stats(subset, mod_name=None):
    sig_realiz_nr = np.shape(subset)[0]
    params_nr = 8
    params_table = np.empty([sig_realiz_nr, params_nr])
    mi_vector = np.empty(params_nr)
    std_vector = np.empty(params_nr)
    for idx, mod_signal in enumerate(subset):
        sig_par_calc = SigParamsCalculator(mod_signal)
        all_params = sig_par_calc.calculate_all_params()
        params_table[idx] = all_params
    for param_idx in range(params_nr):
        mi_vector[param_idx] = np.mean(params_table[:, param_idx])
        std_vector[param_idx] = np.std(params_table[:, param_idx])
    if mod_name is not None:
        print '\n' + mod_name + ':'
        column_names = modulation_classifier.get_columns_names()
        for param_idx in range(params_nr):
            print 'mean of ' + column_names[param_idx] + '=' + str(mi_vector[param_idx])
    return params_table, mi_vector, std_vector


def import_dataset_a(data_file_name):
    file_to_load = open(data_file_name, 'r')
    dataset = cPickle.load(file_to_load)
    assert isinstance(dataset, dict)
    print dataset.keys()
    return dataset


def extract_keys_to_another_file(data_in_file_name, out_file_name):
    file_to_load = open(data_in_file_name, 'r')
    out_file = open(out_file_name, 'w')
    dataset = cPickle.load(file_to_load)
    assert isinstance(dataset, dict)
    keys = dataset.keys()
    cPickle.dump(keys, out_file)


def print_first_object(file_name):
    file_to_load = open(file_name, 'r')
    first_object = cPickle.load(file_to_load)
    print first_object


def extract_signals_to_separate_files(data_file_name):
    file_to_load = open(data_file_name, 'r')
    dataset = cPickle.load(file_to_load)
    assert isinstance(dataset, dict)
    keys = dataset.keys()
    sig_num = len(keys)
    for idx, key in enumerate(keys):
        out_file_name = key[0] + '_' + str(key[1]) + '.dat'
        out_file_path = os.path.join(SEP_MOD_DIR_NAME, out_file_name)
        out_file = open(out_file_path, 'w')
        complex_subset = subset_to_complex_format(dataset.get(key))
        cPickle.dump(complex_subset, out_file)
        print 'progress:' + str(idx+1) + '/' + str(sig_num)


def file_to_complex_format(data_in_file_name, data_out_file_name):
    file_to_load = open(data_in_file_name, 'r')
    out_file = open(data_out_file_name, 'w')
    dataset = cPickle.load(file_to_load)
    complex_dataset = {}
    assert isinstance(dataset, dict)
    keys = dataset.keys()
    sig_num = len(keys)
    for idx, key in enumerate(keys):
        complex_subset = subset_to_complex_format(dataset.get(key))
        complex_dataset[key] = complex_subset
        print 'progress:' + str(idx + 1) + '/' + str(sig_num)
    cPickle.dump(complex_dataset, out_file)


def subset_to_complex_format(subset):
    sig_realiz_nr = np.shape(subset)[0]
    realization_len = np.shape(subset)[2]
    new_subset = np.empty([sig_realiz_nr, realization_len], 'D')
    for idx in range(sig_realiz_nr):
        new_subset[idx] = complex_from_two_real(subset[idx][0], subset[idx][1])
    return new_subset


def complex_from_two_real(x, y):
    z = x + y*1j
    return z


def generate_bar_charts(mi_vectors_file_name, std_vectors_file_name):
    mi_vectors_file = open(mi_vectors_file_name, 'r')
    std_vectors_file = open(std_vectors_file_name, 'r')
    mi_vectors_dict = cPickle.load(mi_vectors_file)
    std_vectors_dict = cPickle.load(std_vectors_file)
    assert isinstance(mi_vectors_dict, dict)
    keys = mi_vectors_dict.keys()
    mod_nr = len(keys)
    par_nr = 8
    par_names = modulation_classifier.get_columns_names()
    mod_names = [key[0] for key in keys]
    mi_table = np.empty([mod_nr, par_nr])
    std_table = np.empty([mod_nr, par_nr])

    for idx, key in enumerate(keys):
        mi_table[idx] = mi_vectors_dict[key]
        std_table[idx] = std_vectors_dict[key]

    for par_idx in range(par_nr):
        par_name = par_names[par_idx]
        mod_pos = np.arange(mod_nr)

        plt.figure(figsize=(16, 8))
        plt.bar(mod_pos, mi_table[:, par_idx], align='center', alpha=0.5)
        plt.xticks(mod_pos, mod_names)
        plt.ylabel('Wartosc srednia parametru')
        plt.title(par_name)
        plt.savefig(os.path.join(CHARTS_DIR_NAME, MEANS_DIR_NAME, par_name))

        plt.figure(figsize=(16, 8))
        plt.bar(mod_pos, std_table[:, par_idx], align='center', alpha=0.5)
        plt.xticks(mod_pos, mod_names)
        plt.ylabel('Odchylenie standardowe parametru')
        plt.title(par_name)
        plt.savefig(os.path.join(CHARTS_DIR_NAME, STD_DIR_NAME,  par_name))

def prepare_set_with_self_gen_wbfm(data_in_file_name, data_out_file_name):
    file_to_load = open(data_in_file_name, 'r')
    dataset = cPickle.load(file_to_load)
    file_wbfm_8 = open('/home/ubuntu/Desktop/Analizator widma/modulation datasets/self_generated/WBFM_8_44a.dat',
                        'r')
    file_wbfm_12 = open('/home/ubuntu/Desktop/Analizator widma/modulation datasets/self_generated/WBFM_12_44a.dat',
                        'r')
    file_wbfm_14 = open('/home/ubuntu/Desktop/Analizator widma/modulation datasets/self_generated/WBFM_14_44a.dat',
                        'r')
    file_wbfm_16 = open('/home/ubuntu/Desktop/Analizator widma/modulation datasets/self_generated/WBFM_16_44a.dat',
                        'r')
    file_wbfm_18 = open('/home/ubuntu/Desktop/Analizator widma/modulation datasets/self_generated/WBFM_18_44a.dat',
                        'r')
    subset_wbfm_8 = cPickle.load(file_wbfm_8)
    subset_wbfm_12 = cPickle.load(file_wbfm_12)
    subset_wbfm_14 = cPickle.load(file_wbfm_14)
    subset_wbfm_16 = cPickle.load(file_wbfm_16)
    subset_wbfm_18 = cPickle.load(file_wbfm_18)

    dataset[('WBFM', 8)] = subset_wbfm_8
    dataset[('WBFM', 12)] = subset_wbfm_12
    dataset[('WBFM', 14)] = subset_wbfm_14
    dataset[('WBFM', 16)] = subset_wbfm_16
    dataset[('WBFM', 18)] = subset_wbfm_18

    file_to_write = open(data_out_file_name, 'w')
    cPickle.dump(dataset, file_to_write)

def prepare_feature_vectors_with_labels():
    params_tables_file = open('mod_params_tables.dat', 'r')
    params_dict = cPickle.load(params_tables_file)
    whole_params_table = np.array([]).reshape(0, 8)
    all_labels = np.array([]).reshape(0, 1)
    assert isinstance(params_dict, dict)
    keys = params_dict.keys()
    for key in keys:
        if key[0] != 'AM-DSB' and key[0] != 'AM-SSB':
            whole_params_table = np.concatenate((whole_params_table, params_dict[key]))
            labels = np.zeros([len(params_dict[key]), 1])
            labels.fill(expected_decisions_dict[key[0]])
            all_labels = np.concatenate((all_labels, labels))
    training_data_file = open('training_data.dat', 'w')
    cPickle.dump(whole_params_table, training_data_file)
    cPickle.dump(all_labels, training_data_file)



def test_params_dist_normality(params_tables_filename):
    params_tables_file = open(params_tables_filename, 'r')
    params_tables_dict = cPickle.load(params_tables_file)
    column_names = modulation_classifier.get_columns_names()
    assert isinstance(params_tables_dict, dict)
    for key in params_tables_dict.keys():
        print key[0]
        mod_param_table = params_tables_dict[key]
        for idx, column_name in enumerate(column_names):
            param_vector = mod_param_table[:, idx]
            k2, p_value = scipy.stats.mstats.normaltest(param_vector)
            plt.hist(param_vector, normed=False, bins=25)
            plt.title(key[0] + ':' + column_name)
            plt.show()
            print column_name + ' probability of norm distribution :' + str(p_value)
        print '\n'


if __name__ == '__main__':
    #file_to_complex_format('RML2016.10a_dict.dat', 'RML2016.10a_dict_complex.dat')
    #print_first_object('RML2016.10a_dict_complex.dat')
    #extract_signals_to_separate_files('RML2016.10a_dict.dat')
    #print_first_object('separated_modulation_files/8PSK_0.dat')
    # make_modulations_stats('dataset_with_self_gen_wbfm.dat', 'mod_params_tables.dat', 'mod_mi_vectors.dat', 'mod_std_vectors.dat')
    # generate_bar_charts('mod_mi_vectors.dat', 'mod_std_vectors.dat')

    # prepare_set_with_self_gen_wbfm('RML2016.10a_dict_complex.dat', 'dataset_with_self_gen_wbfm.dat')
    # make_separated_mod_stats('self_generated/WBFM_16_44a.dat')
    # make_separated_mod_stats('self_generated/WBFM_16_192b.dat')
    # make_separated_mod_stats('self_generated/WBFM_14_192c.dat')
    #
    # make_separated_mod_stats('self_generated/WBFM_18_44a.dat')
    # make_separated_mod_stats('self_generated/WBFM_16_44a.dat')
    # make_separated_mod_stats('self_generated/WBFM_12_44a.dat')
    # make_separated_mod_stats('self_generated/WBFM_8_44a.dat')
    # make_separated_mod_stats('self_generated/WBFM_18_192b.dat')
    # make_separated_mod_stats('self_generated/WBFM_18_192c.dat')
    #
    # print_first_object('keys.dat')

    #test_params_dist_normality('mod_params_tables.dat')

    prepare_feature_vectors_with_labels()

    # make_mapped_stats('mod_params_tables.dat',  'mapped_mod_params_tables.dat', 'mapped_mod_mi_vectors.dat',
    #                    'mapped_mod_std_vectors.dat' )

    #print_first_object('mapped_mod_mi_vectors.dat')


