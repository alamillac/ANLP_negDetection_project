#!/usr/bin/env python

import csv


def getReports(reportFilename):
    reports = []
    with open(reportFilename, 'rb') as reportFile:
        rawReports = csv.reader(reportFile, delimiter='\t')
        rawReports.next()  # remove first line
        reports = getReportFromList(rawReports)
    return reports


def getRules(rulesFilename):
    rules = []
    with open(rulesFilename, 'rb') as rulesFile:
        rules = rulesFile.readlines()
    return rules


def getReportFromList(rawReports):
    """Get a list of reports [id, iliness, report_text, class] and convert it to a list of reportObjects
    {
        id: id,
        word: iliness,
        text: report_text,
        class: (True, False)
    }"""
    reports = [{"id": report[0], "word": report[1], "text": report[2], "class": report[3].lower() == "affirmed"} for report in rawReports]
    return reports


def showResults(results, name="Test"):
    """Print the results of the test set"""
    total = len(results)
    corrects = 0
    neg_corrects = 0
    pos_corrects = 0
    neg_incorrects = 0
    pos_incorrects = 0
    negex_corrects = 0
    negex_neg_corrects = 0
    negex_pos_corrects = 0
    negex_neg_incorrects = 0
    negex_pos_incorrects = 0
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
        else:
            if result["is_correct"]:
                pos_corrects += 1
            else:
                pos_incorrects += 1

            if result["is_negex_correct"]:
                negex_pos_corrects += 1
            else:
                negex_pos_incorrects += 1

    print
    print "###################"
    print name
    print "Total examples: %d" % total
    print "Results: \tCorrect: %d\tNegative Correct: %d, Negative Incorrect: %d\tPositive Correct: %d, Positive Incorrect: %d" % (corrects, neg_corrects, neg_incorrects, pos_corrects, pos_incorrects)
    print "NegEx results: \tCorrect: %d\tNegative Correct: %d, Negative Incorrect: %d\tPositive Correct: %d, Positive Incorrect: %d" % (negex_corrects, negex_neg_corrects, negex_neg_incorrects, negex_pos_corrects, negex_pos_incorrects)
