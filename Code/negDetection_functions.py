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
