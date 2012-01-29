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
            raise Exception("Failing on purpose")
        self.r.handle_GET = fail

        request = test_web.DummyRequest([''])
        request.args["letters"] = ["ehllo"]
        request.method = "GET"
        rval = self.r.render(request)
        self.assertEqual(rval, server.NOT_DONE_YET)
        def eb(result, request):
            self.assertEqual(request.responseCode, 500, "Response code should be INTERNAL_SERVER_ERROR")
        self.r.d.addCallback(eb, request)
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
        self.dictionary.insertWord("foo")
        self.dictionary.insertWord("foobar")
        self.dictionary.insertWord("barbaz")
        self.dictionary.insertWord("foobarbaz")
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

    def test_getScrabbleWords_letters_oneWord(self):
        request = test_web.DummyRequest([''])
        request.args["letters"] = ["EHLLO"]
        request.method = "GET"
        rval = self.r.render(request)
        self.assertEqual(rval, server.NOT_DONE_YET)
        def cb(result, request):
            self.assertEqual(result, [(9, "hello")])
            self.assertEqual(request.written, ['[[9, "hello"]]'])
        self.r.d.addCallbacks(cb, self.fail, callbackArgs=(request,))
        return self.r.d

    def test_getScrabbleWords_letters_twoWords(self):
        request = test_web.DummyRequest([''])
        request.args["letters"] = ["foobar"]
        request.method = "GET"
        rval = self.r.render(request)
        self.assertEqual(rval, server.NOT_DONE_YET)
        def cb(result, request):
            self.assertEqual(result, [(12, "foobar"),
                                      (6, "foo")])
            self.assertEqual(request.written, ['[[12, "foobar"], [6, "foo"]]'])
        self.r.d.addCallbacks(cb, self.fail, callbackArgs=(request,))
        return self.r.d


    def test_tooManyLetters(self):
        request = test_web.DummyRequest([''])
        request.args["letters"] = ["abcdefghijk"]
        request.method = "GET"
        rval = self.r.render(request)
        self.assertEqual(rval, '[[0, "Please use 10 characters or less"]]')

    def test_tooManyWildcards(self):
        request = test_web.DummyRequest([''])
        request.args["letters"] = ["****"]
        request.method = "GET"
        rval = self.r.render(request)
        self.assertEqual(rval, '[[0, "Please use 3 or fewer wildcards (*)"]]')

    def test_noLetters(self):
        request = test_web.DummyRequest([''])
        request.args["letters"] = []
        request.method = "GET"
        rval = self.r.render(request)
        self.assertEqual(rval, '[[0, "Please enter up to 10 letters (including 3 \'*\' wildcards)"]]')

    def test_notAllowedCharacters(self):
        request = test_web.DummyRequest([''])
        request.args["letters"] = [":-("]
        request.method = "GET"
        rval = self.r.render(request)
        self.assertEqual(rval, '[[0, "Please enter up to 10 letters (including 3 \'*\' wildcards)"]]')

    def test_prefixLetters(self):
        """
        If a request specifies query arg 'prefix_letters' we should
        return only words that can be spelled with those letters
        and that begin with prefix_letters.
        """
        request = test_web.DummyRequest([''])
        request.args["letters"] = ["barz"]
        request.args["prefix_letters"] = ["foo"]
        rval = self.r.render(request)
        self.assertEqual(rval, server.NOT_DONE_YET)
        def cb(result, request):
            self.assertEqual(result, [(12, "foobar")])
            self.assertEqual(request.written, ['[[12, "foobar"]]'])
        self.r.d.addCallbacks(cb, self.fail, callbackArgs=(request,))
        return self.r.d

    def test_prefixLettersMultipleResults(self):
        """
        Confirm prefix multiple results are sorted
        """
        request = test_web.DummyRequest([''])
        request.args["letters"] = ["bazbar"]
        request.args["prefix_letters"] = ["foo"]
        rval = self.r.render(request)
        self.assertEqual(rval, server.NOT_DONE_YET)
        def cb(result, request):
            self.assertEqual(result, [(27, "foobarbaz"),
                                      (12, "foobar")])
            self.assertEqual(request.written, ['[[27, "foobarbaz"], [12, "foobar"]]'])
        self.r.d.addCallbacks(cb, self.fail, callbackArgs=(request,))
        return self.r.d

    def test_tooManyPrefixLetters(self):
        """Confirm that >10 prefix letters causes an error message"""
        request = test_web.DummyRequest([''])
        request.args["letters"] = ["barz"]
        request.args["prefix_letters"] = ["foofoofoofoo"]
        rval = self.r.render(request)
        self.assertEqual(rval, '[[0, "Please enter up to 10 prefix letters"]]')

    def test_wildcardsInPrefixLetters(self):
        """Confirm that * letters cause an error message in the prefix field"""
        request = test_web.DummyRequest([''])
        request.args["letters"] = ["barz"]
        request.args["prefix_letters"] = ["foo*"]
        rval = self.r.render(request)
        self.assertEqual(rval, '[[0, "Please enter up to 10 prefix letters (but no wildcards!)"]]')

    def test_suffixLetters(self):
        """
        If a request specifies query arg 'prefix_letters' we should
        return only words that can be spelled with those letters
        and that begin with prefix_letters.
        """
        request = test_web.DummyRequest([''])
        request.args["letters"] = ["oof"]
        request.args["suffix_letters"] = ["bar"]
        rval = self.r.render(request)
        self.assertEqual(rval, server.NOT_DONE_YET)
        def cb(result, request):
            self.assertEqual(result, [(12, "foobar")])
            self.assertEqual(request.written, ['[[12, "foobar"]]'])
        self.r.d.addCallbacks(cb, self.fail, callbackArgs=(request,))
        return self.r.d

    def test_suffixLettersMultipleResults(self):
        """
        Confirm multiple suffix results are sorted
        """
        request = test_web.DummyRequest([''])
        request.args["letters"] = ["foobar"]
        request.args["suffix_letters"] = ["baz"]
        rval = self.r.render(request)
        self.assertEqual(rval, server.NOT_DONE_YET)
        def cb(result, request):
            self.assertEqual(result, [(27, "foobarbaz"),
                                      (21, "barbaz")])
            self.assertEqual(request.written, ['[[27, "foobarbaz"], [21, "barbaz"]]'])
        self.r.d.addCallbacks(cb, self.fail, callbackArgs=(request,))
        return self.r.d

    def test_tooManySuffixLetters(self):
        """Confirm that >10 suffix letters causes an error message"""
        request = test_web.DummyRequest([''])
        request.args["letters"] = ["barz"]
        request.args["suffix_letters"] = ["foofoofoofoo"]
        rval = self.r.render(request)
        self.assertEqual(rval, '[[0, "Please enter up to 10 suffix letters"]]')

    def test_wildcardsInSuffixLetters(self):
        """Confirm that * letters cause an error message in the suffix field"""
        request = test_web.DummyRequest([''])
        request.args["letters"] = ["barz"]
        request.args["suffix_letters"] = ["foo*"]
        rval = self.r.render(request)
        self.assertEqual(rval, '[[0, "Please enter up to 10 suffix letters (but no wildcards!)"]]')

    def test_prefixAndSuffix(self):
        """Confirm that specifying prefix and suffix..."""
        request = test_web.DummyRequest([''])
        request.args["letters"] = ["ba"]
        request.args["prefix_letters"] = ["foo"]
        request.args["suffix_letters"] = ["r"]
        rval = self.r.render(request)
        self.assertEqual(rval, '[[0, "Specify either suffix or prefix (not both)"]]')





