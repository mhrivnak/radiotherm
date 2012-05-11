#!/usr/bin/env python

from distutils.core import setup
import os

readme_location = os.path.join(os.path.dirname(__file__), 'README.rst')

setup(name='radiotherm',
    version='1.0',
    description='client library for wifi thermostats sold by radiothermostat.com',
    long_description=open(readme_location).read(),
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
