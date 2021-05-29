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
* [Important Links](#important-links)
* [Overview](#overview)
  * [Supported Django and Python Versions](#supported-django-and-python-versions)
* [Documentation](#documentation)
  * [Installation](#installation)
  * [Usage](#usage)
  * [Views](#views)
  * [Model Managers](#model-managers)
  * [Template Tags](#template-tags)
  * [Hookset Methods](#hookset-methods)
  * [Settings](#settings)
  * [Templates](#templates)
* [Change Log](#change-log)
* [Contribute](#contribute)
* [Code of Conduct](#code-of-conduct)
* [Connect with Pinax](#connect-with-pinax)
* [License](#license)


## About Pinax

Pinax is an open-source platform built on the Django Web Framework. It is an ecosystem of reusable Django apps, themes, and starter project templates. This collection can be found at http://pinaxproject.com.


## Important Links

Where you can find what you need:
* Releases: published to [PyPI](https://pypi.org/search/?q=pinax) or tagged in app repos in the [Pinax GitHub organization](https://github.com/pinax/)
* Global documentation: [Pinax documentation website](https://pinaxproject.com/pinax/)
* App specific documentation: app repos in the [Pinax GitHub organization](https://github.com/pinax/)
* Support information: [SUPPORT.md](https://github.com/pinax/.github/blob/master/SUPPORT.md) file in the [Pinax default community health file repo](https://github.com/pinax/.github/)
* Contributing information: [CONTRIBUTING.md](https://github.com/pinax/.github/blob/master/CONTRIBUTING.md) file in the [Pinax default community health file repo](https://github.com/pinax/.github/)
* Current and historical release docs: [Pinax Wiki](https://github.com/pinax/pinax/wiki/)


## pinax-documents

### Overview

`pinax-documents` is a well tested, documented, and proven document management app for collecting and sharing documents in folders.

#### Supported Django and Python Versions

Django / Python | 3.6 | 3.7 | 3.8 | 3.9
--------------- | --- | --- | --- | ---  
2.2  |  *  |  *  |  *  |  *   
3.1  |  *  |  *  |  *  |  *  
3.2  |  *  |  *  |  *  |  *  


## Documentation

### Installation

To install pinax-documents:

```shell
    $ pip install pinax-documents
```

Add `pinax.documents` to your `INSTALLED_APPS` setting:

```python
    INSTALLED_APPS = [
        # other apps
        "pinax.documents",
    ]
```

Add `pinax.documents.urls` to your project urlpatterns:

```python
    urlpatterns = [
        # other urls
        url(r"^docs/", include("pinax.documents.urls", namespace="pinax_documents")),
    ]
```

### Usage

### Views

Four views handle Document creation, detail, downloading, and deletion.
Four views handle Folder creation, detail, sharing, and deletion.
All views require an authenticated user but no special permission.

#### document_create

Validates form input to create a new Document. Optionally adds document
to a specified Folder. Specify a folder by adding `?f=5` URL kwarg
to the GET request, where `5` is the PK of the desired Folder.
Redirects to the document index view.

URL: `pinax_documents:document_create`

Template: `pinax/documents/document_create.html`

Form class: `pinax.forms.DocumentCreateForm`

#### document_detail

Shows document detail, if document is within the requesting user's scope.

URL: `pinax_documents:document_detail`

Template: `pinax/documents/document_detail.html`

#### document_download

Download a specified Document, if document is within requesting user's scope.

URL: `pinax_documents:document_download`

#### document_delete

Delete the specified Document.
Redirects to document index view.

URL: `pinax_documents:document_create`

Template: `pinax/documents/document_confirm_delete.html`

#### document_index

Show a list of Documents within user scope.
URL: `pinax_documents:document_index`

Template: `pinax/documents/index.html`

#### folder_create

Create a new Folder.

A folder can be created as a subfolder of an existing folder.
To create this relationship specify a parent folder by adding `?p=3` URL kwarg
to the GET request, where `3` is the PK of the desired "parent" folder.

URL: `pinax_documents:folder_create`

Template: `pinax/documents/folder_create.html`

Form class: `pinax.forms.FolderCreateForm`

#### folder_detail

Shows folder detail, including all documents within the requesting user's scope.

URL: `pinax_documents:folder_detail`

Template: `pinax/documents/folder_detail.html`

Detail view context variables:

##### `members`

User members of the folder.

##### `can_share`

True if user can share the folder.

#### folder_share

Share a folder with another user.

URL: `pinax_documents:folder_share`

Template: `pinax/documents/folder_share.html`

#### folder_delete

Delete the specified Folder.
Redirects to document index view.

URL: `pinax_documents:folder_delete`

Template: `pinax/documents/folder_confirm_delete.html`

### Model Managers

#### `Folder.members(folder, **kwargs)`

#### `Folder.objects.for_user(user)`

Returns all Folders a user can do something with. Chainable query method.

#### `Document.objects.for_user(user)`

Returns all Documents a user can do something with. Chainable query method.

### Template Tags

```django
{% load pinax_documents_tags %}
```

#### Filters

##### can_share

Returns True if `member` can share with `user`:

```django
    {{ member|can_share:user }}
```

##### readable_bytes

Display number of bytes using appropriate units.

```django
    {{ 73741824|readable_bytes }}
```

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

```django
PINAX_DOCUMENTS_HOOKSET = "myapp.hooks.DocumentsHookSet"
```

### Templates

Default templates are provided by the `pinax-templates` app in the
[documents](https://github.com/pinax/pinax-templates/tree/master/pinax/templates/templates/pinax/documents)
section of that project.

Reference pinax-templates
[installation instructions](https://github.com/pinax/pinax-templates/blob/master/README.md#installation)
to include these templates in your project.

View live `pinax-templates` examples and source at [Pinax Templates](https://templates.pinaxproject.com/documents/)!

#### Customizing Templates

Override the default `pinax-templates` templates by copying them into your project
subdirectory `pinax/documents/` on the template path and modifying as needed.

For example if your project doesn't use Bootstrap, copy the desired templates
then remove Bootstrap and Font Awesome class names from your copies.
Remove class references like `class="btn btn-success"` and `class="icon icon-pencil"` as well as
`bootstrap` from the `{% load i18n bootstrap %}` statement.
Since `bootstrap` template tags and filters are no longer loaded, you'll also need to update
`{{ form|bootstrap }}` to `{{ form }}` since the "bootstrap" filter is no longer available.

#### `base.html`

#### `document_confirm_delete.html`

#### `document_create.html`

#### `document_detail.html`

#### `folder_confirm_delete.html`

#### `folder_create.html`

#### `folder_detail.html`

#### `folder_share.html`

#### `index.html`


## Change Log

### 2.0.0

* Drop Django 1.11, 2.0, and 2.1, and Python 2,7, 3.4, and 3.5 support
* Add Django 2.2 and 3.0, and Python 3.6, 3.7, and 3.8 support
* Update packaging configs
* Direct users to community resources

### 1.0.2

* Allow use with any account-management package by removing django-user-accounts dependency
* Require pinax-templates>=2.0.0 if using pinax-templates without django-user-accounts

### 1.0.1

* Update requirements
* Replace pinax-theme-bootstrap requirement with pinax-templates
* Remove doc build support
* Improve documentation markup

### 1.0.0

* Standardize documentation layout
* Drop Django v1.8, v1.10 support
* Replace _clone with _chain to fix unexpected keyword argument 'user' error
* Add hookset documentation
* Add view documentation

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


## Contribute

[Contributing](https://github.com/pinax/.github/blob/master/CONTRIBUTING.md) information can be found in the [Pinax community health file repo](https://github.com/pinax/.github).


## Code of Conduct

In order to foster a kind, inclusive, and harassment-free community, the Pinax Project has a [Code of Conduct](https://github.com/pinax/.github/blob/master/CODE_OF_CONDUCT.md). We ask you to treat everyone as a smart human programmer that shares an interest in Python, Django, and Pinax with you.


## Connect with Pinax

For updates and news regarding the Pinax Project, please follow us on Twitter [@pinaxproject](https://twitter.com/pinaxproject) and check out our [Pinax Project blog](http://blog.pinaxproject.com).


## License

Copyright (c) 2012-present James Tauber and contributors under the [MIT license](https://opensource.org/licenses/MIT).
