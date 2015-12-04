# coding: utf-8

import json

from ..intent import Request, Response
from ..treq import perform_with_treq

from testtools import TestCase

from twisted.internet.defer import succeed
from twisted.trial.unittest import SynchronousTestCase


class TreqTests(SynchronousTestCase):
    """
    Tests for the treq performer.
    """
    def test_perform(self):
        """
        The Request effect dispatches a request to treq, and returns a
        Response with all data populated.
        """
        reactor = object()
        expected_req = ('GET',
                        'http://google.com/',
                        {'reactor': reactor,
                         'headers': None,
                         'data': None})
        response = Response(content='content', code=200, headers={})
        treq = StubTreq(reqs=[(expected_req, response)],
                        contents=[(response, "content")])
        req = Request(method="get", url="http://google.com/")
        self.assertEqual(
            self.successResultOf(perform_with_treq(treq, reactor, req)),
            response)

    def test_idna(self):
        """
        IDNA is supported, despite treq's lack of support. The IDNA-encoded
        URL is passed to treq as bytes.
        """
        reactor = object()
        expected_req = ('GET',
                        'http://xn--wxa.com/',
                        {'reactor': reactor,
                         'headers': None,
                         'data': None})
        response = Response(content='content', code=200, headers={})
        treq = StubTreq(reqs=[(expected_req, response)],
                        contents=[(response, "content")])
        req = Request(method="get", url=u'http://λ.com/')
        self.assertEqual(
            self.successResultOf(perform_with_treq(treq, reactor, req)),
            response)

    def test_unicode_paths(self):
        """
        Unicode paths are supported, despite treq's lack of support. The
        UTF8-then-URL-quoted ascii bytes are passed to treq.
        """
        reactor = object()
        expected_req = ('GET',
                        'http://lambda.com/%CE%BB',
                        {'reactor': reactor,
                         'headers': None,
                         'data': None})
        response = Response(content='content', code=200, headers={})
        treq = StubTreq(reqs=[(expected_req, response)],
                        contents=[(response, "content")])
        req = Request(method="get", url=u'http://lambda.com/λ')
        self.assertEqual(
            self.successResultOf(perform_with_treq(treq, reactor, req)),
            response)

    def test_unicode_queries(self):
        """
        Unicode paths are supported, despite treq's lack of support. The
        UTF8-then-URL-quoted ascii bytes are passed to treq.
        """
        reactor = object()
        expected_req = ('GET',
                        'http://lambda.com/%CE%BB?k%CE%BB=v%CE%BB',
                        {'reactor': reactor,
                         'headers': None,
                         'data': None})
        response = Response(content='content', code=200, headers={})
        treq = StubTreq(reqs=[(expected_req, response)],
                        contents=[(response, "content")])
        # Agh we're escaping =
        req = Request(method="get", url=u'http://lambda.com/lambda?kλ=vλ')
        self.assertEqual(
            self.successResultOf(perform_with_treq(treq, reactor, req)),
            response)

class StubTreq(object):
    """
    A stub version of otter.utils.logging_treq that returns canned responses
    from dictionaries.
    """
    def __init__(self, reqs=None, contents=None):
        """
        :param reqs: A dictionary specifying the values that the `request`
            method should return. Keys are tuples of:
            (method, url, headers, data, (<other key names>)).
            Since headers is usually passed as a dict, here it should be
            specified as a tuple of two-tuples in sorted order.

        :param contents: A dictionary specifying the values that the `content`
            method should return. Keys should match up with the values of the
            `reqs` dict.
        """
        _check_unique_keys(reqs)
        _check_unique_keys(contents)
        self.reqs = reqs
        self.contents = contents

    def request(self, method, url, **kwargs):
        """
        Return a result by looking up the arguments in the `reqs` dict.
        The only kwargs we care about are 'headers' and 'data',
        although if other kwargs are passed their keys count as part of the
        request.

        'log' would also be a useful kwarg to check, but since dictionary keys
        should be immutable, and it's hard to get the exact instance of
        BoundLog, that's being ignored for now.
        """
        key = (method, url, kwargs)
        return succeed(alist_get(self.reqs, key))

    def content(self, response):
        """Return a result by looking up the response in the `contents` dict."""
        return succeed(alist_get(self.contents, response))

    def json_content(self, response):
        """Return :meth:`content` after json-decoding"""
        return self.content(response).addCallback(json.loads)


def _check_unique_keys(data):
    """Check that all the keys in an association list are unique."""
    # O(lol)
    for itemindex, item in enumerate(data):
        for itemagain in data[itemindex + 1:]:
            if item[0] == itemagain[0]:
                raise Exception("Duplicate items in EQDict: %r:%r and %r:%r"
                                % (item[0], item[1], itemagain[0], itemagain[1]))


def alist_get(data, key):
    """Look up a value in an association list."""
    for item in data:
        if item[0] == key:
            return item[1]
    raise KeyError(key)
