#!?usr/bin/env python
"""
"""


import itertools
import os
import string
import sys
import time
import unittest


EndOfWord = Ellipsis

def loadWords(wordsPath="/usr/share/dict/words"):
    wordsList = []
    with open(wordsPath, "r") as words:
        for word in words:
            word = word.strip()
            wordsList.append(word)
    return wordsList

WORDS = loadWords()

LETTER_POINTS = {
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
    "*":0,
}


class Trie(object):
    def __init__(self):
        self.trie = {}

    def insert(self, string):
        #string = string.lower()
        trie = self.trie
        length = len(string)
        n = 0
        if string == "otomi":
            print "inserting otomi"
        for c in string.lower():
            n += 1
            if c not in trie:
                if n == length:
                    trie[c] = {"EOW":EndOfWord,
                               "PROPER":string[0].isupper()}
                else:
                    trie[c] = {"EOW":None}
            trie = trie[c]

    def find(self, string):
        string = string.lower()
        matching = ""
        trie = self.trie
        for c in string:
            trie = trie.get(c, None)
            if not trie:
                return None
            matching += c

        if trie["EOW"] is EndOfWord:
            if trie.get("PROPER", False):
                return matching.capitalize()
            return matching


class TestTrie(unittest.TestCase):
    def setUp(self):
        self.t = Trie()

    def test1(self):
        self.t.insert("hello")
        self.t.insert("hi")
        word = self.t.find("hello")
        self.assertEqual(word, "hello")


if __name__=="__main__":

    trie = Trie()
    print "inserting words..."
    start = time.time()
    for word in WORDS:
        trie.insert(word)
    end = time.time()
    elapsed = end - start
    print "Inserted %s words in %s seconds."%(len(WORDS), elapsed)

    inputString = sys.argv[1].lower().strip()
    print "Searching for words containing the following characters: %s"%(inputString,)

    def findPermutations(inputString):
        words = []
        for n in xrange(2, len(inputString)+1):
            for permutation in itertools.permutations(inputString, n+1):
                candidate = "".join(permutation)
                word = trie.find(candidate)
                if word:
                    words.append(word)
        return words

    # sort words first by length and then by alpha
    def scoreWord(inputString, word):
        allowed = inputString.lower()
        word = word.lower()

        score = 0
        for character in word:
            if character in allowed:
                score += LETTER_POINTS[character]
        return score

    start = time.time()

    if "*" not in inputString:
        words = findPermutations(inputString)
    else:
        # handle wildcards: if input string includes "*"
        # try all 26 letters and see if you can make any other words
        # To handle multiple wildcards we extract all wildcards and then
        # then use itertools.product to insert all possible combinations
        words = []
        nWildcards = inputString.count("*")
        nonWildcardInput = inputString.replace("*", "")
        for wildCards in itertools.product(string.letters, repeat=nWildcards):
            words.extend(findPermutations(nonWildcardInput + "".join(wildCards)))

    if words:
        print "words:", words
        words.sort(key=lambda word: (scoreWord(inputString, word), len(word), word.lower()))
        print "%s could be used to make the word(s):"%(inputString,)
        for word in words:
            print "%s: %s (%s)"%(len(word), word, scoreWord(inputString, word))
    else:
        print "No words could be made with %s"%(inputString,)

    end = time.time()
    elapsed = end - start
    print "Found and scored %s words in %s seconds."%(len(words), elapsed)
