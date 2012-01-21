"""
This works but is considerably slower because it has to check
every permutation of the letters.
"""

import itertools
import sys

dictionary = {}

def getScrabbleWords(letters):
    letters = letters.strip().lower()
    words = []
    for x in xrange(2, len(letters)+1):
        for permutation in itertools.permutations(letters, x):
            word = "".join(permutation)
            if word in dictionary:
                words.append(word)
    words.sort()
    return words

with open("words.txt") as f:
    for word in f:
        dictionary[word.strip().lower()] = 1
print getScrabbleWords(sys.argv[1])

