#!/usr/bin/env python

from setuptools import setup

setup(
        name='discogs',
        version='0.1',
        description='Python interface to the Discogs music information database.',
        author='Jeremy Cantrell',
        author_email='jmcantrell@gmail.com',
        classifiers=[
            'Development Status :: 4 - Beta',
            'Environment :: Console',
            'Intended Audience :: System Administrators',
            'License :: OSI Approved :: BSD License',
            'Natural Language :: English',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Topic :: Communications :: Email :: Email Clients (MUA)',
            'Topic :: System :: Systems Administration',
            'Topic :: Utilities',
            ],
        install_requires=[
            'ScriptUtils',
            ],
        py_modules=[
            'discogs',
            ],
        )
