# -*- coding: utf-8 -*-
from os import path

from setuptools import find_packages, setup

import migrate_metadata

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README.md')) as f:
    long_description = f.read()


setup(
    name='migrate-metadata',
    packages=find_packages('migrate_metadata'),
    version=migrate_metadata.__version__,
    include_package_data=True,
    zip_safe=False,
    long_description=long_description,
    long_description_content_type='text/markdown',
    description='Tool for migrating CKAN dataset metadata to metastore-lib',
    author='Datopian / Viderum Inc.',
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
    entry_points='''
        [console_scripts]
        metastore-import-ckan=migrate_metadata.migrator:main
    ''',
    install_requires=[
        'click',
        'six',
        'requests',
        'ckan_datapackage_tools',
        'metastore-lib',
    ],
)
