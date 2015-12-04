import urllib
from urlparse import urlparse, urlunparse

from twisted.internet.defer import inlineCallbacks, returnValue

from .intent import Response


def idnify(url):
    """
    If the URL is unicode, return a URL with the hostname encoded to IDN, and
    the path and query args encoded to UTF-8 and quoted.
    """
    if isinstance(url, unicode):
        parsed_url = list(urlparse(url))
        parsed_url[1] = parsed_url[1].encode('idna')
        for i in range(2, 5):
            print i, parsed_url[i]
            parsed_url[i] = urllib.quote(parsed_url[i].encode('utf-8'),
                                         safe=';/?:@&=+$,')
        url = urlunparse(parsed_url)
        print url
        return url
    else:
        return url

@inlineCallbacks
def perform_with_treq(treq, reactor, request):
    """
    """
    method = request.method.upper().encode('ascii')
    response = yield treq.request(method,
                                  idnify(request.url),
                                  headers=request.headers,
                                  data=request.data,
                                  reactor=reactor)
    content = yield treq.content(response)
    returnValue(Response(content=content,
                         code=response.code,
                         headers=response.headers))
