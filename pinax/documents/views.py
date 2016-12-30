from django.core.urlresolvers import reverse, reverse_lazy
from django.db import transaction
from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from django.views import static
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    TemplateView,
)
from django.views.generic.detail import (
    SingleObjectMixin, SingleObjectTemplateResponseMixin,
)
from django.views.generic.edit import (
    FormMixin,
    ProcessFormView,
)

from account.mixins import LoginRequiredMixin

from .conf import settings
from .forms import (
    ColleagueFolderShareForm,
    DocumentCreateForm,
    DocumentCreateFormWithName,
    FolderCreateForm
)
from .hooks import hookset
from .models import (
    Document,
    Folder,
    UserStorage,
)


class IndexView(LoginRequiredMixin, TemplateView):

    template_name = "pinax/documents/index.html"

    def get_context_data(self, **kwargs):
        ctx = kwargs
        ctx.update({
            "members": Folder.objects.members(None, user=self.request.user),
            "storage": self.request.user.storage,
            "can_share": False,
        })
        return ctx


class FolderCreate(LoginRequiredMixin, CreateView):
    model = Folder
    form_class = FolderCreateForm
    template_name = "pinax/documents/folder_create.html"
    parent = None

    def get(self, request, *args, **kwargs):
        if "p" in request.GET:
            qs = self.model.objects.for_user(request.user)
            self.parent = get_object_or_404(qs, pk=request.GET["p"])
        else:
            self.parent = None
        return super(FolderCreate, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs.setdefault("parent", self.parent)
        return super(FolderCreate, self).get_context_data(**kwargs)

    def get_initial(self):
        if self.parent:
            self.initial["parent"] = self.parent
        return super(FolderCreate, self).get_initial()

    def get_form_kwargs(self):
        kwargs = super(FolderCreate, self).get_form_kwargs()
        kwargs.update({"folders": self.model.objects.for_user(self.request.user)})
        return kwargs

    def create_folder(self, **kwargs):
        folder = self.model.objects.create(**kwargs)
        folder.touch(self.request.user)
        # if folder is not amongst anything shared it will share with no
        # users which share will no-op; perhaps not the best way?
        folder.share(folder.shared_parent().shared_with())
        return folder

    def form_valid(self, form):
        kwargs = {
            "name": form.cleaned_data["name"],
            "author": self.request.user,
            "parent": form.cleaned_data["parent"],
        }
        self.object = self.create_folder(**kwargs)
        hookset.folder_created_message(self.request, self.object)
        return HttpResponseRedirect(self.get_success_url())


class FolderDetail(LoginRequiredMixin, DetailView):
    model = Folder
    template_name = "pinax/documents/folder_detail.html"

    def get_queryset(self):
        qs = super(FolderDetail, self).get_queryset()
        qs = qs.for_user(self.request.user)
        return qs

    def get_form_kwargs(self):
        kwargs = super(FolderShare, self).get_form_kwargs()
        kwargs.update({"folders": self.model.objects.for_user(self.request.user)})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(FolderDetail, self).get_context_data(**kwargs)
        ctx = {
            "members": self.object.members(user=self.request.user),
            "can_share": self.object.can_share(self.request.user),
        }
        context.update(ctx)
        return context


class FolderShare(LoginRequiredMixin,
                  SingleObjectTemplateResponseMixin,
                  FormMixin,
                  SingleObjectMixin,
                  ProcessFormView):
    model = Folder
    context_object_name = "folder"
    form_class = ColleagueFolderShareForm
    template_name = "pinax/documents/folder_share.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(FolderShare, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(FolderShare, self).post(request, *args, **kwargs)

    def get_queryset(self):
        qs = super(FolderShare, self).get_queryset()
        qs = qs.for_user(self.request.user)
        return qs

    def get_object(self):
        folder = super(FolderShare, self).get_object()
        if not folder.can_share(self.request.user):
            raise Http404(_("Cannot share folder '{}'.".format(folder)))
        return folder

    def get_form_kwargs(self):
        kwargs = super(FolderShare, self).get_form_kwargs()
        can_share_with = hookset.share_with_options(self.request.user, self.object)
        kwargs.update({"colleagues": can_share_with})
        return kwargs

    def form_valid(self, form):
        self.object.share(form.cleaned_data["participants"])
        hookset.folder_shared_message(self.request, self.request.user, self.object)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("pinax_documents:folder_detail", args=[self.object.pk])

    def get_context_data(self, **kwargs):
        context = super(FolderShare, self).get_context_data(**kwargs)
        ctx = {
            "participants": self.object.shared_with(),
        }
        context.update(ctx)
        return context


class FolderDelete(LoginRequiredMixin, DeleteView):
    model = Folder
    success_url = reverse_lazy("pinax_documents:document_index")
    template_name = 'pinax/documents/folder_confirm_delete.html'

    def delete(self, request, *args, **kwargs):
        hookset.folder_pre_delete(self.request, self.get_object())
        success_url = super(FolderDelete, self).delete(request, *args, **kwargs)
        hookset.folder_deleted_message(self.request, self.object)
        return success_url


class DocumentCreate(LoginRequiredMixin, CreateView):
    model = Document
    form_class = DocumentCreateForm
    template_name = "pinax/documents/document_create.html"
    folder = None

    def get(self, request, *args, **kwargs):
        if "f" in request.GET:
            qs = Folder.objects.for_user(request.user)
            self.folder = get_object_or_404(qs, pk=request.GET["f"])
        else:
            self.folder = None
        return super(DocumentCreate, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs.setdefault("folder", self.folder)
        return super(DocumentCreate, self).get_context_data(**kwargs)

    def get_initial(self):
        if self.folder:
            self.initial["folder"] = self.folder
        return super(DocumentCreate, self).get_initial()

    def get_form_kwargs(self):
        kwargs = super(DocumentCreate, self).get_form_kwargs()
        kwargs.update({"folders": Folder.objects.for_user(self.request.user),
                       "storage": self.request.user.storage})
        return kwargs

    def create_document(self, **kwargs):
        document = self.model.objects.create(**kwargs)
        document.touch(self.request.user)
        if document.folder is not None:
            # if folder is not amongst anything shared it will share with no
            # users which share will no-op; perhaps not the best way?
            document.share(document.folder.shared_parent().shared_with())
        return document

    def increase_usage(self, bytes):
        # increase usage for this user based on document size
        storage_qs = UserStorage.objects.filter(pk=self.request.user.storage.pk)
        storage_qs.update(bytes_used=F("bytes_used") + bytes)

    def get_create_kwargs(self, form):
        return {
            "name": form.cleaned_data["file"].name,
            "original_filename": form.cleaned_data["file"].name,
            "folder": form.cleaned_data["folder"],
            "author": self.request.user,
            "file": form.cleaned_data["file"],
        }

    def form_valid(self, form):
        with transaction.atomic():
            kwargs = self.get_create_kwargs(form)
            self.object = self.create_document(**kwargs)
            hookset.document_created_message(self.request, self.object)
            bytes = form.cleaned_data["file"].size
            self.increase_usage(bytes)
            return HttpResponseRedirect(self.get_success_url())


class DocumentWithCustomNameCreate(DocumentCreate):

    form_class = DocumentCreateFormWithName

    def get_create_kwargs(self, form):
        return {
            "name": form.cleaned_data["name"],
            "original_filename": form.cleaned_data["file"].name,
            "folder": form.cleaned_data["folder"],
            "author": self.request.user,
            "file": form.cleaned_data["file"],
        }


class DocumentDetail(LoginRequiredMixin, DetailView):
    model = Document
    template_name = "pinax/documents/document_detail.html"

    def get_queryset(self):
        qs = super(DocumentDetail, self).get_queryset()
        qs = qs.for_user(self.request.user)
        return qs


class DocumentDownload(LoginRequiredMixin, DetailView):
    model = Document

    def get_queryset(self):
        qs = super(DocumentDownload, self).get_queryset()
        qs = qs.for_user(self.request.user)
        return qs

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if settings.DOCUMENTS_USE_X_ACCEL_REDIRECT:
            response = HttpResponse()
            response["X-Accel-Redirect"] = self.object.file.url
            # delete content-type to allow Gondor to determine the filetype and
            # we definitely don't want Django's crappy default :-)
            del response["content-type"]
        else:
            # Note:
            #
            # The 'django.views.static.py' docstring states:
            #
            #     Views and functions for serving static files. These are only to be used
            #     during development, and SHOULD NOT be used in a production setting.
            #
            response = static.serve(request, self.object.file.name,
                                    document_root=settings.MEDIA_ROOT)
        return response


class DocumentDelete(LoginRequiredMixin, DeleteView):
    model = Document
    success_url = reverse_lazy("pinax_documents:document_index")
    template_name = 'pinax/documents/document_confirm_delete.html'

    def delete(self, request, *args, **kwargs):
        success_url = super(DocumentDelete, self).delete(request, *args, **kwargs)
        hookset.document_deleted_message(self.request, self.object)
        return success_url
