from .. import Request

from testtools import TestCase
from testtools.matchers import raises


class RequestTests(TestCase):
    def test_header_types(self):
        """
        Header keys and values must be bytes, not unicode.
        """
        self.assertThat(
            lambda: Request(method='get', url='http://google.com/',
                            headers={u'foo': b'bar'}),
            raises(TypeError("headers key {0!r} is not bytes".format(u'foo')))
            )
        self.assertThat(
            lambda: Request(method='get', url='http://google.com/',
                            headers={b'foo': u'bar'}),
            raises(TypeError("headers value {0!r} is not bytes".format(u'bar')))
            )
