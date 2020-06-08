# -*- coding: utf-8 -*-

import os
import io
from setuptools import setup, find_packages


# Helpers
def read(*paths):
    """Read a text file."""
    basedir = os.path.dirname(__file__)
    fullpath = os.path.join(basedir, *paths)
    contents = io.open(fullpath, encoding='utf-8').read().strip()
    return contents


# Prepare
PACKAGE = 'migrate_metadata'
NAME = PACKAGE.replace('_', '-')
INSTALL_REQUIRES = [
    'ckan_datapackage_tools',
    'metastore-lib',
    'requests'
    ]

README = read('README.md')
PACKAGES = find_packages(exclude=['examples', 'tests'])


# Run
setup(
    name=NAME,
    packages=PACKAGES,
    include_package_data=True,
    install_requires=INSTALL_REQUIRES,
    zip_safe=False,
    long_description=README,
    description='{{ DESCRIPTION }}',
    author='Open Knowledge International',
    url='https://github.com/datopian/migrate-metadata',
    license='MIT',
    keywords=[
        'migrate',
        'metadata'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
