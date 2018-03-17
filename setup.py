import os
import sys
from setuptools import find_packages, setup

VERSION = "1.0.2"
LONG_DESCRIPTION = """
.. image:: http://pinaxproject.com/pinax-design/patches/pinax-documents.svg
    :target: https://pypi.python.org/pypi/pinax-documents/

===============
Pinax Documents
===============

.. image:: https://img.shields.io/pypi/v/pinax-documents.svg
    :target: https://pypi.python.org/pypi/pinax-documents/

\ 

.. image:: https://img.shields.io/circleci/project/github/pinax/pinax-documents.svg
    :target: https://circleci.com/gh/pinax/pinax-documents
.. image:: https://img.shields.io/codecov/c/github/pinax/pinax-documents.svg
    :target: https://codecov.io/gh/pinax/pinax-documents
.. image:: https://img.shields.io/github/contributors/pinax/pinax-documents.svg
    :target: https://github.com/pinax/pinax-documents/graphs/contributors
.. image:: https://img.shields.io/github/issues-pr/pinax/pinax-documents.svg
    :target: https://github.com/pinax/pinax-documents/pulls
.. image:: https://img.shields.io/github/issues-pr-closed/pinax/pinax-documents.svg
    :target: https://github.com/pinax/pinax-documents/pulls?q=is%3Apr+is%3Aclosed

\ 

.. image:: http://slack.pinaxproject.com/badge.svg
    :target: http://slack.pinaxproject.com/
.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target: https://opensource.org/licenses/MIT/

\ 

``pinax-documents`` is a document management app, collecting and sharing documents in folders.
 
Supported Django and Python Versions
------------------------------------

+-----------------+-----+-----+-----+-----+
| Django / Python | 2.7 | 3.4 | 3.5 | 3.6 |
+=================+=====+=====+=====+=====+
|  1.11           |  *  |  *  |  *  |  *  |
+-----------------+-----+-----+-----+-----+
|  2.0            |     |  *  |  *  |  *  |
+-----------------+-----+-----+-----+-----+
"""


# Publish Helper.
if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist bdist_wheel upload')
    sys.exit()


setup(
    author="Pinax Team",
    author_email="team@pinaxprojects.com",
    description="a document management app for Django",
    name="pinax-documents",
    long_description=LONG_DESCRIPTION,
    version=VERSION,
    url="http://github.com/pinax/pinax-documents/",
    license="MIT",
    packages=find_packages(),
    package_data={
        "documents": []
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=[
        "django>=1.11",
        "django-appconf>=1.0.2"
    ],
    tests_require=[
        "dj-inmemorystorage>=1.4.0",
        "django-bootstrap-form>=3.0.0",
        "django-test-plus>=1.0.22",
        "mock>=2.0.0",
        "pinax-templates>=2.0.0",
    ],
    test_suite="runtests.runtests",
    zip_safe=False
)
