import codecs

from collections import defaultdict

from levenshtein import levenshtein_distance


def p_wc(word, correct):
    dist = levenshtein_distance(word, correct)
    return 1 - float(dist) / len(word)


if __name__ == '__main__':
    print p_wc('kot', 'kot')
    print p_wc('kot', 'kod')
    print p_wc('abba', 'ala')
    print p_wc('telefon', 'telegraf')
    print p_wc('javascript', 'typescript')
    print p_wc('krowa', 'zdrowie')
