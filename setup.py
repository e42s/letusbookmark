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
desc = "ebookme is a Web application that provides a bookmarklet to convert any web page to a .mobi file"
long_desc = read('README')


setup(
      name='ebookme',
      version=find_version('ebookme', '__init__.py'),
      author='Sylvain Prat',
      author_email='sylvain.prat+ebookme@gmail.com',
      description=desc,
      long_description=long_desc,
      license='MIT License',
      keywords='',
      url='http://bitbucket.org/sprat/ebookme',
      packages=find_packages(),
      include_package_data=True,
      package_data={'' : ['*.cfg']},
      zip_safe=False,
      install_requires=('nagare',),
      message_extractors={ 'ebook.me' : [('**.py', 'python', None)] },
      entry_points="""
      [nagare.applications]
      ebookme = ebookme.app:app
      """
     )

