from django.core.urlresolvers import reverse
from django.db import transaction
from django.db.models import F
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views import static
from django.views.generic.base import TemplateView

from django.contrib import messages
from django.contrib.auth import get_user_model

from account.decorators import login_required
from account.mixins import LoginRequiredMixin
from account.utils import default_redirect, user_display

from .conf import settings
from .forms import (
    FolderCreateForm, DocumentCreateForm, ColleagueFolderShareForm
)
from .models import Folder, Document, UserStorage


class IndexView(LoginRequiredMixin, TemplateView):

    template_name = "documents/index.html"

    def get_context_data(self, **kwargs):
        ctx = kwargs
        ctx.update({
            "members": Folder.objects.members(None, user=self.request.user),
            "storage": self.request.user.storage,
            "can_share": False,
        })
        return ctx


@login_required
def folder_create(request):
    if "p" in request.GET:
        qs = Folder.objects.for_user(request.user)
        parent = get_object_or_404(qs, pk=request.GET["p"])
    else:
        parent = None
    form_kwargs = {"folders": Folder.objects.for_user(request.user)}
    if request.method == "POST":
        form = FolderCreateForm(request.POST, **form_kwargs)
        if form.is_valid():
            kwargs = {
                "name": form.cleaned_data["name"],
                "author": request.user,
                "parent": form.cleaned_data["parent"],
            }
            folder = Folder.objects.create(**kwargs)
            folder.touch(request.user)
            # if folder is not amongst anything shared it will share with no
            # users which share will no-op; perhaps not the best way?
            folder.share(folder.shared_parent().shared_with())
            return redirect(folder)
    else:
        initial = {}
        if parent:
            initial["parent"] = parent
        form_kwargs["initial"] = initial
        form = FolderCreateForm(**form_kwargs)
    ctx = {
        "form": form,
        "parent": parent,
    }
    return render(request, "documents/folder_create.html", ctx)


@login_required
def folder_detail(request, pk):
    qs = Folder.objects.for_user(request.user)
    folder = get_object_or_404(qs, pk=pk)
    ctx = {
        "folder": folder,
        "members": folder.members(user=request.user),
        "can_share": folder.can_share(request.user),
    }
    return render(request, "documents/folder_detail.html", ctx)


@login_required
def document_create(request):
    if "f" in request.GET:
        qs = Folder.objects.for_user(request.user)
        folder = get_object_or_404(qs, pk=request.GET["f"])
    else:
        folder = None
    form_kwargs = {
        "folders": Folder.objects.for_user(request.user),
        "storage": request.user.storage,
    }
    if request.method == "POST":
        form = DocumentCreateForm(request.POST, request.FILES, **form_kwargs)
        if form.is_valid():
            with transaction.atomic():
                bytes = form.cleaned_data["file"].size
                kwargs = {
                    "name": form.cleaned_data["file"].name,
                    "folder": form.cleaned_data["folder"],
                    "author": request.user,
                    "file": form.cleaned_data["file"],
                }
                document = Document.objects.create(**kwargs)
                document.touch(request.user)
                if document.folder is not None:
                    # if folder is not amongst anything shared it will share with no
                    # users which share will no-op; perhaps not the best way?
                    document.share(document.folder.shared_parent().shared_with())
                # increase usage for this user based on document size
                storage_qs = UserStorage.objects.filter(pk=request.user.storage.pk)
                storage_qs.update(bytes_used=F("bytes_used") + bytes)
            return redirect(document)
    else:
        initial = {}
        if folder:
            initial["folder"] = folder
        form_kwargs["initial"] = initial
        form = DocumentCreateForm(**form_kwargs)
    ctx = {
        "form": form,
        "folder": folder,
    }
    return render(request, "documents/document_create.html", ctx)


@login_required
def document_detail(request, pk):
    qs = Document.objects.for_user(request.user)
    document = get_object_or_404(qs, pk=pk)
    ctx = {
        "document": document,
    }
    return render(request, "documents/document_detail.html", ctx)


@login_required
def document_download(request, pk, *args):
    qs = Document.objects.for_user(request.user)
    document = get_object_or_404(qs, pk=pk)
    if settings.DOCUMENTS_USE_X_ACCEL_REDIRECT:
        response = HttpResponse()
        response["X-Accel-Redirect"] = document.file.url
        # delete content-type to allow Gondor to determine the filetype and
        # we definitely don't want Django's crappy default :-)
        del response["content-type"]
    else:
        response = static.serve(request, document.file.name, document_root=settings.MEDIA_ROOT)
    return response


@login_required
def folder_share(request, pk):
    User = get_user_model()
    qs = Folder.objects.for_user(request.user)
    folder = get_object_or_404(qs, pk=pk)
    if not folder.can_share(request.user):
        raise Http404()
    form_kwargs = {
        "colleagues": User.objects.all()  # @@@ make this a hookset to be defined at site level
    }
    if request.method == "POST":
        if "remove" in request.POST:
            user_to_remove = User.objects.get(pk=request.POST["remove"])
            messages.success(request, "{} has been removed from folder share".format(user_display(user_to_remove)))
            return redirect("documents_folder_share", folder.pk)
        else:
            form = ColleagueFolderShareForm(request.POST, **form_kwargs)
            if form.is_valid():
                folder.share(form.cleaned_data["participants"])
                return redirect(folder)
    else:
        form = ColleagueFolderShareForm(**form_kwargs)
    ctx = {
        "folder": folder,
        "form": form,
        "participants": folder.shared_with(),
    }
    return render(request, "documents/folder_share.html", ctx)


def document_delete(request):
    redirect_to = default_redirect(request, reverse("documents_index"))
    messages.success(request, "Document has been deleted")
    return redirect(redirect_to)
