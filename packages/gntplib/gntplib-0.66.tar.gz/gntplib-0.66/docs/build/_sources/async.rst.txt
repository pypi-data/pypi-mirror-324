.. _async:

Asynchronous Support
====================

.. module:: gntplib.async

:mod:`gntplib.async` provides support for asynchronous processing built on
Tornado_.

.. _Tornado: http://www.tornadoweb.org/

Publisher
~~~~~~~~~

:class:`~gntplib.async.AsyncPublisher` provides asynchronous methods:
:meth:`~gntplib.async.AsyncPublisher.register()` and
:meth:`~gntplib.async.AsyncPublisher.publish()`.
These methods are inherited from :class:`~gntplib.Publisher` directly.

Note that they are asynchronous methods especially when you use them in a row.
:meth:`~gntplib.async.AsyncPublisher.register()` returns regardless of wheather
the ``REGISTER`` request has been received by the GNTP server, so successive
:meth:`~gntplib.async.AsyncPublisher.publish()` method call is possible to fail
due to unregistered application or notification name.

To avoid this, pass :meth:`~gntplib.async.AsyncPublisher.publish()` method call
to ``callback`` keyword argument as callback function::

    >>> publisher = AsyncPublisher('App', ['Async Event'])
    >>> def my_callback(ignored):
    ...     publisher.publish('Async Event', 'Title')
    >>> publisher.register(callback=my_callback)

Or use Tornado's ``gen.Task`` syntax like this::

    >>> @gen.engine
    ... def async_publish():
    ...     publisher = AsyncPublisher('App', ['Async Event'])
    ...     yield gen.Task(publisher.register)
    ...     publisher.publish('Async Event', 'Title')


Subscriber
~~~~~~~~~~

:class:`~gntplib.async.AsyncSubscriber` provides asynchronous method
:meth:`~gntplib.async.AsyncSubscriber.subscribe()`, which is inherited
from :class:`~gntplib.Subscriber` directly.


Resource
~~~~~~~~

:class:`~gntplib.async.AsyncResource` is a lazy resource.
Before request dispatching, the resource data is fetched asynchronously
from the url passed to the constructor.

You can use :class:`~gntplib.async.AsyncResource` instead of
:class:`~gntplib.Resource` in :class:`~gntplib.async.AsyncPublisher`
or :class:`~gntplib.async.AsyncSubscriber`::

    >>> icon = AsyncResource('http://example.org/icon.png')
    >>> resource = AsyncResource('http://example.org/resource.pdf')
    >>> publisher = AsyncPublisher('App', ['Async Event'],
    ...                            custom_headers=[('resource', resource)])
    >>> publisher.publish('Async Event', 'Title', icon=icon)
