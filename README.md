![](http://pinaxproject.com/pinax-design/patches/pinax-documents.svg)
    
# Pinax Documents

[![](https://img.shields.io/pypi/v/pinax-documents.svg)](https://pypi.python.org/pypi/pinax-documents/)
[![](https://img.shields.io/badge/license-MIT-blue.svg)](https://pypi.python.org/pypi/pinax-documents/)

[![CircleCi](https://img.shields.io/circleci/project/github/pinax/pinax-documents.svg)](https://circleci.com/gh/pinax/pinax-documents)
[![Codecov](https://img.shields.io/codecov/c/github/pinax/pinax-documents.svg)](https://codecov.io/gh/pinax/pinax-documents)
![](https://img.shields.io/github/contributors/pinax/pinax-documents.svg)
![](https://img.shields.io/github/issues-pr/pinax/pinax-documents.svg)
![](https://img.shields.io/github/issues-pr-closed/pinax/pinax-documents.svg)

[![](http://slack.pinaxproject.com/badge.svg)](http://slack.pinaxproject.com/)


## pinax-documents

`pinax-documents` is a well tested, documented, and proven document management app for collecting and sharing documents in folders.

### Supported Django and Python Versions

* Django 1.8, 1.10, 1.11, and 2.0
* Python 2.7, 3.4, 3.5, and 3.6


## Table of Contents

* [Installation](#installation)
* [Template tags](#template-tags)
* [Change Log](#change-log)
* [Pinax](#pinax)
* [Contribute](#contribute)
* [Contributors](#contributors)
* [Code of Conduct](#code-of-conduct)
* [Pinax Project Blog and Twitter](#pinax-project-blog-and-twitter)


## Installation

To install pinax-documents:

    pip install pinax-documents

Add `pinax.documents` to your `INSTALLED_APPS` setting:

    INSTALLED_APPS = (
        ...
        "pinax.documents",
        ...
    )

Add `pinax.documents.urls` to your project urlpatterns:

    urlpatterns = [
        ...
        url(r"^docs/", include("pinax.documents.urls", namespace="pinax_documents")),
        ...
    ]
    

## Template Tags

`{% load pinax_documents_tags %}`

### Filters

#### can_share

Returns True if `member` can share with `user`:

    {{ member|can_share:user }}

#### readable_bytes

Display number of bytes using appropriate units.

    {{ 73741824|readable_bytes }}

yields "70MB".


## Change Log

### 0.6.0

* Add Django 2.0 compatibility testing
* Drop Django 1.9 and Python 3.3 support
* Convert CI and coverage to CircleCi and CodeCov
* Add PyPi-compatible long description
* Move documentation to README.md

### 0.4.2

* Fix bug in document deletion where quota was not given back
* Made model strings for `Folder` and `Document` Python 3 compatible

### 0.4.1

* Updating documentation

### 0.4.0

* Moved template locations to be under `pinax/` [PR #9](https://github.com/pinax/pinax-documents/pull/9)
* Namespaced URLs [PR #10](https://github.com/pinax/pinax-documents/pull/10), [PR #16](https://github.com/pinax/pinax-documents/pull/16)
* Moved signal receiver to receivers.py [PR #11](https://github.com/pinax/pinax-documents/pull/11)
* Converted views to class based views [PR #12](https://github.com/pinax/pinax-documents/pull/12)
* Added hooksets [PR #15](https://github.com/pinax/pinax-documents/pull/15)
* Document deletion [PR #17](https://github.com/pinax/pinax-documents/pull/17)
* Folder deletion [PR #19](https://github.com/pinax/pinax-documents/pull/19)
* Disallow document name duplicates within same folder [PR #20](https://github.com/pinax/pinax-documents/pull/20)
* Disallow folder name duplicates within same parent [PR #20](https://github.com/pinax/pinax-documents/pull/20)

### 0.3.1

### 0.3.0

### 0.2.0

### 0.1


## Pinax

[Pinax](http://pinaxproject.com/pinax/) is an open-source platform built on the
Django Web Framework. It is an ecosystem of reusable Django apps, themes, and
starter project templates.

This app is part of the Pinax ecosystem and is designed for use both with and
independently of other Pinax apps.


## Contribute

See [this blog post](http://blog.pinaxproject.com/2016/02/26/recap-february-pinax-hangout/) including a video, or our [How to Contribute](http://pinaxproject.com/pinax/how_to_contribute/) section for an overview on how contributing to Pinax works. For concrete contribution ideas, please see our [Ways to Contribute/What We Need Help With](http://pinaxproject.com/pinax/ways_to_contribute/) section.

In case of any questions we recommend you [join our Pinax Slack team](http://slack.pinaxproject.com) and ping us there instead of creating an issue on GitHub. Creating issues on GitHub is of course also valid but we are usually able to help you faster if you ping us in Slack.

We also highly recommend reading our [Open Source and Self-Care blog post](http://blog.pinaxproject.com/2016/01/19/open-source-and-self-care/).


## Contributors

* [Graham Ullrich](https://github.com/grahamu)
* [Ethan A Kent](https://github.com/ethankent)
* [Patrick Altman](https://github.com/paltman)
* [Brian Rosner](https://github.com/brosner)
* [Anna Ossowski](https://github.com/ossanna16)
* [Thomas Schreiber](https://github.com/rizumu)
* [John Franey](https://github.com/johnfraney)
* [Katherine “Kati” Michel](https://github.com/KatherineMichel)


## Code of Conduct

In order to foster a kind, inclusive, and harassment-free community, the Pinax Project has a code of conduct, which can be found here http://pinaxproject.com/pinax/code_of_conduct/. We ask you to treat everyone as a smart human programmer that shares an interest in Python, Django, and Pinax with you.


## Pinax Project Blog and Twitter

For updates and news regarding the Pinax Project, please follow us on Twitter at @pinaxproject and check out our blog http://blog.pinaxproject.com.
