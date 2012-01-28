#-*- test-case-name: words.test_wordlib -*-

"""
Defines a :class:`Dictionary` that supports various queries
useful in playing Scrabble or Words with Friends.

"""

from functools import wraps
import itertools
import string


WWF = "WORDS_WITH_FRIENDS"
SCRABBLE = "SCRABBLE"
SCORES = {
    SCRABBLE: {"a":1,
               "b":1,
               "c":1,
               "d":1,
               "e":1,
               "f":1,
               "g":1,
               "h":1,
               "i":1,
               "j":1,
               "k":1,
               "l":1,
               "m":1,
               "n":1,
               "o":1,
               "p":1,
               "q":1,
               "r":1,
               "s":1,
               "t":1,
               "u":1,
               "v":1,
               "w":1,
               "x":1,
               "y":1,
               "z":1,},
    WWF: {
    "a":1,
    "b":4,
    "c":4,
    "d":2,
    "e":1,
    "f":4,
    "g":3,
    "h":3,
    "i":1,
    "j":10,
    "k":5,
    "l":2,
    "m":4,
    "n":2,
    "o":1,
    "p":4,
    "q":10,
    "r":1,
    "s":1,
    "t":1,
    "u":2,
    "v":5,
    "w":4,
    "x":8,
    "y":3,
    "z":10,
    "*":0,}
}


# I found it useful to play with these
# to get a sense how many times I'd
# need to query my dictionary to do
# scrabble lookups.
def factorial(n):
    """
    Calculate n!

    .. note:: This is an iterative implementation of factorial.
        Recursive factorial is so bourgeois. :-)

        Seriously it is nice to have the option to be able to calculate factorial
        bigger than sys.getrecursionlimit().

    :arg n:
    :type n: int
    """
    f = 1
    for x in xrange(1, n+1):
        f *= x
    return f


def permutations(n, k):
    """select k out of n, including order"""
    return factorial(n) / factorial(n-k)


def combinations(n, r):
    """select r out of n, ignoring order"""
    return permutations(n, r) / factorial(r)


EOW = 0


class Dictionary(object):
    """
    Not a Python dictionary but an actual dictionary of words
    """
    def __init__(self):
        self.nodeCount = 0
        self.wordCount = 0
        self.nodes = {}
        # store words in a trie for lookups of
        # all words starting with a prefix
        self.trie = {}
        # suffix lookups:
        self.suffixTrie = {}

    def cleanWord(f):
        """
        Method decorator to help methods of this class keep it DRY.
        """
        @wraps(f)
        def cleanWordDeco(self, word):
            return f(self, word.strip().lower())
        return cleanWordDeco

    @cleanWord
    def insertWord(self, word):
        """
        Insert a word into the dictionaries indexes.

        :arg word: The word to insert
        :type arg: str
        """
        self.insertNode(word)
        self.insertTrie(word)

    def insertNode(self, word):
        """
        Store anagrams in a hash table keyed on sorted version of `word`

        :arg word: The word to insert
        :type word: str
        """
        letters = "".join(sorted(word))
        if letters not in self.nodes:
            self.wordCount += 1
            self.nodeCount += 1
            self.nodes[letters] = [word]
        elif word not in self.nodes[letters]:
            self.wordCount += 1
            self.nodes[letters].append(word)

    def insertTrie(self, word):
        """
        Store `word` in trie structures for efficient prefix/suffix lookups.

        :arg word: The word to insert
        :type word: str
        """
        self._insertTrie(self.trie, word)
        self._insertTrie(self.suffixTrie, reversed(word))

    def _insertTrie(self, trie, letters):
        """
        Helper method to store a word in a single trie.

        """
        trieNode = trie
        for letter in letters:
            if not letter in trieNode:
                trieNode[letter] = {}
            trieNode = trieNode[letter]
        trieNode[EOW] = 1

    @cleanWord
    def getWord(self, word):
        """
        Check if `word` is a valid word.

        :arg word: The word to lookup
        :type word: str
        :returns: Returns the word found or none.
        """
        letters = "".join(sorted(word))
        words = self.nodes.get(letters, [])
        if word in words:
            return word
        else:
            return None

    @cleanWord
    def getAnagrams(self, word):
        """
        :arg word: The word to lookup
        :type word: str
        :returns: Returns list of anagrams for `word`
        """
        letters = "".join(sorted(word))
        words = self.nodes.get(letters, [])
        return words

    @cleanWord
    def getScore(self, word):
        """
        Compute Words With Friends score for a given word.

        :arg word: any string although it should be a valid word
        :type word: str
        :returns: Returns a tuple of the score of that word in Words with Friends (int) and the word (str)
        """
        scores = SCORES[WWF]
        score = sum(map(lambda x: scores[x], word))
        return score, word

    @cleanWord
    def getScrabbleWords(self, letters):
        """
        Given a set of scrambled letters return a list of all the unique words
        that can be spelled with those letters sorted by their WWF score.
        """
        lookupCount = 0
        words = []
        letters = "".join(sorted(letters))
        for n in xrange(2, len(letters)+1):
            for combination in itertools.combinations(letters, n):
                candidate = "".join(combination)
                lookupCount += 1
                w = self.nodes.get(candidate, [])
                if w:
                    words.extend(w)

        # remove duplicates and sort appropriately
        words = map(self.getScore, set(words))
        words.sort()
        return words

    @cleanWord
    def getScrabbleWordsWithWildcards(self, letters):
        """
        Given a set of scrambled letters (including wildcards) return a list of
        all the unique words that can be spelled with those letters sorted by their
        WWF score.

        .. note:: any '*' characters in letters indicate wildcards.

        :arg letters: letters and wildcards that to search for in the dictionary
        :type letters: str
        :returns: Unique list of words sorted by WWF score.

        """
        lookupCount = 0
        wildcard, blank = "*", ""
        wildcardCount = letters.count(wildcard)
        # after counting wildcards remove them:
        letters.replace(wildcard, blank)
        # now generate possible combinations for the
        # wildcards and find words:
        words = []
        for combination in itertools.combinations(string.letters[0:26],
                                                  wildcardCount):
            candidate = letters + "".join(combination)
            lookupCount += 1
            results = self.getScrabbleWords(candidate)
            if results:
                words.extend(results)

        words = list(set(words))
        words.sort()

        return words

    def depthFirstWords(self, letters, trieNode, accumulator):
        """
        Recursive depth first traversal of the tree to retrieve all
        the child words

        """
        for letter, node in trieNode.iteritems():
            if letter != EOW and node:
                if node.get(EOW, False):
                    accumulator.append("".join(letters + letter))
                self.depthFirstWords(letters+letter, node, accumulator)
        return accumulator

    def getWordsFromTrieWithTransform(self, trie, letters, transform):
        """
        Apply `transform` to `letters` and return words in `trie` that
        match include the transformed letters.

        :arg trie:
        :type trie: dict
        :arg letters:
        :type letters: str
        :arg transform:
        :type transform: callable
        :returns: list

        """
        trieNode = trie
        letters = transform(letters)
        for letter in letters:
            trieNode = trieNode.get(letter, None)
            if not trieNode:
                return []

        words = []
        if trieNode.get(EOW, False):
            words.append("".join(letters))

        self.depthFirstWords(letters, trieNode, words)

        words = [transform(word) for word in words]
        words.sort()
        return words

    @cleanWord
    def getWordsStartingWith(self, letters):
        """
        Return a list of words beginning with `letters`

        :arg letters:
        :type letters: str
        :returns: list

        """
        identity = lambda x: x
        return self.getWordsFromTrieWithTransform(self.trie, letters, identity)

    def getWordsStartingWithPrefixContainingLetters(self, prefix, letters):
        return []

    @cleanWord
    def getWordsEndingWith(self, letters):
        """
        Return a list of words ending with `letters`

        :arg letters:
        :type letters: str
        :returns: list

        """
        reverseString = lambda x: "".join(reversed(x))
        return self.getWordsFromTrieWithTransform(self.suffixTrie, letters, reverseString)


