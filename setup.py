from setuptools import find_packages, setup

LONG_DESCRIPTION = """
.. image:: http://pinaxproject.com/pinax-design/patches/pinax-documents.svg
    :target: https://pypi.python.org/pypi/pinax-documents/

=================
Pinax Documents
=================

.. image:: https://img.shields.io/pypi/v/pinax-documents.svg
    :target: https://pypi.python.org/pypi/pinax-documents/
.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target: https://pypi.python.org/pypi/pinax-documents/

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

.. image:: http://slack.pinaxproject.com/badge.svg
    :target: http://slack.pinaxproject.com/


``pinax-documents`` is a document management app, collecting and sharing documents in folders.


Supported Django and Python Versions
------------------------------------

* Django 1.8, 1.10, 1.11, and 2.0
* Python 2.7, 3.4, 3.5, and 3.6
"""

setup(
    author="Pinax Team",
    author_email="team@pinaxproject.com",
    description="a document management app for Django",
    name="pinax-documents",
    long_description=LONG_DESCRIPTION,
    version="0.6.0",
    url="http://github.com/pinax/pinax-documents/",
    license="MIT",
    packages=find_packages(),
    package_data={
        "documents": []
    },
    test_suite="runtests.runtests",
    tests_require=[
        "dj-inmemorystorage>=1.4.0",
        "django-appconf>=1.0.1",
        "django-test-plus>=1.0.11",
        "mock>=1.3.0",
        "django-user-accounts>=1.3.1",
        "pinax-theme-bootstrap>=7.6.0",
    ],
    install_requires=[
        "django-appconf>=1.0.1"
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.10',
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
    zip_safe=False,
)