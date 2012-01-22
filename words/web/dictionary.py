#-*- test-case-name: words.test.test_web -*-
"""
"""

import json
import os

from twisted.python import log
from twisted.internet import defer
from twisted.internet import reactor
from twisted.internet import threads
from twisted.web import http
from twisted.web import resource
from twisted.web import server
from twisted.web import static


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

    def handle_GET(self, request):
        lettersArg = request.args.get("letters", [])
        letters = "".join(lettersArg)
        words = []
        if letters:
            words = list(reversed(self.dictionary.getScrabbleWordsWithWildcards(letters)))
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
        log.err(error)
        request.setResponseCode(http.INTERNAL_SERVER_ERROR)
        request.write(error.getErrorMessage())
        request.finish()

    def render_GET(self, request):
        self.d = threads.deferToThread(self.handle_GET, request)
        self.d.addCallback(self.cb, request)
        self.d.addErrback(self.eb, request)
        return server.NOT_DONE_YET



