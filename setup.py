#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import io
import os
import re
import shutil
import sys

from setuptools import find_packages, setup, Command

here = os.path.abspath(os.path.dirname(__file__))


def get_readme():
    path = os.path.join(here, 'README.md')
    with io.open(path, encoding='utf-8') as f:
        return '\n' + f.read()


class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            shutil.rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPI via Twine…')
        os.system('twine upload dist/*')

        sys.exit()


def _read_about():
    """
    Read package metadata without importing `crossplane` (import has side effects).
    """
    about = {}
    init_py = os.path.join(here, "crossplane", "__init__.py")
    with io.open(init_py, encoding="utf-8") as f:
        contents = f.read()

    keys = ["__summary__", "__url__", "__version__", "__author__", "__email__", "__license__"]
    for key in keys:
        # NOTE: This must match normal Python assignment like:
        # __summary__ = '...'
        # Keep escapes minimal; raw strings already handle backslashes.
        m = re.search(
            r"^%s\s*=\s*['\"]([^'\"]+)['\"]\s*$" % re.escape(key),
            contents,
            re.M,
        )
        if not m:
            raise RuntimeError("Could not find %s in %s" % (key, init_py))
        about[key] = m.group(1)
    return about


ABOUT = _read_about()

setup(
    # PyPI distribution name (intentionally different from import name `crossplane`)
    name="ngxparse",
    version=ABOUT["__version__"],
    description=ABOUT["__summary__"],
    long_description=get_readme(),
    long_description_content_type='text/markdown',
    author=ABOUT["__author__"],
    author_email=ABOUT["__email__"],
    # Point users at this fork's repo (upstream URL is still available in history)
    url="https://github.com/dvershinin/crossplane",
    packages=find_packages(exclude=['tests','tests.*']),
    license=ABOUT["__license__"],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
    entry_points={
        'console_scripts': [
            'crossplane = crossplane.__main__:main'
        ],
    },
    cmdclass={'upload': UploadCommand}
)
