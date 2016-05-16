#!/usr/bin/env python

from negex import sortRules, negTagger
from nltk import word_tokenize
import math
import re


class NegDetection(object):
    def __init__(self, rules):
        self.__rules = sortRules(rules)
        self.__tagged_options = set(['CONJ', 'PSEU', 'POST', 'PREP', 'POSP', 'PREN', 'PHRASE', 'NEGATED'])
        self.__conversion_table = {
            "NEGATED": "PHRASE",
            ".": "POINT",
            ",": "COMMA",
            "OR": "OR",
            "AND": "AND"
        }
        self.__WORDS = "WORDS"
        self.__class_names = {
            True: "pos_class",
            False: "neg_class"
        }
        self._model = None

    def train(self, train_set):
        listFeatures = self.get_listfeatures_from_reports(train_set)
        self._model = self.get_model(listFeatures)

    def get_listfeatures_from_reports(self, reports):
        listFeatures = []
        for report in reports:
            features = self.get_features(report["word"], report["text"])
            if features:
                # Get the class from negEx to evaluate the results
                negexTagger = negTagger(sentence=report["text"], phrases=[report["word"]], rules=self.__rules, negP=False)
                negex_class_result = negexTagger.getNegationFlag().lower() == "affirmed"

                # add to list
                listFeatures.append({
                    "features": features,
                    "class": self.__class_names[report["class"]],
                    "negex_class": self.__class_names[negex_class_result]
                })
        return listFeatures

    def get_model(self, listFeatures):
        model = {}

        model["vocabulary"] = len(set(list(self.__tagged_options) + self.__conversion_table.values() + [self.__WORDS]))
        model["total_docs"] = len(listFeatures)

        for class_name in self.__class_names.values():
            model[class_name] = {
                "prev": {
                    "feature_1": {"values": {}, "count": 0}
                },
                "next": {
                    "feature_1": {"values": {}, "count": 0}
                },
                "count": 0
            }

        for data in listFeatures:
            class_name = data["class"]
            # update count class
            model[class_name]["count"] += 1

            # update feature1
            for prev_or_next in ["prev", "next"]:
                feature1 = self.get_feature1(data, prev_or_next)
                if feature1:
                    if feature1 in model[class_name][prev_or_next]["feature_1"]["values"]:
                        model[class_name][prev_or_next]["feature_1"]["values"][feature1] += 1
                    else:
                        model[class_name][prev_or_next]["feature_1"]["values"][feature1] = 1
                    model[class_name][prev_or_next]["feature_1"]["count"] += 1

        return model

    def get_features(self, word, text):
        """Get the word and text from a report and return the features of this report
            Ex:
        """
        features = None
        tagged_text = self.tagger(word, text)
        try:
            idx = tagged_text.index("PHRASE")
            features = {}
            features["prev"] = tagged_text[idx - 1::-1]
            features["next"] = tagged_text[idx + 1:]
        except:
            print "PHRASE: %s not found" % word

        return features

    def tagger(self, s_word, _text):
        """Tokenize a text
        Ex:
            word = "bilateral high-grade carotid stenosis"
            text = "A CT angiogram   showed left MCA CVA, BILATERAL HIGH-GRADE CAROTID STENOSIS."
            tokenized_word = ["WORDS", "COMMA", "PHRASE", "POINT"]
        """

        # Sometimes the negex don't find the s_word in sentece TODO: Borrar la linea si afecta
        text = re.sub(r'(?i)%s' % s_word.strip(), 'FRASE', _text)

        # Get the taged text from negEx
        negexTagger = negTagger(sentence=text, phrases=["FRASE"], rules=self.__rules, negP=False)
        tagged_text = negexTagger.getNegTaggedSentence()

        # Replace the tagged words
        for tagged_option in self.__tagged_options:
            re_tagged_option = r'\[%s\].+?\[%s\]' % (tagged_option, tagged_option)
            tagged_text = re.sub(re_tagged_option, ' %s ' % tagged_option, tagged_text)

        pre_tokenized_word = [word_tok.upper() for word_tok in word_tokenize(tagged_text)]
        tokenized_word = []
        previous_word = ''
        for word in pre_tokenized_word:
            end_word = None
            if word in self.__conversion_table:
                end_word = self.__conversion_table[word]
            elif word in self.__tagged_options:
                end_word = word
            elif previous_word != self.__WORDS:
                end_word = self.__WORDS
            if end_word:
                previous_word = end_word
                tokenized_word.append(end_word)

        return tokenized_word

    def get_feature1(self, data, prev_or_next):
        features = data["features"][prev_or_next]
        feature1 = None
        if features:
            feature1 = features[0]
        return feature1

    def get_prob_feature1(self, data, class_name):
        f1_p = self.get_feature1(data, "prev")
        f1_n = self.get_feature1(data, "next")

        vocabulary = self._model["vocabulary"]
        f1_p_total = self._model[class_name]["prev"]["feature_1"]["count"]
        f1_n_total = self._model[class_name]["next"]["feature_1"]["count"]

        if f1_p in self._model[class_name]["prev"]["feature_1"]["values"]:
            f1_p_count = self._model[class_name]["prev"]["feature_1"]["values"][f1_p]
        else:
            f1_p_count = 0

        if f1_n in self._model[class_name]["next"]["feature_1"]["values"]:
            f1_n_count = self._model[class_name]["next"]["feature_1"]["values"][f1_n]
        else:
            f1_n_count = 0

        prob = math.log(float(f1_p_count + 1) / (f1_p_total + vocabulary)) + math.log(float(f1_n_count + 1) / (f1_n_total + vocabulary))
        return prob

    def get_probability(self, data):
        prob = {}
        for class_name in self.__class_names.values():
            f1_prob = self.get_prob_feature1(data, class_name)
            prob[class_name] = math.log(float(self._model[class_name]["count"]) / self._model["total_docs"]) + f1_prob
        return prob

    def test(self, test_set):
        listFeatures = self.get_listfeatures_from_reports(test_set)
        results = []
        for data in listFeatures:
            probs = self.get_probability(data)
            true_class = data["class"]
            negex_class = data["negex_class"]

            if probs["neg_class"] > probs["pos_class"]:
                test_class = "neg_class"
            else:
                test_class = "pos_class"

            if test_class == true_class:
                is_correct = True
            else:
                is_correct = False

            if negex_class == true_class:
                is_negex_correct = True
            else:
                is_negex_correct = False

            results.append({"probs": probs, "negex_class": negex_class, "test_class": test_class, "is_correct": is_correct, "is_negex_correct": is_negex_correct, "class": true_class})
        return results
