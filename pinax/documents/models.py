import itertools
import math
import os
import uuid

from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from django.contrib.auth import get_user_model

from .compat import izip_longest
from .conf import settings
from .managers import FolderManager, FolderQuerySet, DocumentQuerySet


def uuid_filename(instance, filename):
    ext = filename.split(".")[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join("document", filename)


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

    def __unicode__(self):
        return self.name

    def save(self, **kwargs):
        self.touch(self.author, commit=False)
        super(Folder, self).save(**kwargs)

    def get_absolute_url(self):
        return reverse("documents_folder_detail", args=[self.pk])

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
        Determines the shared parent and checks if given user is the author
        of the folder.
        """
        # sp = self.shared_parent()
        # return sp.author_id == user.id and self == sp
        # only share folders that live at the top-level
        return self.parent_id is None and self.author_id == user.id

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


class Document(models.Model):

    name = models.CharField(max_length=255)
    folder = models.ForeignKey(Folder, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="+")
    created = models.DateTimeField(default=timezone.now)
    modified = models.DateTimeField(default=timezone.now)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="+")
    file = models.FileField(upload_to=uuid_filename)

    objects = DocumentQuerySet.as_manager()

    kind = "document"
    icon = "file"
    shared = None

    @classmethod
    def shared_user_model(cls):
        return DocumentSharedUser

    def __unicode__(self):
        return self.name

    def save(self, **kwargs):
        self.touch(self.author, commit=False)
        super(Document, self).save(**kwargs)

    def get_absolute_url(self):
        return reverse("documents_document_detail", args=[self.pk])

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
        return reverse("documents_document_download", args=[self.pk, os.path.basename(self.file.name).lower()])


class MemberSharedUser(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    # @@@ priviledges

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
        p = self.percentage
        if p >= 0 and p < 60:
            return "success"
        if p >= 60 and p < 90:
            return "warning"
        if p >= 90 and p <= 100:
            return "danger"
        raise ValueError("percentage out of range")


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def ensure_userstorage(sender, **kwargs):
    if kwargs["created"]:
        user = kwargs["instance"]
        UserStorage.objects.create(user=user, bytes_total=(1024 * 1024 * 50))
