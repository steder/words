from twisted.trial import unittest
from twisted.web import resource
from twisted.web import server
from twisted.web.test import test_web

from words.web import root
from words.web import dictionary
from words import wordlib


class MockServer(object):
    def __init__(self, dictionary):
        self.dictionary = dictionary


class TestRootResource(unittest.TestCase):
    def setUp(self):
        self.server = MockServer(None)
        self.r = root.Root(self.server)

    def test_create(self):
        r = root.Root(self.server)
        self.assertTrue(r is not None)

    def test_renderGet(self):
        """should get the login page"""
        result = self.r.render_GET(test_web.DummyRequest(['']))
        self.assertTrue(result == server.NOT_DONE_YET)
        return self.r.d


class TestRootTraversal(unittest.TestCase):
    def setUp(self):
        self.server = MockServer(None)
        self.r = root.Root(self.server)

    def test_missing_resource(self):
        request = test_web.DummyRequest([''])
        child = self.r.getChild("not_a_real_resource", request)
        self.assertTrue(isinstance(child, resource.NoResource))

    def test_dictionary(self):
        request = test_web.DummyRequest([''])
        child = self.r.getChild("dictionary", request)
        self.assertTrue(isinstance(child, dictionary.DictionaryResource))


class TestDictionaryResource(unittest.TestCase):
    def setUp(self):
        self.dictionary = wordlib.Dictionary()
        self.dictionary.insertWord("hello")
        self.server = MockServer(self.dictionary)
        self.root = root.Root(self.server)
        self.r = self.root.getChild("dictionary", None)

    def test_failure(self):
        def fail(*args, **kwargs):
            print "Fail being called"
            raise Exception("Failing on purpose")
        self.r.handle_GET = fail

        request = test_web.DummyRequest([''])
        request.method = "GET"
        rval = self.r.render(request)
        self.assertEqual(rval, server.NOT_DONE_YET)
        def eb(result, request):
            self.assertEqual(request.responseCode, 500, "Response code should be INTERNAL_SERVER_ERROR")
        self.r.d.addCallback(eb, request)
        return self.r.d

    def test_getScrabbleWords_noLetters(self):
        request = test_web.DummyRequest([''])
        request.args["letters"] = []
        request.method = "GET"
        rval = self.r.render(request)
        self.assertEqual(rval, server.NOT_DONE_YET)
        def cb(result):
            self.assertEqual(result, [])
        self.r.d.addCallbacks(cb, self.fail)
        return self.r.d

    def test_getScrabbleWords_letters_ehllo(self):
        request = test_web.DummyRequest([''])
        request.args["letters"] = ["ehllo"]
        request.method = "GET"
        rval = self.r.render(request)
        self.assertEqual(rval, server.NOT_DONE_YET)
        def cb(result, request):
            self.assertEqual(result, [(9, "hello")])
            self.assertEqual(request.written, ["[(9, 'hello')]"])
        self.r.d.addCallbacks(cb, self.fail, callbackArgs=(request,))
        return self.r.d


class TestJsonDictionaryResource(unittest.TestCase):
    def setUp(self):
        self.dictionary = wordlib.Dictionary()
        self.dictionary.insertWord("hello")
        self.server = MockServer(self.dictionary)
        self.root = root.Root(self.server)
        self.r = self.root.getChild("dictionary.json", None)

    def test_getScrabbleWords_letters_ehllo(self):
        request = test_web.DummyRequest([''])
        request.args["letters"] = ["ehllo"]
        request.method = "GET"
        rval = self.r.render(request)
        self.assertEqual(rval, server.NOT_DONE_YET)
        def cb(result, request):
            self.assertEqual(result, [(9, "hello")])
            self.assertEqual(request.written, ['[[9, "hello"]]'])
        self.r.d.addCallbacks(cb, self.fail, callbackArgs=(request,))
        return self.r.d
