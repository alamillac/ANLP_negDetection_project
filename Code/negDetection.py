#!/usr/bin/env python

from negDetection_classes import *
from negDetection_functions import *
from sklearn.cross_validation import train_test_split


def main():
    reports = getReports('Annotations-1-120.txt')
    rules = getRules('negex_triggers.txt')
    train_set, test_set = train_test_split(reports, train_size=0.9)
    detection_system = NegDetection(rules)
    detection_system.train(train_set)
    results = detection_system.test(test_set)
    corrects = 0
    neg_corrects = 0
    neg_incorrects = 0
    negex_corrects = 0
    negex_neg_corrects = 0
    negex_neg_incorrects = 0
    for result in results:
        if result["is_correct"]:
            corrects += 1

        if result["is_negex_correct"]:
            negex_corrects += 1

        if result["class"] == "neg_class":
            if result["is_correct"]:
                neg_corrects += 1
            else:
                neg_incorrects += 1

            if result["is_negex_correct"]:
                negex_neg_corrects += 1
            else:
                negex_neg_incorrects += 1


    import ipdb; ipdb.set_trace()  # BREAKPOINT


if __name__ == '__main__':
    main()

# idea: CONJUNTION(WITHOUT)  NEG_TERM(Not, no, ...) VP NP PUNTUATION_MARK(.) .. PHRASE_DISEASE
