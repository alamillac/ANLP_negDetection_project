#!/usr/bin/env python

from libs.negex import sortRules, negTagger
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
                    "feature_1": {"values": {}, "count": 0},
                    "feature_2": {"values": {}, "count": 0},
                    "feature_3": {"values": {}, "count": 0},
                    "feature_4": {"values": {
                        "PREN": 0,
                        "NO_PREN": 0
                    }, "count": 0}
                },
                "next": {
                    "feature_1": {"values": {}, "count": 0},
                    "feature_2": {"values": {}, "count": 0},
                    "feature_3": {"values": {}, "count": 0},
                    "feature_4": {"values": {
                        "PREN": 0,
                        "NO_PREN": 0
                    }, "count": 0}
                },
                "count": 0
            }

        for data in listFeatures:
            class_name = data["class"]
            # update count class
            model[class_name]["count"] += 1

            for prev_or_next in ["prev", "next"]:
                for feature_name in ["feature_1", "feature_2", "feature_3", "feature_4"]:
                    # update features
                    feature_n = self.get_feature(data, prev_or_next, feature_name)
                    if feature_n:
                        if feature_n in model[class_name][prev_or_next][feature_name]["values"]:
                            model[class_name][prev_or_next][feature_name]["values"][feature_n] += 1
                        else:
                            model[class_name][prev_or_next][feature_name]["values"][feature_n] = 1
                        model[class_name][prev_or_next][feature_name]["count"] += 1

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
            #print "PHRASE: %s not found" % word
            pass

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

    def get_feature2(self, data, prev_or_next):
        features = data["features"][prev_or_next]
        feature2 = None
        if len(features) > 1:
            feature2 = "%s_%s" % (features[0], features[1])
        return feature2

    def get_feature3(self, data, prev_or_next):
        features = data["features"][prev_or_next]
        feature3 = None
        if len(features) > 2:
            feature3 = "%s_%s_%s" % (features[0], features[1], features[2])
        return feature3

    def get_feature4(self, data, prev_or_next):
        """PREN exist before POINT"""
        features = data["features"][prev_or_next]
        idx = 0
        exit = False
        feature4 = "NO_PREN"
        while not exit and idx < len(features):
            if features[idx] == "PREN":
                feature4 = "PREN"
                exit = True
            elif features[idx] == "POINT":
                exit = True
            idx += 1
        return feature4

    def get_feature(self, data, prev_or_next, feature_name):
        handler = {
            "feature_1": self.get_feature1,
            "feature_2": self.get_feature2,
            "feature_3": self.get_feature3,
            "feature_4": self.get_feature4
        }
        return handler[feature_name](data, prev_or_next)

    def get_vocabulary(self, feature_name):
        handler = {
            "feature_1": self._model["vocabulary"],
            "feature_2": self._model["vocabulary"] ** 2,
            "feature_3": self._model["vocabulary"] ** 3,
            "feature_4": 2
        }
        return handler[feature_name]

    def get_prob_feature(self, data, class_name, feature_name):
        f_p = self.get_feature(data, "prev", feature_name)
        f_n = self.get_feature(data, "next", feature_name)

        vocabulary = self.get_vocabulary(feature_name)
        f_p_total = self._model[class_name]["prev"][feature_name]["count"]
        f_n_total = self._model[class_name]["next"][feature_name]["count"]

        if f_p in self._model[class_name]["prev"][feature_name]["values"]:
            f_p_count = self._model[class_name]["prev"][feature_name]["values"][f_p]
        else:
            f_p_count = 0

        if f_n in self._model[class_name]["next"][feature_name]["values"]:
            f_n_count = self._model[class_name]["next"][feature_name]["values"][f_n]
        else:
            f_n_count = 0

        prob = math.log(float(f_p_count + 1) / (f_p_total + vocabulary)) + math.log(float(f_n_count + 1) / (f_n_total + vocabulary))
        return prob

    def get_log_probability(self, data, opt_features=["feature_1", "feature_2", "feature_3", "feature_4"]):
        prob = {}
        for class_name in self.__class_names.values():
            f_prob = 0
            for feature_name in opt_features:
                f_prob += self.get_prob_feature(data, class_name, feature_name)
            prob[class_name] = math.log(float(self._model[class_name]["count"]) / self._model["total_docs"]) + f_prob
        return prob

    def test(self, test_set, opt_features=["feature_1", "feature_2", "feature_3", "feature_4"]):
        listFeatures = self.get_listfeatures_from_reports(test_set)
        results = []
        for data in listFeatures:
            probs = self.get_log_probability(data, opt_features)
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
