#!/usr/bin/env python

"""
"""

import os
import cPickle as pickle
import time

import wordlib

#WORD_PATH = "/usr/share/dict/words"
# /usr/share/dict/words includes words
# that WoF doesn't think are words and
# misses some words that WoF thinks are
# words.
# This words file is from:
# http://blogmybrain.com/words-with-friends-cheat/words.txt
WORD_PATH = "words.txt"
PICKLE_PATH = "dictionary.pickle"


dictionary = None


def save_dictionary():
    global dictionary
    pickleFile = open(PICKLE_PATH, "w")
    try:
        pickle.dump(dictionary, pickleFile)
    except PicklingError:
        pickleFile.close()
        os.unlink(PICKLE_PATH)
    else:
        pickleFile.close()


if __name__=="__main__":
    if os.path.exists(PICKLE_PATH):
        print "Unpickling dictionary..."
        start = time.time()
        with open(PICKLE_PATH, "r") as pickleFile:
            dictionary = pickle.load(pickleFile)
        end = time.time()
        elapsed = end - start
        print "Unpickled dictionary in %s seconds"%(elapsed,)
    else:
        print "Constructing new dictionary..."
        start = time.time()
        dictionary = wordlib.Dictionary()
        with open(WORD_PATH, "r") as wordsFile:
            for word in wordsFile:
                dictionary.insertWord(word)
        end = time.time()
        elapsed = end - start
        print "\rConstructed new dictionary in %s seconds"%(elapsed,)

    print dictionary.getScrabbleWords("ablesut")
    print dictionary.getWordsStartingWith("quo")
