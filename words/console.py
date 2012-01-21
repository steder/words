"""
Entry point for interactive console use in the standard python
interpreter or ipython.

"""

import pkgutil
import time

import wordlib


dictionary = None


print "Constructing new dictionary..."
start = time.time()
dictionary = wordlib.Dictionary()
words = pkgutil.get_data("words", "words.txt").split("\n")
for word in words:
    dictionary.insertWord(word)
end = time.time()
elapsed = end - start
print "\rConstructed new dictionary in %s seconds"%(elapsed,)

print "Example usage:"
print """
print dictionary.getScrabbleWords("ablesut")
print dictionary.getWordsStartingWith("quo")
"""
