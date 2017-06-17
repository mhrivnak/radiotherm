Introduction
============

This is a library for communicating with a wifi-enabled home thermostat made by
`Radio Thermostat Company of America <http://radiothermostat.com>`_. At the
time of writing, this includes the CT30, CT80, and the `Filtrete 3M50
<http://www.radiothermostat.com/filtrete/products/3M-50/>`_, which is made by
Radio Thermostat but rebranded and sold at Home Depot in the US.

Radio Thermostat Company of America was not involved in the creation of this
software and has not sanctioned or endorsed it in any way.

License
=======

This software is available under a BSD-style license. Please see LICENSE.txt.

Author
======
Michael Hrivnak <mhrivnak@hrivnak.org> is a professional software engineer who
is passionate about open source software and reducing energy consumption.

Features
========

- *Auto-Discovery* Your thermostat can be automatically detected, so there is
  no need to enter an IP address or domain name.
- *Comprehensive* Nearly every documented feature that works is implemented in
  this library.
- *Python 3 Support* This works in all Python versions from 2.6 up.
- *Tested* There is good test coverage using true unit tests.

Usage
=====

Getting Started
---------------

Import the library, and away we go.

    >>> import radiotherm
    >>> tstat = radiotherm.get_thermostat('192.168.0.2')
    >>> tstat.temp
    {'raw': 72.5}

If you have only one thermostat on your network, you can do auto-discovery by
omitting the address.

    >>> tstat = radiotherm.get_thermostat()

Human-Readable Values
---------------------

The value from the thermostat is always returned under the key 'raw'. For
fields that support human-readable values, there will be a key 'human'.

    >>> tstat.tmode
    {'raw': 2, 'human': 'Cool'}

API
===

The library centers around the Thermostat class, whose attributes are closely
related to the attributes defined in Radio Thermostat's API doccumentation. For
example, /tstat/temp in this case maps to the "temp" attribute on your
Thermostat instance.

Device Versions
---------------

Supported models:

- CT30 v1.75
- CT30 v1.92
- CT30 v1.94
- CT30 v1.99
- CT50 V1.09
- CT50 V1.88
- CT50 V1.92
- CT50 V1.94
- CT80 Rev B2 V1.03
- CT80 Rev B2 V1.09

Since I only have access to the 3M50 (which reports its model as "CT50 V1.94"),
that is the model that most development has occured with. Do you have another
model? Let me know, and let's collaborate to get it supported!

New models can be supported easily by subclassing either the CT30 or CT80
classes, depending on the thermostat model. Most of the API should work on all
devices, but there are apparently some differences that will need to be
accounted for. Long-term, I expect for those common features to be implemented
on CommonThermostat, while device-specific deviations will be implemented on
subclasses, such as the CT50v194 class.

Supported Features
------------------

Many of the features documented in the manufacturer's API reference do not seem
to work. For example, /tstat/save_energy seems to be broken. This library
should not implement those broken features.

Also, there are some features, like humidity control, that are only available
on specific devices.

Isn't there already a python library?
=====================================

Yes! Many thanks to Paul Jenning for creating `Python-TStat
<https://github.com/pjennings/Python-TStat>`_. The existance of his library was
a substantial motivation for me to buy this device.

Why create a new library?
-------------------------

I quickly identified some areas of Python-TStat that I wanted to improve. That
led me to realize that there were conceptual differences between that library
and my idea of what I wanted to use in my own projects.

- *Thin wrapper*. I want API libraries to be thin. Python-TStat does automatic
  result caching by default, which I personally don't want.
- *PEP-8*. I think it's important, and it would have taken a lot of work to
  make Python-TStat compliant.
- *Testing*. It's important to me that code be tested, and Python-TStat had no
  tests. Proper unit-testing is much easier to do when the code was written
  from the beginning with it in mind, so that made it more convenient to start
  over.
- *Simplicity*. My approach to defining the API in python is inspired by
  Django's model API, and I think it's resulted in easy-to-use and easy-to-read
  code.
- *Less Code*. I've implemented a feature set very similar to that of
  Python-TStat (minus caching). Not counting comments, doc blocks or blank
  lines, this library (at the time of initial release) has 201 lines of code,
  whereas Python-TStat has 349.
- *Python 3 Support*. This is also important to me. This library supports all
  python versions from 2.6 up.

All of that said, Python-TStat is a good library that works well. I just
decided that the quickest way for me to achieve the above goals was to start
from scratch, which was relatively painless since the device's API isn't very
complicated or large.

Release Notes
=============

1.3
---

Several models were added with thanks to the corresponding contributors!

CT30 v1.75 - Albert Lee
CT30 V1.94 - billy1
CT30 v1.99 - Adam Fazzari
CT50 V1.92 - mdingman
CT80 Rev B2 V1.09 - Steve Bauer

Thanks also to Albert Lee for adding remote temperature support, energy LED
support, plus support for the "lock_mode" and "simple_mode".

1.2
---

Thanks to a contribution from Nick Pegg, the CT80 Rev B2 V1.03 is now supported.

Support for `Travis CI <http://travis-ci.org>`_ was added, so all pushes to
the GitHub repository are automatically tested with multiple python versions.

1.1
---

Thanks to community contributions, this library now supports the CT50 V1.09 and
CT50 V1.88. No changes were made except to certify that all functionality works
with these models, and add a new subclass for each.

1.0
---

Initial release! This supports only the CT50 V1.94
