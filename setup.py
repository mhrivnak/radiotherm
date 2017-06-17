#!/usr/bin/env python

from distutils.core import setup

long_desc = open('README.rst').read()

setup(name='radiotherm',
    version='1.3',
    description='client library for wifi thermostats sold by radiothermostat.com',
    long_description=long_desc,
    packages=('radiotherm',),
    license='BSD',
    author='Michael Hrivnak',
    author_email='mhrivnak@hrivnak.org',
    url='https://github.com/mhrivnak/radiotherm',
    classifiers=(
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Topic :: Home Automation',
        'Topic :: Software Development :: Libraries',
    )
)
