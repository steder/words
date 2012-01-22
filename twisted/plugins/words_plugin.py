from zope import interface

from twisted import plugin
from twisted.application import service
from twisted.python import usage

from words import server, settings


class Options(usage.Options):
    optParameters = (
        ('port', 'p', None, 'Port on which to listen.'),
    )


class WordsServiceMaker(object):
    interface.implements(plugin.IPlugin, service.IServiceMaker)
    description = "Words with Friends Solver Service"
    options = Options
    tapname = 'words'

    def makeService(self, options):
        """
        Return an instance of words.server.WordsServer
        """
        port = settings.port

        if options['port'] is not None:
            port = int(options['port'])

        from words import console
        return server.WordsServer(port, console.dictionary)


serviceMaker = WordsServiceMaker()
