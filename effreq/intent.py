"""
The intent (in Effect parlance) and attendant objects.
"""


from characteristic import attributes, Attribute
from urlobject import URLObject


# TODO: an option for not fetching the content immediately, like requests'
# "stream"?

@attributes(
    [
        Attribute('method'),
        Attribute('url'),
        Attribute('headers', default_value=None),
        Attribute('data', default_value=None),
        Attribute('timeout', default_value=None),
    ],
    apply_immutable=True)
class Request(object):
    """
    An intent for performing HTTP requests.

    This is intended to be passed to Effect, as in:

        eff = Effect(Request(...)).on(success=got_response)

    The effect results an instance of :class:`Response`.
    """
    def __init__(self):
        """
        Initialize the Request. All parameters are set as public attributes
        with the same name.

        :param str method: (or bytes) the method to use
        :param str url: (or bytes) the URL to fetch. This can have non-ASCII
            characters, and they will be interpreted as an IRI.
        :param dict headers: the headers to send with the request.
            keys and values must be bytes.
        :param bytes data: the request body to send
        :param int timeout: time to way before giving up. None means
            no timeout
        """
        self.url = URLObject.from_iri(self.url)
        if self.headers is not None:
            for k,v in self.headers.items():
                if type(k) is not bytes:
                    raise TypeError("headers key {key!r} is not bytes".format(key=k))
                elif type(v) is not bytes:
                    raise TypeError("headers value {value!r} is not bytes".format(value=v))



@attributes(
    [
        Attribute('content', exclude_from_repr=True),
        Attribute('code'),
        Attribute('headers'),
    ])
class Response(object):
    """A response."""

    def __init__(self):
        """
        Initialize the Response. All parameters are set as public attributes
        with the same name.

        :param content: (bytes): the response body
        :param code: (int): the HTTP response code
        :param headers: (dict): HTTP response headers. Keys are bytes,
            values are lists of bytes
        """