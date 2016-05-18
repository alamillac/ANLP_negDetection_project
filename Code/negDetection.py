#!/usr/bin/env python

from negDetection_classes import *
from negDetection_functions import *
from sklearn.cross_validation import train_test_split


def main():
    reports = getReports('Annotations-1-120.txt')
    rules = getRules('negex_triggers.txt')
    train_set, test_set = train_test_split(reports, train_size=0.9, random_state=7)
    detection_system = NegDetection(rules)
    print "Training system"
    detection_system.train(train_set)

    # Show train results
    print "Testing system"
    train_results = detection_system.test(train_set)
    showResults(train_results, "Train results")

    # Show test results
    opt_features = [
        ("Feature 1", ["feature_1"]),
        ("Features 1,2", ["feature_1", "feature_2"]),
        ("Features 1,2,3", ["feature_1", "feature_2", "feature_3"]),
        ("Features 1,2,3,4", ["feature_1", "feature_2", "feature_3", "feature_4"]),
        ("Feature 4", ["feature_4"])
    ]

    for title, feature_names in opt_features:
        results = detection_system.test(test_set, feature_names)
        showResults(results, title)


if __name__ == '__main__':
    main()

# idea: CONJUNTION(WITHOUT)  NEG_TERM(Not, no, ...) VP NP PUNTUATION_MARK(.) .. PHRASE_DISEASE
