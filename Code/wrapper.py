from negex import *
import csv


def main():
    rfile = open(r'negex_triggers.txt')
    irules = sortRules(rfile.readlines())
    reports = csv.reader(open(r'Annotations-1-120.txt', 'rb'), delimiter='\t')
    reports.next()
    reportNum = 0
    correctNum = 0
    ofile = open(r'negex_output.txt', 'w')
    oEfile = open(r'negex_errors_output.csv', 'w')
    output = []
    eOutput = []
    fn = 0
    fp = 0
    outputfile = csv.writer(ofile, delimiter='\t')
    outputEfile = csv.writer(oEfile, delimiter=',')
    for report in reports:
        tagger = negTagger(sentence=report[2], phrases=[report[1]], rules=irules, negP=False)
        report.append(tagger.getNegTaggedSentence())
        report.append(tagger.getNegationFlag())
        report = report + tagger.getScopes()
        reportNum += 1
        if report[3].lower() == report[5]:
            correctNum += 1
        else:
            # reportErrors = [report[0], report[1], report[3], ]
            eOutput.append(report)
            if report[3].lower() == 'affirmed':
                fn += 1
            else:
                fp += 1
        output.append(report)
    outputfile.writerow(['Percentage correct:', float(correctNum) / float(reportNum)])
    # fp = 43, fn = 23
    # import ipdb; ipdb.set_trace()  # BREAKPOINT
    for row in output:
        if row:
            outputfile.writerow(row)
    ofile.close()

    for row in eOutput:
        if row:
            outputEfile.writerow(row)
    oEfile.close()

if __name__ == '__main__':
    main()

# idea: CONJUNTION(WITHOUT)  NEG_TERM(Not, no, ...) VP NP PUNTUATION_MARK(.) .. PHRASE_DISEASE
