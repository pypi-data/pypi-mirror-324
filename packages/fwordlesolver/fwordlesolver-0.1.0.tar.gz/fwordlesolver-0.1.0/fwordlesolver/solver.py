from collections import defaultdict

from .data import all_words


class Solver:
    def __init__(self, word_size: int):
        self.word_size = word_size
        self.words = [w for w in all_words if len(w) == word_size]
        self.char_cnts = defaultdict(int)

    def update_char_cnts(self):
        self.char_cnts = defaultdict(int)
        for w in self.words:
            for c in set(w):
                self.char_cnts[c] += 1

    @property
    def len_words(self):
        return len(self.words)

    def get_score(self, word):
        return sum(
            self.len_words - abs(2 * self.char_cnts[c] - self.len_words)
            for c in set(word)
        )

    def get_suggestions(self):
        self.update_char_cnts()
        return sorted(self.words, key=self.get_score)[-5:][::-1]

    def filter_words(self, check_func: lambda x: bool):
        self.words = [w for w in self.words if check_func(w)]

    def validate_inputs(self, word: str, places: str):
        if len(word) != self.word_size or len(places) != self.word_size:
            raise TypeError(f"Invalid input length, expected {self.word_size}")
        for p in places:
            if p not in "x.?":
                raise TypeError(f"Invalid placement character: {p}")

    def filter_word(self, word: str, places: str):
        word = word.strip().lower()
        places = places.strip().lower()

        self.validate_inputs(word, places)

        for i, (c, p) in enumerate(zip(word, places)):
            len_words = len(self.words)
            if p == "x":
                self.filter_words(lambda w: w[i] == c)
            if p == "?":
                self.filter_words(lambda w: w[i] != c and c in w)
            if p == ".":
                hits = sum(1 for (_c, _p) in zip(word, places) if _p != "." and _c == c)
                self.filter_words(lambda w: w.count(c) <= hits)
            print(f"Filtered {c}{p} from {len_words} to {len(self.words)}")
        print("-" * 20)
        print(self.words)
        print("-" * 20)
