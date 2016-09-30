Representing Constructible Numbers in Python
============================================
Build Status: [![Build Status](https://travis-ci.org/leovt/constructible.svg?branch=master)](https://travis-ci.org/leovt/constructible)

The constructible module provides exact representation of 
[constructible numbers](http://en.wikipedia.org/wiki/Constructible_number) in Python.

Python 2 and Python 3 are supported.


The constructible numbers are the smallest field containing the rational numbers, where the square root of
any non-negative constructible number is constructible as well. The non-negative constructible numbers are 
the lengths which can be constructed from the unit length using only a compass and a straightedge.

Usage
-----
Usually the `sqrt` function is enough to work with constructible numbers:

    >>> from constructible import sqrt
    >>> x = sqrt(2) + sqrt(3)
    >>> print(x)
    ((0 + 1 * sqrt(2)) + (1 + 0 * sqrt(2)) * sqrt((3 + 0 * sqrt(2))))
    >>> y = x*x
    >>> print(y)
    ((5 + 0 * sqrt(2)) + (0 + 2 * sqrt(2)) * sqrt((3 + 0 * sqrt(2))))
    >>> z = y*y
    >>> t = 10*y - z
    >>> t == 1
    True
    
Installation
------------
To install from PYPI just type

    pip install constructible

The library is a single pure python file, so it is also easy to install by hand.

Testing
-------
There are some tests using `untittest`. Thanks to [Travis-CI](https://travis-ci.org/) each push to github triggers a test: 
[![Build Status](https://travis-ci.org/leovt/constructible.svg?branch=master)](https://travis-ci.org/leovt/constructible)

Realeasing on PYPI
------------------
The following steps are needed:

* Update the version in setup.py
* Tag the version in git
    `git tag 0.1 -m "Adds a tag so that we can put this on PyPI."`
    `git push --tags origin`
* Test release with 
    `python setup.py register -r pypitest`
    `python setup.py sdist upload -r pypitest`
* Productive release with
    `python setup.py register -r pypi`
    `python setup.py sdist upload -r pypi`

Changelog
---------

* 2016-05-23 V0.1 Initial Release
* 2016-09-30 V0.2 Fixing Issue 1 and added Tests
