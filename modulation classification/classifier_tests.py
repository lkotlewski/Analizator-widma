from modulation_classifier import ModulationClassifier
from dataset_helper import expected_decisions_dict
import cPickle

EXPECTED_DECISIONS_FILE = 'expected_decisions.dat'


def overall_accuracy(data_file_name):
    file_to_load = open(data_file_name, 'r')
    dataset = cPickle.load(file_to_load)
    assert isinstance(dataset, dict)
    keys = dataset.keys()
    filtered_keys = [key for key in keys if (key[1] == 16 or key[1] == 12 or key[1] == 8) and key[0] != 'AM-SSB' and key[0] != 'AM-DSB']
    mod_classif = ModulationClassifier()
    overall_score = 0
    overall_decision_nr = 0
    for key in filtered_keys:
        score = 0
        decision_nr = 0
        for signal in dataset[key]:
            result, _, _ = mod_classif.classify(signal)
            if result == expected_decisions_dict[key[0]]:
                score += 1
            decision_nr += 1
        print key[0] + ' score=' + str(score) + '/' + str(decision_nr)
        overall_score += score
        overall_decision_nr += decision_nr
    print 'overall acurracy =' + str(float(overall_score)/overall_decision_nr*100) + '%'


if __name__ == '__main__':
    #generate_expected_decisions_dict()
    overall_accuracy('/home/ubuntu/Desktop/Analizator widma/modulation datasets/dataset_with_self_gen_wbfm.dat')
