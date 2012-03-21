# -*- coding: UTF-8 -*-
# Copyright (c) 2012 Sylvain Prat. This program is open-source software,
# and may be redistributed under the terms of the MIT license. See the
# LICENSE file in this distribution for details.

import os
import re

from setuptools import setup, find_packages


def read(*path_parts):
    here = os.path.dirname(__file__)
    return open(os.path.join(here, *path_parts)).read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


# package description
desc = "Let Us Bookmark demonstrates how to create bookmarklets with Nagare."
long_desc = read('README')


setup(
    name='letusbookmark',
    version=find_version('letusbookmark', '__init__.py'),
    author='Sylvain Prat',
    author_email='sylvain.prat+letusbookmark@gmail.com',
    description=desc,
    long_description=long_desc,
    license='MIT License',
    keywords='',
    url='http://bitbucket.org/sprat/letusbookmark',
    packages=find_packages(),
    include_package_data=True,
    package_data={'': ['*.cfg']},
    zip_safe=False,
    install_requires=('nagare',),
    message_extractors={'letusbookmark': [('**.py', 'python', None)]},
    entry_points="""
    [nagare.applications]
    letusbookmark = letusbookmark.app:app
    """
)
