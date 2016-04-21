# Installation

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
