#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

# Note: To use the 'upload' functionality of this file, you must:
#   $ pip install twine

import os
import sys

from shutil import rmtree
from codecs import open
from setuptools import find_packages, setup, Command

here = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(here, 'README.rst')
with open(path, encoding='utf-8') as f:
    readme = '\n' + f.read()


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
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPi via Twine…')
        os.system('twine upload dist/*')

        sys.exit()


setup(
    name='crossplane',
    version='0.1.0',
    description='Reliable and fast NGINX configuration file parser.',
    long_description=readme,
    author='Arie van Luttikhuizen',
    author_email='aluttik@gmail.com',
    url='https://github.com/nginxinc/crossplane',
    packages=find_packages(exclude=['tests']),
    license='Apache 2.0',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
    entry_points={
        'console_scripts': [
            'crossplane = crossplane.__main__:main'
        ],
    },
    cmdclass={
        'upload': UploadCommand  # setup.py publish support
    }
)
