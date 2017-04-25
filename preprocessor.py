import re


def remove_special_chars(text):
    return re.compile(r'[\W\d]+', re.UNICODE).sub(' ', text)


def deduplicate_whitespace(text):
    return re.compile(r'[\s\n]+', re.UNICODE).sub(' ', text)


def clean_corpus(corpus):
    corpus = corpus.strip().lower()
    corpus = remove_special_chars(corpus)
    corpus = deduplicate_whitespace(corpus)
    return corpus.split()
