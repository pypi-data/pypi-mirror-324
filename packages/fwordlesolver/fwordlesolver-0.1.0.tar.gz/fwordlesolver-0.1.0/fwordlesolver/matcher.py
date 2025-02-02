from collections import defaultdict


def match(word, target):
    # pre calculate the hits
    places = ["x" if c == p else "." for c, p in zip(word, target)]
    # calculate the misplaces after hits
    # if there are multiple occurrences of same letter in word, we need to consider them:
    # * both hits -> no problem
    # * both misplaced -> both shown as misplaced
    # * one hit one misplaced -> hit is shown, misplaced is shown
    # * one hit one miss -> hit is shown, miss is shown as miss (not misplaced)
    word_miss = defaultdict(int)
    for i, (p, c) in enumerate(zip(places, word)):
        if p != ".":
            continue
        num_tc = target.count(c)  # number of occurrences of c in word
        num_th = sum(_p == "x" and _t == c for _p, _t in zip(places, target))
        if num_tc > num_th + word_miss[c]:
            word_miss[c] += 1
            places[i] = "?"
        # print(i, p, c, t, num_tc, num_th, ''.join(places))
    # print(word, target, ''.join(places))
    return "".join(places)
