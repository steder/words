"""
Unittests to quickly verify :py:mod:`words.wordlib`

"""

import unittest

from words import wordlib


class TestFactorial(unittest.TestCase):
    def test_3(self):
        self.assertEqual(wordlib.factorial(3), 6)

    def test_7(self):
        self.assertEqual(wordlib.factorial(7), 5040)

    def test_9(self):
        self.assertEqual(wordlib.factorial(9), 362880)



class TestPermutations(unittest.TestCase):
    def test_n_pick_1(self):
        self.assertEqual(wordlib.permutations(5, 1), 5)

    def test_4_pick_2(self):
        self.assertEqual(wordlib.permutations(4, 2), 12)

    def test_n_pick_n(self):
        self.assertEqual(wordlib.permutations(5,5), 120)


class TestCombinations(unittest.TestCase):
    def test_5_choose_1(self):
        self.assertEqual(wordlib.combinations(5, 1), 5)

    def test_5_choose_2(self):
        self.assertEqual(wordlib.combinations(5, 2), 10)

    def test_n_choose_n(self):
        """
        This case is part of why combinations are much faster.
        """
        self.assertEqual(wordlib.combinations(5, 5), 1)


class TestAnagrams(unittest.TestCase):
    def setUp(self):
        self.dictionary = wordlib.Dictionary()

    def test_insert_anagrams(self):
        """
        We want to be able to do one lookup
        to get all the anagrams for a given
        set of letters.
        """
        self.dictionary.insertWord("able")
        self.dictionary.insertWord("elba")
        words = self.dictionary.getAnagrams("able")
        self.assertEqual(words, ["able", "elba"])


class TestGetWords(unittest.TestCase):
    WORDS = ["hello",
             "word",
             "world",
             ]

    def setUp(self):
        self.dictionary = wordlib.Dictionary()
        for word in self.WORDS:
            self.dictionary.insertWord(word)

    def test_success(self):
        r = self.dictionary.getWord("hello")
        self.assertEqual(r, "hello")

    def test_missing(self):
        r = self.dictionary.getWord("missing")
        self.assertEqual(r, None)


class TestScore(unittest.TestCase):
    def setUp(self):
        self.d = wordlib.Dictionary()

    def test_hello(self):
        score = self.d.getScore("Hello")
        self.assertEqual(score, (9, "hello"))

    def test_zen(self):
        score = self.d.getScore("zen")
        self.assertEqual(score, (13, "zen"))


class TestGetScrabbleWords(unittest.TestCase):
    WORDS = ['ae',
             'as',
             'at',
             'es',
             'et',
             'ta',
             'al',
             'ate',
             'eat',
             'el',
             'eta',
             'la',
             'sae',
             'sat',
             'sea',
             'set',
             'tae',
             'tas',
             'tea',
             'us',
             'ut',
             'ale',
             'als',
             'alt',
             'ates',
             'east',
             'eats',
             'eau',
             'els',
             'etas',
             'las',
             'lat',
             'lea',
             'let',
             'sal',
             'sate',
             'sau',
             'seat',
             'sel',
             'seta',
             'sue',
             'tau',
             'teas',
             'tel',
             'use',
             'uta',
             'ute',
             'uts',
             'ab',
             'ales',
             'alts',
             'ba',
             'be',
             'lase',
             'last',
             'late',
             'lats',
             'leas',
             'lest',
             'lets',
             'leu',
             'sale',
             'salt',
             'seal',
             'slat',
             'suet',
             'tael',
             'tale',
             'taus',
             'teal',
             'tela',
             'tels',
             'utas',
             'utes',
             'abs',
             'bas',
             'bat',
             'bet',
             'latu',
             'least',
             'lues',
             'lust',
             'lute',
             'sab',
             'saul',
             'saute',
             'setal',
             'slate',
             'slue',
             'stale',
             'steal',
             'stela',
             'tab',
             'taels',
             'tales',
             'teals',
             'tesla',
             'tule',
             'abet',
             'alb',
             'bal',
             'base',
             'bast',
             'bate',
             'bats',
             'beat',
             'bel',
             'best',
             'beta',
             'bets',
             'bus',
             'but',
             'lab',
             'lutea',
             'lutes',
             'sabe',
             'sault',
             'stab',
             'sub',
             'tabs',
             'talus',
             'tub',
             'tules',
             'abets',
             'able',
             'abut',
             'albs',
             'bale',
             'bals',
             'baste',
             'bates',
             'beast',
             'beats',
             'beau',
             'bels',
             'belt',
             'betas',
             'blae',
             'blat',
             'blet',
             'bust',
             'bute',
             'buts',
             'labs',
             'salute',
             'slab',
             'stub',
             'suba',
             'tabes',
             'tabu',
             'tuba',
             'tube',
             'tubs',
             'ables',
             'abuse',
             'abuts',
             'bales',
             'beaus',
             'beaut',
             'belts',
             'blase',
             'blast',
             'blate',
             'blats',
             'bleat',
             'blest',
             'blets',
             'blue',
             'lube',
             'sable',
             'slub',
             'table',
             'tabus',
             'tsuba',
             'tubae',
             'tubas',
             'tubes',
             'ablest',
             'beauts',
             'bleats',
             'blues',
             'bluet',
             'butle',
             'lubes',
             'stable',
             'tables',
             'tubal',
             'bluest',
             'bluets',
             'bustle',
             'butles',
             'suable',
             'sublet',
             'subtle',
             'usable',
             'sublate']

    def setUp(self):
        self.d = wordlib.Dictionary()
        for word in self.WORDS:
            self.d.insertWord(word)

    def test_lbea(self):
        words = self.d.getScrabbleWords("lbea")
        self.assertEqual(words,
                         [(2, 'ae'),
                          (3, 'al'),
                          (3, 'el'),
                          (3, 'la'),
                          (4, 'ale'),
                          (4, 'lea'),
                          (5, 'ab'),
                          (5, 'ba'),
                          (5, 'be'),
                          (7, 'alb'),
                          (7, 'bal'),
                          (7, 'bel'),
                          (7, 'lab'),
                          (8, 'able'),
                          (8, 'bale'),
                          (8, 'blae')]
                         )

    def test_lbea_with_wildcard(self):
        words = self.d.getScrabbleWordsWithWildcards("bill*")
        self.assertEqual(words,
                         [(3, 'al'),
                          (3, 'el'),
                          (3, 'la'),
                          (5, 'ab'),
                          (5, 'ba'),
                          (5, 'be'),
                          (7, 'alb'),
                          (7, 'bal'),
                          (7, 'bel'),
                          (7, 'lab')]
                         )


class TestPrefixLookups(unittest.TestCase):
    WORDS = ["penguin",
             "pen",
             "penknife",
             "pendulum",
             "yogurt",
             "yogi"]

    def setUp(self):
        self.d = wordlib.Dictionary()
        for word in self.WORDS:
            self.d.insertWord(word)

    def test_pen(self):
        words = self.d.getWordsStartingWith("pen")
        self.assertEqual(words, ['pen', 'pendulum', 'penguin', 'penknife'])

    def test_yog(self):
        words = self.d.getWordsStartingWith("yog")
        self.assertEqual(words, ["yogi", "yogurt"])

    def test_not_in_dictionary(self):
        words = self.d.getWordsStartingWith("blah")
        self.assertEqual(words, [])


class TestSuffixLookups(unittest.TestCase):
    """
    Populates a dictionary with some words with
    common suffixes for suffix lookups.
    """

    WORDS = [
        "grate",
        "denigrate",
        "integrate",
        "age",
        "message",
        "sausage",
             ]

    def setUp(self):
        self.dictionary = wordlib.Dictionary()
        for word in self.WORDS:
            self.dictionary.insertWord(word)

    def test_grate(self):
        self.assertEqual(self.dictionary.getWordsEndingWith("grate"),
                         ["denigrate", "grate", "integrate"])

    def test_age(self):
        self.assertEqual(self.dictionary.getWordsEndingWith("age"),
                         ["age", "message", "sausage"])

    def test_not_in_dictionary(self):
        words = self.dictionary.getWordsEndingWith("blah")
        self.assertEqual(words, [])


class TestPrefixLookupsWithLetters(unittest.TestCase):
    """
    If you have the dictionary with words:
      'bar'
      'baz'
      'bazil'
      'bazooka'
      'bingo'

    And you have a hand with 'gzrilpt'.

    If you want all the words beginningn with 'baz'
    then we should return 'bazil' and not bazooka
    because we have the letters to spell 'bazil'
    but not enough / or the right kind of letters to spell
    'bazooka' or 'bazill'.

    """
    WORDS = ["bar",
             "baz",
             "bazil",
             "bazooka",
             "bazill",
             "bingo"]

    def setUp(self):
        self.dictionary = wordlib.Dictionary()
        for word in self.WORDS:
            self.dictionary.insertWord(word)

    def test_startsWithBazAndHandContainsGzrilpt(self):
        #self.assertEqual(self.dictionary.getWordsEndingWith("grate"),
        #                 ["denigrate", "grate", "integrate"])
        self.assertEqual(
            self.dictionary.getWordsStartingWithPrefixContainingLetters("baz", "gzrilpt"),
            ["bazil"]
        )

