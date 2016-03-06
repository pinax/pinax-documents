from django.conf.urls import url, include


urlpatterns = [
    url(r"^", include("pinax.documents.urls", namespace="pinax_documents")),
]
