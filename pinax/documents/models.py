import itertools
import math

from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import F
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible

from django.contrib.auth import get_user_model

from .compat import izip_longest
from .conf import settings
from .exceptions import DuplicateFolderNameError, DuplicateDocumentNameError
from .hooks import hookset
from .managers import FolderManager, FolderQuerySet, DocumentQuerySet


def uuid_filename(instance, filename):
    return hookset.file_upload_to(instance, filename)


@python_2_unicode_compatible
class Folder(models.Model):

    name = models.CharField(max_length=140)
    parent = models.ForeignKey("self", null=True, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="+")
    created = models.DateTimeField(default=timezone.now)
    modified = models.DateTimeField(default=timezone.now)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="+")

    objects = FolderManager.from_queryset(FolderQuerySet)()

    kind = "folder"
    icon = "folder-open"
    shared = None

    @classmethod
    def shared_user_model(cls):
        return FolderSharedUser

    @classmethod
    def already_exists(cls, name, parent=None):
        return cls.objects.filter(name=name, parent=parent).exists()

    def __str__(self):
        return self.name

    def save(self, **kwargs):
        if not self.pk and Folder.already_exists(self.name, self.parent):
            raise DuplicateFolderNameError("{} already exists in this folder.".format(self.name))
        self.touch(self.author, commit=False)
        super(Folder, self).save(**kwargs)

    def get_absolute_url(self):
        return reverse("pinax_documents:folder_detail", args=[self.pk])

    def unique_id(self):
        return "f-%d" % self.id

    def members(self, **kwargs):
        return Folder.objects.members(self, **kwargs)

    def touch(self, user, commit=True):
        self.modified = timezone.now()
        self.modified_by = user
        if commit:
            if self.parent:
                self.parent.touch(user)
            self.save()

    @property
    def size(self):
        """
        Return size of this folder.
        """
        return sum([m.size for m in self.members(direct=False) if m.kind == "document"])

    def breadcrumbs(self):
        """
        Produces a list of ancestors (excluding self).
        """
        crumbs = []
        if self.parent:
            crumbs.extend(self.parent.breadcrumbs())
            crumbs.append(self.parent)
        return crumbs

    def shared_queryset(self):
        """
        Returns queryset of this folder mapped into the shared user model.
        The queryset should only consist of zero or one instances (aka shared
        or not shared.) This method is mostly used for convenience.
        """
        model = self.shared_user_model()
        return model._default_manager.filter(**{model.obj_attr: self})

    @property
    def shared(self):
        """
        Determines if self is shared. This checks the denormalization and
        does not return whether self SHOULD be shared (based on parents.)
        """
        return self.shared_queryset().exists()

    def shared_ui(self):
        """
        Returns boolean based on whether self should show any shared UI.
        """
        return self.parent_id is None and self.shared

    def shared_with(self, user=None):
        """
        Returns a User queryset of users shared on this folder, or, if user
        is given optimizes the check and returns boolean.
        """
        User = get_user_model()
        qs = self.shared_queryset()
        if user is not None:
            return qs.filter(user=user).exists()
        if not qs.exists():
            return User.objects.none()
        return User.objects.filter(pk__in=qs.values("user"))

    def shared_parent(self):
        """
        Returns the folder object that is the shared parent (the root of
        a shared folder hierarchy) or None if there is no shared parent.
        """
        root = self
        a, b = itertools.tee(reversed(self.breadcrumbs()))
        next(b, None)
        for folder, parent in izip_longest(a, b):
            if folder.shared:
                root = folder
            if parent is None or not parent.shared:
                break
        return root

    def can_share(self, user):
        """
        Ensures folder is top-level and `user` is the author.
        """
        return hookset.can_share_folder(user, self)

    def share(self, users):
        """
        Ensures self is shared with given users (can accept users who are
        already shared on self).
        """
        users = [u for u in users if not self.shared_with(user=u)]
        if users:
            members = [self] + self.members(direct=False)
            FM, DM = self.shared_user_model(), Document.shared_user_model()
            fm, dm = [], []
            for member, user in itertools.product(members, users):
                if user.pk == member.author_id:
                    continue
                if isinstance(member, Folder):
                    fm.append(FM(**{FM.obj_attr: member, "user": user}))
                if isinstance(member, Document):
                    dm.append(DM(**{DM.obj_attr: member, "user": user}))
            FM._default_manager.bulk_create(fm)
            DM._default_manager.bulk_create(dm)

    def delete_url(self):
        return reverse(
            "pinax_documents:folder_delete",
            args=[self.pk]
        )


@python_2_unicode_compatible
class Document(models.Model):

    name = models.CharField(max_length=255)
    folder = models.ForeignKey(Folder, null=True, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="+")
    created = models.DateTimeField(default=timezone.now)
    modified = models.DateTimeField(default=timezone.now)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="+")
    file = models.FileField(upload_to=uuid_filename)
    original_filename = models.CharField(max_length=500)

    objects = DocumentQuerySet.as_manager()

    kind = "document"
    icon = "file"
    shared = None

    def delete(self, *args, **kwargs):
        bytes_to_free = self.size
        super(Document, self).delete(*args, **kwargs)
        storage_qs = UserStorage.objects.filter(pk=self.author.storage.pk)
        storage_qs.update(bytes_used=F("bytes_used") - bytes_to_free)

    @classmethod
    def shared_user_model(cls):
        return DocumentSharedUser

    @classmethod
    def already_exists(cls, name, folder=None):
        return cls.objects.filter(name=name, folder=folder).exists()

    def __str__(self):
        return self.name

    def save(self, **kwargs):
        if not self.pk and Document.already_exists(self.name, self.folder):
            raise DuplicateDocumentNameError("{} already exists in this folder.".format(self.name))
        self.touch(self.author, commit=False)
        super(Document, self).save(**kwargs)

    def get_absolute_url(self):
        return reverse("pinax_documents:document_detail", args=[self.pk])

    def unique_id(self):
        return "d-%d" % self.id

    def touch(self, user, commit=True):
        self.modified = timezone.now()
        self.modified_by = user
        if commit:
            if self.folder:
                self.folder.touch(user)
            self.save()

    @property
    def size(self):
        return self.file.size

    def breadcrumbs(self):
        crumbs = []
        if self.folder:
            crumbs.extend(self.folder.breadcrumbs())
            crumbs.append(self.folder)
        return crumbs

    def shared_queryset(self):
        """
        Returns queryset of this folder mapped into the shared user model.
        The queryset should only consist of zero or one instances (aka shared
        or not shared.) This method is mostly used for convenience.
        """
        model = self.shared_user_model()
        return model._default_manager.filter(**{model.obj_attr: self})

    @property
    def shared(self):
        """
        Determines if self is shared. This checks the denormalization and
        does not return whether self SHOULD be shared (based on parents.)
        """
        return self.shared_queryset().exists()

    def shared_ui(self):
        return False

    def shared_with(self, user=None):
        """
        Returns a User queryset of users shared on this folder, or, if user
        is given optimizes the check and returns boolean.
        """
        User = get_user_model()
        qs = self.shared_queryset()
        if user is not None:
            return qs.filter(user=user).exists()
        if not qs.exists():
            return User.objects.none()
        return User.objects.filter(pk__in=qs.values("user"))

    def share(self, users):
        users = [u for u in users if not self.shared_with(user=u)]
        if users:
            model = self.shared_user_model()
            objs = []
            for user in users:
                objs.append(self.shared_user_model()(**{model.obj_attr: self, "user": user}))
            model._default_manager.bulk_create(objs)

    def download_url(self):
        return reverse(
            "pinax_documents:document_download",
            args=[self.pk]
        )

    def delete_url(self):
        return reverse(
            "pinax_documents:document_delete",
            args=[self.pk]
        )


class MemberSharedUser(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    # @@@ privileges

    class Meta:
        abstract = True

    @classmethod
    def for_user(cls, user):
        qs = cls._default_manager.filter(user=user)
        return qs.values_list(cls.obj_attr, flat=True)


class FolderSharedUser(MemberSharedUser):

    folder = models.ForeignKey(Folder)
    obj_attr = "folder"

    class Meta:
        unique_together = [("folder", "user")]


class DocumentSharedUser(MemberSharedUser):

    document = models.ForeignKey(Document)
    obj_attr = "document"

    class Meta:
        unique_together = [("document", "user")]


class UserStorage(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="storage")
    bytes_used = models.BigIntegerField(default=0)
    bytes_total = models.BigIntegerField(default=0)

    @property
    def percentage(self):
        return int(math.ceil((float(self.bytes_used) / self.bytes_total) * 100))

    @property
    def color(self):
        return hookset.storage_color(self)
