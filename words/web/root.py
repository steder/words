#-*- test-case-name: words.test.test_web -*-
import os

from twisted.python import log
from twisted.internet import defer, reactor
from twisted.web import http, resource, server, static

from words import settings
from words.web import dictionary


routes = {"dictionary":dictionary.DictionaryResource}


class Root(resource.Resource):
    def __init__(self, server):
        resource.Resource.__init__(self)
        self.server = server
        self.putChild("static", static.File(settings.words_root.child("words").child("static").path))
        self.putChild("favicon.ico", static.File(settings.words_root.child("words").child("favicon.ico").path))

    def _failed(self, reason):
        log.err(reason)
        return http.Response(
            code=500,
            headers=None,
            stream=reason.getErrorMessage()
        )

    def _got(self, result, request):
        request.setResponseCode(http.OK)
        request.write(result)
        request.finish()

    def getStaticFile(self, deferred):
        filepath = os.path.join(settings.words_root.path, "words/static/index.html")
        template = open(filepath, "r")
        contents = template.read()
        deferred.callback(contents)

    def render_GET(self, request):
        self.d = defer.Deferred()
        self.d.addCallback(self._got, request)
        self.d.addErrback(self._failed)
        reactor.callLater(0.001, self.getStaticFile, self.d)
        return server.NOT_DONE_YET

    def getChild(self, path, request):
        path, ext = os.path.splitext(path)
        if path == "":
            return self
        elif path in routes:
            child_resource = routes[path]
            instance = child_resource(self.server)
            instance.setFormat(ext)
            return instance
        return resource.Resource.getChild(self, path, request)
