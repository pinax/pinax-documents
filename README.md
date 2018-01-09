![](http://pinaxproject.com/pinax-design/patches/pinax-documents.svg)

# Pinax Documents

[![](https://img.shields.io/pypi/v/pinax-documents.svg)](https://pypi.python.org/pypi/pinax-documents/)

[![CircleCi](https://img.shields.io/circleci/project/github/pinax/pinax-documents.svg)](https://circleci.com/gh/pinax/pinax-documents)
[![Codecov](https://img.shields.io/codecov/c/github/pinax/pinax-documents.svg)](https://codecov.io/gh/pinax/pinax-documents)
[![](https://img.shields.io/github/contributors/pinax/pinax-documents.svg)](https://github.com/pinax/pinax-documents/graphs/contributors)
[![](https://img.shields.io/github/issues-pr/pinax/pinax-documents.svg)](https://github.com/pinax/pinax-documents/pulls)
[![](https://img.shields.io/github/issues-pr-closed/pinax/pinax-documents.svg)](https://github.com/pinax/pinax-documents/pulls?q=is%3Apr+is%3Aclosed)

[![](http://slack.pinaxproject.com/badge.svg)](http://slack.pinaxproject.com/)
[![](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

## Table of Contents

* [About Pinax](#about-pinax)
* [Overview](#overview)
  * [Supported Django and Python versions](#supported-django-and-python-versions)
* [Documentation](#documentation)
  * [Installation](#installation)
  * [Usage](#usage)
  * [Template Tags](#template-tags)
  * [Hookset Methods](#hookset-methods)
  * [Settings](#settings)
* [Change Log](#change-log)
* [Contribute](#contribute)
* [Code of Conduct](#code-of-conduct)
* [Connect with Pinax](#connect-with-pinax)
* [License](#license)

## About Pinax

Pinax is an open-source platform built on the Django Web Framework. It is an ecosystem of reusable
Django apps, themes, and starter project templates. This collection can be found at http://pinaxproject.com.

## pinax-documents

### Overview

`pinax-documents` is a well tested, documented, and proven document management app for collecting and sharing documents in folders.

#### Supported Django and Python versions

Django \ Python | 2.7 | 3.4 | 3.5 | 3.6
--------------- | --- | --- | --- | ---
1.11 |  *  |  *  |  *  |  *  
2.0  |     |  *  |  *  |  *


## Documentation

### Installation

To install pinax-documents:

    pip install pinax-documents

Add `pinax.documents` to your `INSTALLED_APPS` setting:

    INSTALLED_APPS = (
        # other apps
        "pinax.documents",
    )

Add `pinax.documents.urls` to your project urlpatterns:

    urlpatterns = [
        # other urls
        url(r"^docs/", include("pinax.documents.urls", namespace="pinax_documents")),
    ]
    
### Usage


### Template Tags

`{% load pinax_documents_tags %}`

#### Filters

##### can_share

Returns True if `member` can share with `user`:

    {{ member|can_share:user }}

##### readable_bytes

Display number of bytes using appropriate units.

    {{ 73741824|readable_bytes }}

yields "70MB".


### Hookset Methods

#### `already_exists_validation_message(name, folder)`

String used to indicate a document with `name`
already exists in `folder`.

#### `can_share_folder(self, user, folder)`

Return True if `user` can share `folder`.

#### `document_created_message(self, request, document)`

Success message when document is created.

#### `document_deleted_message(self, request, document)`

Success message when a document is deleted.

#### `file_upload_to(self, instance, filename)`

Callable passed to the FileField's `upload_to kwarg` on Document.file

#### `folder_created_message(self, request, folder)`

Success message when folder is created.

#### `folder_deleted_message(self, request, folder)`

Success message when a folder is deleted.

#### `folder_pre_delete(self, request, folder)`

Perform folder operations prior to deletions. For example, deleting all contents.

#### `folder_shared_message(self, request, user, folder)`

Success message when a folder is shared.

#### `folder_unshared_message(self, request, user, folder)`

Success message when a folder is unshared.

#### `share_with_options(self, user, folder)`

Return a list of users with whom `user` can share `folder`.

#### `storage_color(self, user_storage)`

Returns a label indicating amount of storage used.

* "success" - sixty percent or more available
* "warning" - forty percent or less storage remaining
* "danger" - ten percent or less storage remaining


### Settings

#### PINAX_DOCUMENTS_HOOKSET

Used to provide your own custom hookset methods, as described above. Value is a dotted path to
your own hookset class:

`PINAX_DOCUMENTS_HOOKSET = "myapp.hooks.DocumentsHookSet"`



## Change Log

### 1.0.0

* Standardize documentation layout
* Drop Django v1.8, v1.10 support
* Replace _clone with _chain to fix unexpected keyword argument 'user' error
* Add hookset documentation

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

#### Contributors

* [Graham Ullrich](https://github.com/grahamu)
* [Ethan A Kent](https://github.com/ethankent)
* [Patrick Altman](https://github.com/paltman)

#### Changes

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


## Contribute

For an overview on how contributing to Pinax works read this [blog post](http://blog.pinaxproject.com/2016/02/26/recap-february-pinax-hangout/)
and watch the included video, or read our [How to Contribute](http://pinaxproject.com/pinax/how_to_contribute/) section.
For concrete contribution ideas, please see our
[Ways to Contribute/What We Need Help With](http://pinaxproject.com/pinax/ways_to_contribute/) section.

In case of any questions we recommend you join our [Pinax Slack team](http://slack.pinaxproject.com)
and ping us there instead of creating an issue on GitHub. Creating issues on GitHub is of course
also valid but we are usually able to help you faster if you ping us in Slack.

We also highly recommend reading our blog post on [Open Source and Self-Care](http://blog.pinaxproject.com/2016/01/19/open-source-and-self-care/).


## Code of Conduct

In order to foster a kind, inclusive, and harassment-free community, the Pinax Project
has a [code of conduct](http://pinaxproject.com/pinax/code_of_conduct/).
We ask you to treat everyone as a smart human programmer that shares an interest in Python, Django, and Pinax with you.


## Connect with Pinax

For updates and news regarding the Pinax Project, please follow us on Twitter [@pinaxproject](https://twitter.com/pinaxproject)
and check out our [Pinax Project blog](http://blog.pinaxproject.com).


## License

Copyright (c) 2012-2018 James Tauber and contributors under the [MIT license](https://opensource.org/licenses/MIT).
