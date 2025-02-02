# kas - setup tool for bitbake based projects
#
# Copyright (c) Siemens AG, 2017-2019
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""
    Setup script for kas, a setup tool for bitbake based projects
"""

from os import path
from setuptools import setup, find_packages

from kas import __version__

__license__ = 'MIT'
__copyright__ = 'Copyright (c) Siemens AG, 2017-2019'

HERE = path.abspath(path.dirname(__file__))
with open(path.join(HERE, 'README.rst')) as f:
    LONG_DESCRIPTION = f.read()


setup(
    name='kas',
    version=__version__,

    scripts=['kas-container'],

    description='Setup tool for bitbake based projects',
    long_description=LONG_DESCRIPTION,

    maintainer='Jan Kiszka',
    maintainer_email='jan.kiszka@siemens.com',

    url='https://github.com/siemens/kas',
    download_url=('https://github.com/siemens/'
                  f'kas/archive/{__version__}.tar.gz'),

    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 5 - Production/Stable',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
    ],
    keywords='OpenEmbedded bitbake development',

    packages=find_packages(),

    package_data={'kas': ['*.json']},

    entry_points={
        'console_scripts': [
            'kas=kas.kas:main',
        ],
    },

    install_requires=[
        'PyYAML>=3.0,<7',
        'distro>=1.0.0,<2',
        'jsonschema>=2.5.0,<5',
        'kconfiglib>=14.1.0,<15',
        'GitPython>=3.1.0,<4',
        "cached-property>=1.0,<2; python_version<'3.8'"
    ],

    # At least python 3.6 is needed by now:
    python_requires='>=3.6',
)
