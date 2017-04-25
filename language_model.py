# coding=utf-8
import codecs
import json
from collections import defaultdict, Counter

import sys

from levenshtein import levenshtein_distance, common_errors
from preprocessor import clean_corpus


class LanguageModel(object):
    def __init__(self, err_filename, words_filename, corpus_filenames):
        self.alpha = 1.0
        self.N = 0
        self.M = 0
        self.words = []
        self.p_c = defaultdict(self.smooth)
        self.p_wc = defaultdict(lambda: 0)
        self.load_data(err_filename, words_filename, corpus_filenames)

    def load_data(self, err_filename, words_filename, corpus_filenames):
        self.load_err_statistics(err_filename)
        self.load_words(words_filename)
        self.load_ranking(corpus_filenames)

    def load_err_statistics(self, err_filename):
        with codecs.open(err_filename, encoding='utf-8') as errors_file:
            errors = [line.strip().split(';') for line in errors_file.readlines()]

        for w, c in errors:
            dist = levenshtein_distance(w, c)
            self.p_wc[dist * 4] += 1

        for dist, p in self.p_wc.items():
            self.p_wc[dist * 4] = float(p) / len(errors)

        self.p_wc[0] = 1

    def load_words(self, words_filename):
        with codecs.open(words_filename, encoding='utf-8') as words_file:
            self.words = set(words_file.read().split())

    def load_ranking(self, corpus_filenames):
        words = []
        for filename in corpus_filenames:
            with codecs.open(filename, encoding='utf-8') as corpus_file:
                words += clean_corpus(corpus_file.read())

        ranking = Counter(words)

        for word, freq in ranking.items():
            self.p_c[word] = float(freq) / len(words)

        self.N = sum(ranking.values())
        self.M = len(ranking.items())

    def calc_p_wc(self, dist):
        dist *= 4
        if self.p_wc[dist] != 0:
            return self.p_wc[dist]
        return (self.p_wc[dist - 1] + self.p_wc[dist + 1]) / 2

    def smooth(self):
        return self.alpha / (self.N + self.alpha * self.M)

    def edits(self, word):
        alphabet = u'aąbcćdeęfghijklłmnoópqrsśtuvwxyzżź'
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes = [a + b[1:] for a, b in splits if b]
        transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b) > 1]
        replaces = [a + c + b[1:] for a, b in splits for c in alphabet if b]
        inserts = [a + c + b for a, b in splits for c in alphabet]
        candidates = deletes + transposes + replaces + inserts
        return set(candidates)

    def correct_error(self, w):
        edits1 = self.edits(w)
        if len(w) > 4:
            edits2 = set([e2 for e1 in edits1 for e2 in self.edits(e1)])
            candidates = filter(lambda x: x in self.words, edits1 | edits2)
        else:
            candidates = filter(lambda x: x in self.words, edits1)

        corrections = []

        for candidate in candidates:
            dist = levenshtein_distance(w, candidate)
            prob = self.calc_p_wc(dist) * self.p_c[candidate]
            corrections.append((candidate, prob))

        return sorted(corrections, key=lambda x: x[1], reverse=True)


ERR_FILENAME = 'data/bledy.txt'
WORDS_FILENAME = 'data/formy.txt'
SAMPLES_FILENAME = 'samples.json'

if __name__ == '__main__':
    with open(SAMPLES_FILENAME) as samples_file:
        samples = json.load(samples_file)

    model = LanguageModel(ERR_FILENAME, WORDS_FILENAME, samples)

    while True:
        input_text = raw_input('> ').decode(sys.stdin.encoding).strip()
        if input_text == '':
            continue
        corrections = model.correct_error(input_text)
        for c, prob in corrections[:3]:
            print c.encode('utf-8')
