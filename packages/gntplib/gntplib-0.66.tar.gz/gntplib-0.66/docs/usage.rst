.. _usage:

Usage
=====

gntplib provides :class:`~gntplib.Publisher` to send notifications and
:class:`~gntplib.Subscriber` to send subscription requests.


Publish
-------

Here is a general usage::

    >>> publisher = Publisher('App', ['Event'])
    >>> publisher.register()
    >>> publisher.publish('Event', 'Title', 'Text')

This is constructed from the following 3 steps:

1. Create a publisher instance
2. Register the publisher instance to the GNTP server
3. Send a notification to the GNTP server

Create a Publisher Instance
~~~~~~~~~~~~~~~~~~~~~~~~~~~

    >>> publisher = Publisher('App', ['Event'])

First argument is the name of the application.
This name should be unique among the GNTP clients registered to the GNTP server.

Second argument is the list of the notification types which this publisher will
sent.  The item of the list is a string, a string-bool tuple or a
:class:`~gntplib.Event` instance.

The tuple is to define disabled notification type easily::

    >>> Publisher('App', ['Event A', ('Event B', False)])

Then enabled notification type ``Event A`` and disabled notification type
``Event B`` are registered.

To fully define the properties of the notification type,
use :class:`~gntplib.Event` instance.

Moreover, you can specify the address of the GNTP server and the timeout in
seconds with keyword arguments::

    >>> Publisher('App', ['Event'],
                  host='remote.example.org', port=30000, timeout=20)

The defaults are `host='localhost'`, `port=23053` and `timeout=10`.

Register the Publisher Instance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    >>> publisher.register()

Use :meth:`~gntplib.Publisher.register()` method.

Once the publisher is registered, you don't need to re-register the same
application name and notification types of it.

Send a Notification
~~~~~~~~~~~~~~~~~~~

    >>> publisher.publish('Event', 'Title', 'Text')

Use :meth:`~gntplib.Publisher.publish()` method.

First argument is the name of the notification.  This is one of the names of
the notification types which is defined at :class:`~gntplib.Publisher`
constructor's second argument.

Second argument is the title of the notification, and third argument is the
text of the notification.


Subscribe
---------

Here is a general usage::

    >>> id = uuid.uuid4().hex
    >>> subscriber = Subscriber(id, 'Subscriber', 'hub.example.org', 'secret')
    >>> subscriber.subscribe()

:class:`~gntplib.Subscriber` requires four positional arguments: `id_` as
a subscriber id, `name` as a subscriber name, `hub` as a subscribed-to machine
address, `password` as a password.

The port numbers of the subscriber and subscribed-to machine are used default
port number: `23053`.  To change the port number of the subscriber, set `port`
keyword argument to the desired port number.  To change the port number of the
subscribed-to machine, set `hub` to host-port tuple instead of host string.

``SUBSCRIBE`` request is sent by :meth:`~gntplib.Subscriber.subscribe()`.
:meth:`~gntplib.Subscriber.subscribe()` accepts `callback` keyword argument
as a final callback like the methods of :class:`gntplib.Publisher`.
If you don't set `callback` keyword argument,
:meth:`~gntplib.Subscriber.store_ttl()` is used as a final callback,
and :class:`gntplib.Subscriber`\'s :attr:`ttl` attribute is updated by
the value of ``'Subscription-TTL'`` header of the response from the
subscribed-to machine.

And you can also use convenience function :func:`~gntplib.subscribe()`::

    >>> ttl = subscribe(id, 'Subscriber', 'hub.example.org', 'secret')


Icon
----

In GNTP, you can use icons in the following scenes.

* as icon of the application -
  ``icon`` keyword argument of :class:`~gntplib.Publisher`
* as default icon of the notification -
  ``icon`` keyword argument of :class:`~gntplib.Event`
* as icon of the notification -
  ``icon`` keyword argument of :meth:`~gntplib.Publisher.publish()`

The data type of the icon is <url> or <uniqueid>.
gntplib supports both data types in the same way::

    >>> icon1 = 'http://growl.googlecode.com/hg/Core/Resources/About.png'
    >>> icon2 = Resource(open('notification.png', 'rb').read())
    >>> publisher = Publisher('App', ['Icon Event'], icon=icon1)
    >>> publisher.register()
    >>> publisher.publish('Icon Event', 'Title', icon=icon2)

To use <url> data type, pass url string to ``icon`` keyword argument.  To use
<uniqueid> data type, pass a :class:`~gntplib.Resource` instance to ``icon``
keyword argument.  In the above example, ``icon1`` is of <url> data type, and
``icon2`` is of <uniqueid> data type.


Callback
--------

In GNTP, you can define the notification window's callback.  URL callbacks are
on click callbacks, which the GNTP server handles their events.  Socket
callbacks are on click, on close and/or on timeout callbacks, which the GNTP
client handles their events.

gntplib supports both callbacks in the same way::

    >>> publisher.publish('Callback Event', 'Click me!',
    ...                   gntp_callback='http://google.com')

or

    >>> import webbrowser
    >>> class MyCallback(SocketCallback):
    ...     def __init__(self, url):
    ...         SocketCallback.__init__(self, url)
    ...     def on_click(self, response):
    ...         webbrowser.open_new_tab(self.context)
    >>> publisher.publish('Callback Event', 'Click me!',
    ...                   gntp_callback=MyCallback('http://google.com'))


To use url callback, pass url string to ``gntp_callback`` keyword argument.
To use socket callback, pass :class:`~gntplib.SocketCallback` instance to
``gntp_callback`` keyword argument.

For socket callback, gntplib provides more ease-of-use keyword arguments:
``context``, ``context_type``, ``on_click``, ``on_close`` and ``on_timeout``.
And the following is same as above::

    >>> def on_click(response):
    ...     webbrowser.open_new_tab('http://google.com')
    >>> publisher.publish('Callback Event', 'Click me!', on_click=on_click)

You cannot use ``gntp_callback`` keyword argument with other socket callback's
keyword arguments.

.. note:: Socket callback blocks the client thread until the notification
          window is dismissed by the user, so it is usually used on thread
          pool, and so on.  Or use :mod:`gntplib.async` module, which supports
          asynchronous proccessing built on Tornado.


Security
--------

Password
~~~~~~~~

.. module:: gntplib.keys

You can set `password` keyword argument of :class:`~gntplib.Publisher` to
password string::

    >>> Publisher('App', ['Event'], password='secret')

gntplib use SHA256 as default hashing algorithm.
To change the hashing algorithm, set `key_hashing` keyword argument to
`keys.MD5`, `keys.SHA1` or `keys.SHA512`::

    >>> Publisher('App', ['Event'], password='secret', key_hashing=keys.MD5)

`password` is a required positional argument for :class:`~gntplib.Subscriber`
as described above.  :class:`~gntplib.Subscriber` can also accepts
`key_hashing` keyword argument.

Encryption
~~~~~~~~~~

.. module:: gntplib.ciphers

You can set `encryption` keyword argument of :class:`~gntplib.Publisher` and
:class:`~gntplib.Subscriber` to encryption algorithm.  Available encryption
algorithms are `ciphers.AES`, `ciphers.DES` and `ciphers.DES3`.  To enable
encryption, setting `password` argument is required.  If `password` argument is
set to `None`, `encryption` keyword argument will be ignored::

    >>> Publisher('App', ['Event'], password='secret', encryption=ciphers.AES)

The key size of `key_hashing` must be at least the key size of `encryption`.
So `keys.MD5` and `keys.SHA1` cannot be used with `ciphers.AES` or
`ciphers.DES3`.

.. note:: The encryption of messages is not implemented in Growl 1.3.3.


Additional Headers
------------------

To include custom headers or app-specific headers, pass the list of key-value
tuples to `custom_headers` or `app_specific_headers` keyword arguments of
:class:`~gntplib.Publisher` and :class:`~gntplib.Subscriber`::

    >>> publisher = Publisher('App', ['Event'],
    ...                       custom_headers=[('Sender', 'gntplib')],
    ...                       app_specific_headers=[('Filename', 'file.txt')])

If you want to change them each request, modify their attributes directly
before dispatching requests::

    >>> publisher.app_specific_headers = [('Filename', 'foo.txt')]
    >>> publisher.register()
    >>> publisher.app_specific_headers = [('Filename', 'bar.txt')]
    >>> publisher.publish('Event', 'Title')

You can also pass binary contents with :class:`~gntplib.Resource`::

    >>> resource = Resource(open('manual.pdf', 'rb').read())
    >>> publisher.app_specific_headers = [('resource', resource)]
