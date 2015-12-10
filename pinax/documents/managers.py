import itertools
import operator

from django.apps import apps
from django.db import models
from django.db.models import Q
from django.db.models.query import QuerySet


class FolderManager(models.Manager):

    def members(self, folder, **kwargs):
        direct = kwargs.get("direct", True)
        user = kwargs.get("user")
        Document = apps.get_model("documents", "Document")
        folders = self.filter(parent=folder)
        documents = Document.objects.filter(folder=folder)
        if user:
            folders = folders.for_user(user)
            documents = documents.for_user(user)
        M = sorted(itertools.chain(folders, documents), key=operator.attrgetter("name"))
        if direct:
            return M
        for child in folders:
            M.extend(self.members(child, **kwargs))
        return M


class FolderQuerySet(QuerySet):

    def for_user(self, user):
        """
        All folders the given user can do something with.
        """
        qs = SharedMemberQuerySet(model=self.model, using=self._db, user=user)
        qs = qs.filter(Q(author=user) | Q(foldershareduser__user=user))
        return qs.distinct() & self.distinct()


class DocumentQuerySet(QuerySet):

    def for_user(self, user):
        """
        All documents the given user can do something with.
        """
        qs = SharedMemberQuerySet(model=self.model, using=self._db, user=user)
        qs = qs.filter(Q(author=user) | Q(documentshareduser__user=user))
        return qs.distinct() & self.distinct()


class SharedMemberQuerySet(QuerySet):

    def __init__(self, **kwargs):
        if "user" in kwargs:
            self.user = kwargs.pop("user")
        super(SharedMemberQuerySet, self).__init__(**kwargs)

    def iterator(self):
        shared_user_model = self.model.shared_user_model()
        shared_members = shared_user_model.for_user(self.user)
        for obj in super(SharedMemberQuerySet, self).iterator():
            if obj.pk in shared_members:
                obj._shared = True
            yield obj

    def _clone(self, **kwargs):
        kwargs["user"] = self.user
        return super(SharedMemberQuerySet, self)._clone(**kwargs)
