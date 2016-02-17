from django.conf.urls import url

from . import views


urlpatterns = [
    url(r"^$", views.IndexView.as_view(),
        name="pinax_documents_index"),
    url(r"^f/create/$", views.FolderCreate.as_view(),
        name="pinax_documents_folder_create"),
    url(r"^d/create/$", views.DocumentCreate.as_view(),
        name="pinax_documents_document_create"),
    url(r"^f/(?P<pk>\d+)/$", views.FolderDetail.as_view(),
        name="pinax_documents_folder_detail"),
    url(r"^f/(?P<pk>\d+)/share/$", views.FolderShare.as_view(),
        name="pinax_documents_folder_share"),
    url(r"^d/(?P<pk>\d+)/$", views.DocumentDetail.as_view(),
        name="pinax_documents_document_detail"),
    url(r"^d/(?P<pk>\d+)/download/$", views.DocumentDownload.as_view(),
        name="pinax_documents_document_download"),
    url(r"^d/(?P<pk>\d+)/delete/$", views.DocumentDelete.as_view(),
        name="pinax_documents_document_delete"),
]
