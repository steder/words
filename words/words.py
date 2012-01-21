#!/usr/bin/env python

"""
"""

import os
import pkgutil
import time

import wordlib


dictionary = None


def main():
    global dictionary
    print "Constructing new dictionary..."
    start = time.time()
    dictionary = wordlib.Dictionary()
    words = pkgutil.get_data("words", "words.txt").split("\n")
    for word in words:
        dictionary.insertWord(word)
    end = time.time()
    elapsed = end - start
    print "\rConstructed new dictionary in %s seconds"%(elapsed,)

    print dictionary.getScrabbleWords("ablesut")
    print dictionary.getWordsStartingWith("quo")


if __name__=="__main__":
    main()
