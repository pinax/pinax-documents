from django.conf.urls import url

from . import views


urlpatterns = [
    url(r"^$", views.IndexView.as_view(), name="pinax_documents_index"),
    url(r"^f/create/$", views.folder_create, name="pinax_documents_folder_create"),
    url(r"^d/create/$", views.document_create, name="pinax_documents_document_create"),
    url(r"^f/(\d+)/$", views.folder_detail, name="pinax_documents_folder_detail"),
    url(r"^f/(\d+)/share/$", views.folder_share, name="pinax_documents_folder_share"),
    url(r"^d/(\d+)/$", views.document_detail, name="pinax_documents_document_detail"),
    url(r"^d/(\d+)/([^/]+)$", views.document_download, name="pinax_documents_document_download"),
    url(r"^d/delete/$", views.document_delete, name="pinax_documents_document_delete"),
]
