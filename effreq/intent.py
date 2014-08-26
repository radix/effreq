"""
The intent (in Effect parlance) and attendant objects.
"""


from characteristic import attributes, Attribute


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

    .. py:attribute:: method (str): the method to use
    .. py:attribute:: url (str): the URL to fetch
    .. py:attribute:: headers (dict): the headers to set on the request.
        keys are bytes and values are lists of bytes
    .. py:attribute:: data (bytes): the request body to send
    .. py:attribute:: timeout (int): time to way before giving up. None means
        no timeout
    """


@attributes(
    [
        Attribute('content'),
        Attribute('code'),
        Attribute('headers'),
    ])
class Response(object):
    """
    A response.

    .. py:attribute:: content (bytes): the response body
    .. py:attribute:: code (int): the HTTP response code
    .. py:attribute:: headers (dict): HTTP response headers. Keys are bytes,
        values are lists of bytes
    """
