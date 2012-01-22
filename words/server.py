#-*- test-case-name: words.test.test_server -*-
"""
Defines the Words Server

"""
from twisted.application import internet, service
from twisted.internet import defer, reactor
from twisted.python import log
from twisted.web import server

from words.web import root


class WordsServer(service.MultiService):
    def __init__(self, port):
        service.MultiService.__init__(self)
        webServerFactory = server.Site(root.Root())
        webServer = internet.TCPServer(port, webServerFactory)
        webServer.setName("Words")
        webServer.setServiceParent(self)

    def _cbStarted(self, result):
        service.MultiService.startService(self)        
        return result

    def _ebError(self, failure):
        log.err("failure starting service:", failure)
        return failure

    def startupHook(self, deferred):
        """Include additional startup steps here

        """
        deferred.callback(True)

    def startService(self):
        d = defer.Deferred()
        d.addCallback(self._cbStarted)
        d.addErrback(self._ebError)
        reactor.callWhenRunning(self.startupHook, d)
        return d

    def stopService(self):
        print "Shutting down service:"
        return service.MultiService.stopService(self)
