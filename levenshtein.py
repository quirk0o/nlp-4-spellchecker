# coding=utf-8

polonica_errors = [
    (u'a', u'ą'),
    (u'e', u'ę'),
    (u'c', u'ć'),
    (u'l', u'ł'),
    (u'n', u'ń'),
    (u'o', u'ó'),
    (u's', u'ś'),
    (u'z', u'ż'),
    (u'z', u'ż')
]

ort_errors = [
    (u'ą', u'om'),
    (u'om', u'ą'),
    (u'ą', u'on'),
    (u'on', u'ą'),
    (u'ą', u'ę'),
    (u'au', u'ał'),
    (u'uła', u'ua'),
    (u'ę', u'en'),
    (u'en', u'ę'),
    (u'ę', u'em'),
    (u'em', u'ę'),
    (u'w', u'f'),
    (u'f', u'w'),
    (u'ó', u'u'),
    (u'u', u'ó'),
    (u'ch', u'h'),
    (u'h', u'ch'),
    (u'rz', u'ż'),
    (u'ż', u'rz'),
    (u'p', u'b'),
    (u's', u'z'),
    (u'z', u's'),
    (u'rz', u'sz'),
    (u'sz', u'z'),
    (u'sz', u'ż'),
    (u'sz', u'rz'),
    (u'ji', u'i'),
    (u'cz', u'trz'),
    (u'trz', u'cz'),
    (u'rs', u'rws'),
    (u'd', u't')
]

space_errors = [
    (u'z ', u's'),
    (u'z ', u'z'),
    (u'w ', u'w'),
    (u'z ', u'z'),
    (u' by', u'by')
]

common_errors = polonica_errors + ort_errors + space_errors


def split_word(w, i, l):
    return list(w[:i]) + [w[i:i + l]] + list(w[i + l:])


def str_to_splits(w, char_groups):
    splits = [list(w)]
    if len(char_groups) == 0:
        return splits
    max_len = max([len(err) for err in char_groups])

    for l in xrange(2, max_len + 1):
        splits += [split_word(w, i, l) for i in range(len(w)) if i + l <= len(w) if w[i:i + l] in char_groups]
    return splits


def indicator(c_w, c_c):
    if c_w == c_c:
        return 0
    if (c_w, c_c) in common_errors:
        return 0.25
    return 1


def calculate_distance(w, c, threshold):
    len_w = len(w)
    len_c = len(c)

    distance = [[0 for i in xrange(len_c + 1)] for j in xrange(len_w + 1)]

    for i in xrange(0, len_w + 1):
        distance[i][0] = i

    for j in xrange(0, len_c + 1):
        distance[0][j] = j

    for i, c_w in enumerate(w, start=1):
        for j, c_c in enumerate(c, start=1):
            distance[i][j] = min(
                distance[i - 1][j] + 1,
                distance[i][j - 1] + 1,
                distance[i - 1][j - 1] + indicator(c_w, c_c)
            )

    return distance[len_w][len_c]


def levenshtein_distance(w, c, threshold=None):
    len_w = len(w)
    len_c = len(c)

    if min(len_w, len_c) == 0:
        return max(len_w, len_c)

    w_splits = str_to_splits(w, [err[0] for err in common_errors])
    c_splits = str_to_splits(c, [err[1] for err in common_errors])

    return min([calculate_distance(w, c, threshold) for w in w_splits for c in c_splits])


if __name__ == '__main__':
    print levenshtein_distance('kot', 'kot')
    print levenshtein_distance('kot', 'kod')
    print levenshtein_distance('abba', 'ala')
    print levenshtein_distance('telefon', 'telegraf')
    print levenshtein_distance('javascript', 'typescript')
    print levenshtein_distance('krowa', 'zdrowie')
    print levenshtein_distance(u'abonamęt', u'abonament')
    print levenshtein_distance('agrafce', 'agrawce')
    print levenshtein_distance(u'wodem', u'wodę')
