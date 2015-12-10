from django.conf.urls import url

from . import views


urlpatterns = [
    url(r"^$", views.IndexView.as_view(), name="documents_index"),
    url(r"^f/create/$", views.folder_create, name="documents_folder_create"),
    url(r"^d/create/$", views.document_create, name="documents_document_create"),
    url(r"^f/(\d+)/$", views.folder_detail, name="documents_folder_detail"),
    url(r"^f/(\d+)/share/$", views.folder_share, name="documents_folder_share"),
    url(r"^d/(\d+)/$", views.document_detail, name="documents_document_detail"),
    url(r"^d/(\d+)/([^/]+)$", views.document_download, name="documents_document_download"),
    url(r"^d/delete/$", views.document_delete, name="documents_document_delete"),
]
