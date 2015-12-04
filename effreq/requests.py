from .intent import Response


@inlineCallbacks
def perform_with_treq(requests, request):
    """
    """
    response = requests.request(request.method.upper(),
                                request.url,
                                headers=request.headers,
                                data=request.data)
    content = yield treq.content(response)
    returnValue(Response(content=content,
                         code=response.code,
                         headers=response.headers))
