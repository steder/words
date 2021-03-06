#-*- test-case-name: words.test.test_web -*-
"""
"""

import itertools
import json
#import os
import re

from twisted.python import log
#from twisted.internet import defer
#from twisted.internet import reactor
from twisted.internet import threads
from twisted.web import http
from twisted.web import resource
from twisted.web import server
#from twisted.web import static


# for validating the input:
pattern = "[^abcdefghijklmnopqrstuvwxyABCDEFGHIJKLMNOPQRSTUVWXYZ*]+"
regex = re.compile(pattern)


class DictionaryResource(resource.Resource):
    def __init__(self, server):
        resource.Resource.__init__(self)
        self.dictionary = server.dictionary
        self.d = None
        self.format = None

    def setFormat(self, extension):
        if extension == ".json":
            self.format = "json"
        else:
            self.format = "text"

    def getLetters(self, request):
        lettersArg = request.args.get("letters", [])
        letters = "".join(lettersArg)
        letters = regex.sub("", letters)
        return letters

    def handle_GET(self, request):
        letters = self.getLetters(request)
        words = []
        if letters:
            # get a maximum of the first 1000 words which seems like more than anyone is likely to look at:
            words = list(itertools.islice(reversed(self.dictionary.getScrabbleWordsWithWildcards(letters)), 0, 1000))
        request.setResponseCode(http.OK)
        if self.format == "json":
            data = json.dumps(words)
            request.write(data)
        else:
            request.write(str(words))
        return words

    def cb(self, result, request):
        request.finish()
        return result

    def eb(self, error, request):
        log.err("Error occured while handling dictionary request")
        request.setResponseCode(http.INTERNAL_SERVER_ERROR)
        request.write(error.getErrorMessage())
        request.finish()

    def render_GET(self, request):
        letters = self.getLetters(request)
        print "letters: '%s'"%(letters,)
        if len(letters) > 10:
            return json.dumps([
                [0, "Please use 10 characters or less"],
                ])
        elif letters.count("*") > 3:
            return json.dumps([
                [0, "Please use 3 or fewer wildcards (*)"]
                ])
        elif letters == "":
            return json.dumps([
                [0, "Please enter up to 10 letters (including 3 \'*\' wildcards)"]
                ])
        else:
            self.d = threads.deferToThread(self.handle_GET, request)
            self.d.addCallback(self.cb, request)
            self.d.addErrback(self.eb, request)
            return server.NOT_DONE_YET



