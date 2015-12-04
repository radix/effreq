effreq
======

.. image:: https://travis-ci.org/radix/effreq.svg?branch=master
    :target: https://travis-ci.org/radix/effreq

``effreq`` is a purely functional HTTP client library, using the
`Effect`_ library to isolate the purely functional part from the
side-effecting part.

.. _`Effect`: https://warehouse.python.org/project/effect/


You use effreq like this:

.. code:: python

    from effect import sync_perform
    from effreq.intent import Request

    eff = Effect(Request(method='get', url='http://google.com/'))
    eff = eff.on(success=lambda response: print(response.code,
                                                response.headers,
                                                response.content))
    sync_perform(eff) # or effect.twisted.perform(eff)


IO Backends
===========

Because effreq uses the Effect library, you can use it in normal blocking code,
Twisted-using code, and so on. Currently the following IO backends are supported:

- `Twisted`_, via `treq`_
- `requests`_
.. _`Twisted`: https://twistedmatrix.com/
.. _`treq`: https://github.com/dreid/treq/

More to come!


Unicode support
===============

``effreq`` makes use of the URLObject library to parse addresses as IRIs, so
you can use non-ASCII unicode in both domains and other parts of a network
address.

Status: Alpha
=============

Right now ``effreq`` is in alpha, and is likely to change incompatibly. Once it's
being used in production, I'll release a final version.

Thanks
======

Thanks to Rackspace for allowing me to work on this project, and having an
*excellent* `open source employee contribution policy`_

.. _`open source employee contribution policy`: https://www.rackspace.com/blog/rackspaces-policy-on-contributing-to-open-source/


License
=======

Effect is licensed under the MIT license:

Copyright (C) 2014 Christopher Armstrong

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
