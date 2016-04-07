from django.conf.urls import url

from . import views

urlpatterns = [
    url(r"^$", views.IndexView.as_view(),
        name="document_index"),
    url(r"^d/create/$", views.DocumentCreate.as_view(),
        name="document_create"),
    url(r"^d/(?P<pk>\d+)/$", views.DocumentDetail.as_view(),
        name="document_detail"),
    url(r"^d/(?P<pk>\d+)/download/$", views.DocumentDownload.as_view(),
        name="document_download"),
    url(r"^d/(?P<pk>\d+)/delete/$", views.DocumentDelete.as_view(),
        name="document_delete"),
    url(r"^f/create/$", views.FolderCreate.as_view(),
        name="folder_create"),
    url(r"^f/(?P<pk>\d+)/$", views.FolderDetail.as_view(),
        name="folder_detail"),
    url(r"^f/(?P<pk>\d+)/share/$", views.FolderShare.as_view(),
        name="folder_share"),
    url(r"^f/(?P<pk>\d+)/delete/$", views.FolderDelete.as_view(),
        name="folder_delete"),
]
