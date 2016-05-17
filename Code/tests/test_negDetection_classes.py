#!/usr/bin/env python

import unittest
from negDetection_functions import getRules
from negDetection_classes import NegDetection


class TestNegDetection(unittest.TestCase):
    def setUp(self):
        self.reports = [
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
            }
        ]

        rules = getRules('negex_triggers.txt')
        self.detection_system = NegDetection(rules)

    def test_get_model(self):
        model_expected = {
            "pos_class": {
                "prev": {
                    "feature_1": {
                        "values": {
                            "COMMA": 2,
                            "AND": 1
                        },
                        "count": 3
                    },
                    "feature_2": {
                        "values": {
                            "COMMA_WORDS": 2,
                            "AND_WORDS": 1
                        },
                        "count": 3
                    },
                    "feature_3": {
                        "values": {
                            "COMMA_WORDS_COMMA": 1,
                            "AND_WORDS_COMMA": 1
                        },
                        "count": 2
                    },
                    "feature_4": {
                        "values": {
                            "PREN": 0,
                            "NO_PREN": 3
                        },
                        "count": 3
                    }
                },
                "next": {
                    "feature_1": {
                        "values": {
                            "POINT": 3
                        },
                        "count": 3
                    },
                    "feature_2": {
                        "values": {},
                        "count": 0
                    },
                    "feature_3": {
                        "values": {},
                        "count": 0
                    },
                    "feature_4": {
                        "values": {
                            "PREN": 0,
                            "NO_PREN": 3
                        },
                        "count": 3
                    }
                },
                "count": 3
            },
            "neg_class": {
                "prev": {
                    "feature_1": {
                        "values": {
                            "COMMA": 1
                        },
                        "count": 1
                    },
                    "feature_2": {
                        "values": {
                            "COMMA_WORDS": 1
                        },
                        "count": 1
                    },
                    "feature_3": {
                        "values": {
                            "COMMA_WORDS_PREN": 1
                        },
                        "count": 1
                    },
                    "feature_4": {
                        "values": {
                            "PREN": 1,
                            "NO_PREN": 0
                        },
                        "count": 1
                    }
                },
                "next": {
                    "feature_1": {
                        "values": {
                            "COMMA": 1
                        },
                        "count": 1
                    },
                    "feature_2": {
                        "values": {
                            "COMMA_OR": 1
                        },
                        "count": 1
                    },
                    "feature_3": {
                        "values": {
                            "COMMA_OR_WORDS": 1
                        },
                        "count": 1
                    },
                    "feature_4": {
                        "values": {
                            "PREN": 0,
                            "NO_PREN": 1
                        },
                        "count": 1
                    }
                },
                "count": 1
            },
            "total_docs": 4,
            "vocabulary": 13
        }

        listFeatures = self.detection_system.get_listfeatures_from_reports(self.reports)
        model = self.detection_system.get_model(listFeatures)
        self.assertEqual(model, model_expected)

    def test_get_listfeatures_from_reports(self):
        listFeatures_expected = [
            {
                "features": {
                    "prev": ["COMMA", "WORDS", "COMMA", "WORDS"],
                    "next": ["POINT"]
                },
                "class": "pos_class",
                "negex_class": "pos_class"
            },
            {
                "features": {
                    "prev": ["COMMA", "WORDS"],
                    "next": ["POINT"]
                },
                "class": "pos_class",
                "negex_class": "pos_class"
            },
            {
                "features": {
                    "prev": ["AND", "WORDS", "COMMA", "WORDS"],
                    "next": ["POINT"]
                },
                "class": "pos_class",
                "negex_class": "pos_class"
            },
            {
                "features": {
                    "prev": ["COMMA", "WORDS", "PREN"],
                    "next": ["COMMA", "OR", "WORDS", "POINT"]
                },
                "class": "neg_class",
                "negex_class": "neg_class"
            }
        ]

        listFeatures = self.detection_system.get_listfeatures_from_reports(self.reports)
        self.assertEqual(listFeatures, listFeatures_expected)

    def test_tagger(self):
        tokenize_list_expected = [
            ["WORDS", "COMMA", "WORDS", "COMMA", "PHRASE", "POINT"],
            ["WORDS", "COMMA", "PHRASE", "POINT"],
            ["WORDS", "COMMA", "WORDS", "AND", "PHRASE", "POINT"],
            ["PREN", "WORDS", "COMMA", "PHRASE", "COMMA", "OR", "WORDS", "POINT"]
        ]
        tokenize_list = [self.detection_system.tagger(report["word"], report["text"]) for report in self.reports]
        self.assertEqual(tokenize_list, tokenize_list_expected)

    def test_test(self):
        # TODO
        pass


def main():
    unittest.main()

if __name__ == '__main__':
    main()
