.. _installation:

Installation
============

Simply use pip::

    $ pip install gntplib

There are the following **optional** prerequisites.

* ``pycrypto`` - to use :mod:`gntplib.ciphers` module for message encryption
* ``tornado`` - to use :mod:`gntplib.async` module for asynchronous processing

Let's send a simple notification to test installation.
Use :func:`gntplib.publish()`::

    >>> import gntplib
    >>> gntplib.publish('App', 'Event', 'Hello, Growl!')
