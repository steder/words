"""
"""

from functools import wraps
import itertools
import string


WOF = "WORDS_WITH_FRIENDS"
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
    WOF: {
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
    recursive factorial is so bourgeois :-)
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
    def __init__(self):
        self.nodeCount = 0
        self.wordCount = 0
        self.nodes = {}
        # store words in a trie for lookups of
        # all words starting with a prefix
        self.trie = {}

    def cleanWord(f):
        def cleanWordDeco(self, word):
            return f(self, word.strip().lower())
        wraps(f, cleanWordDeco)
        return cleanWordDeco

    @cleanWord
    def insertWord(self, word):
        self.insertNode(word)
        self.insertTrie(word)

    def insertNode(self, word):
        letters = "".join(sorted(word))
        if letters not in self.nodes:
            self.wordCount += 1
            self.nodeCount += 1
            self.nodes[letters] = [word]
        elif word not in self.nodes[letters]:
            self.wordCount += 1
            self.nodes[letters].append(word)

    def insertTrie(self, word):
        trieNode = self.trie
        for letter in word:
            if not letter in trieNode:
                trieNode[letter] = {}
            trieNode = trieNode[letter]
        trieNode[EOW] = 1

    @cleanWord
    def getWord(self, word):
        letters = "".join(sorted(word))
        words = self.nodes.get(letters, [])
        if word in words:
            return word
        else:
            return None

    @cleanWord
    def getAnagrams(self, word):
        letters = "".join(sorted(word))
        words = self.nodes.get(letters, [])
        return words

    @cleanWord
    def getScore(self, word):
        scores = SCORES[WOF]
        score = sum(map(lambda x: scores[x], word))
        return score, word

    @cleanWord
    def getScrabbleWords(self, letters):
        lookupCount = 0
        words = []
        letters = "".join(sorted(letters))
        for n in xrange(2, len(letters)+1):
            print "Trying %s length permutations of %s"%(n, letters)
            for combination in itertools.combinations(letters, n):
                candidate = "".join(combination)
                lookupCount += 1
                w = self.nodes.get(candidate, [])
                if w:
                    words.extend(w)

        # remove duplicates and sort appropriately
        words = map(self.getScore, set(words))
        words.sort()

        print "Found words in %s lookups."%(lookupCount,)
        return words

    @cleanWord
    def getScrabbleWordsWithWildcards(self, letters):
        """
        any '*' characters in letters indicate wildcards.
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

        print "Tried %s wildcard lookups."%(lookupCount,)
        return words

    @cleanWord
    def getWordsStartingWith(self, letters):
        """
        :arg: letters

        Returns a list of words beginning with letters
        """
        trieNode = self.trie
        for letter in letters:
            trieNode = trieNode.get(letter, None)
            if not trieNode:
                return None
        # now we're at the root trie node for all words that
        # begin with letters.  we'll want to do a depth
        # first traversal of the tree to retrieve all the child
        # words:

        def prefixWords(letters, trieNode, accumulator):
            for letter, node in trieNode.iteritems():
                if letter != EOW and node:
                    print "prefixWords checking word: ", "".join(letters+letter)
                    if node.get(EOW, False):
                        accumulator.append("".join(letters + letter))
                    prefixWords(letters+letter, node, accumulator)
            return accumulator

        words = []
        if trieNode.get(EOW, False):
            words.append("".join(letters))
        prefixWords(letters, trieNode, words)
        words.sort()
        return words




