#!/usr/bin/env python

import unittest
from negDetection_functions import getReportFromList


class TestGetReports(unittest.TestCase):
    def test_getReportFromList(self):
        rawReports = [
            ['5', 'right pleural effusion', 'S_O_H  Counters Report Type Record Type Subgroup Classifier  161,JAlB6a0EJoOb RAD RAD   E_O_H  [Report de-identified (Safe-harbor compliant) by De-ID v.6.14.02]      EXAMINATION PERFORMED:  US GUIDED THORACENTESIS PUNCTURE RIGHT   **DATE[Nov 07 07]     1251 HOURS    CLINICAL HISTORY:     Right thoracentesis, RIGHT PLEURAL EFFUSION.', 'Affirmed'],
            ['49', 'bilateral high-grade carotid stenosis', 'A CT angiogram   showed left MCA CVA, BILATERAL HIGH-GRADE CAROTID STENOSIS.', 'Affirmed'],
            ['73', 'vomiting', 'The patient was admitted   on **DATE[Sep 25 2007], complaining of nausea and VOMITING.', 'Affirmed'],
            ['81', 'gallops', 'No murmurs, GALLOPS, or rubs.', 'Negated'],
            ['27', 'atrial   flutter', 'A **AGE[90+]-year-old female presents to the Emergency Department with ATRIAL   FLUTTER.', 'Affirmed'],
            ['100', 'cirrhosis', 'The indication for this procedure is CIRRHOSIS  and staging of portal hypertension.', 'Affirmed'],
            ['69', 'focal neurologic deficit', 'She   does not have any FOCAL NEUROLOGIC DEFICIT.', 'Negated'],
            ['27', 'Abdomen is soft, nontender, and mildly distended', 'ABDOMEN: ABDOMEN IS SOFT, NONTENDER, AND MILDLY DISTENDED.', 'Affirmed'],
            ['37', 'more pleasant ', 'She was getting MORE PLEASANT after pain was more   controlled and moving around with wheelchair accompanied by her husband.', 'Affirmed']
        ]
        reports_expected = [
            {
                "id": '5',
                "word": 'right pleural effusion',
                "text": 'S_O_H  Counters Report Type Record Type Subgroup Classifier  161,JAlB6a0EJoOb RAD RAD   E_O_H  [Report de-identified (Safe-harbor compliant) by De-ID v.6.14.02]      EXAMINATION PERFORMED:  US GUIDED THORACENTESIS PUNCTURE RIGHT   **DATE[Nov 07 07]     1251 HOURS    CLINICAL HISTORY:     Right thoracentesis, RIGHT PLEURAL EFFUSION.',
                "class": True
            },
            {
                "id": '49',
                "word": 'bilateral high-grade carotid stenosis',
                "text": 'A CT angiogram   showed left MCA CVA, BILATERAL HIGH-GRADE CAROTID STENOSIS.',
                "class": True
            },
            {
                "id": '73',
                "word": 'vomiting',
                "text": 'The patient was admitted   on **DATE[Sep 25 2007], complaining of nausea and VOMITING.',
                "class": True
            },
            {
                "id": '81',
                "word": 'gallops',
                "text": 'No murmurs, GALLOPS, or rubs.',
                "class": False
            },
            {
                "id": '27',
                "word": 'atrial   flutter',
                "text": 'A **AGE[90+]-year-old female presents to the Emergency Department with ATRIAL   FLUTTER.',
                "class": True
            },
            {
                "id": '100',
                "word": 'cirrhosis',
                "text": 'The indication for this procedure is CIRRHOSIS  and staging of portal hypertension.',
                "class": True
            },
            {
                "id": '69',
                "word": 'focal neurologic deficit',
                "text": 'She   does not have any FOCAL NEUROLOGIC DEFICIT.',
                "class": False
            },
            {
                "id": '27',
                "word": 'Abdomen is soft, nontender, and mildly distended',
                "text": 'ABDOMEN: ABDOMEN IS SOFT, NONTENDER, AND MILDLY DISTENDED.',
                "class": True
            },
            {
                "id": '37',
                "word": 'more pleasant ',
                "text": 'She was getting MORE PLEASANT after pain was more   controlled and moving around with wheelchair accompanied by her husband.',
                "class": True
            }
        ]

        reports = getReportFromList(rawReports)
        self.assertEqual(reports, reports_expected)


def main():
    unittest.main()

if __name__ == '__main__':
    main()
