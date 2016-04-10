from django.core.files.uploadedfile import SimpleUploadedFile

from test_plus.test import TestCase as PlusTestCase

from ..exceptions import DuplicateFolderNameError, DuplicateDocumentNameError
from ..models import (
    Document,
    Folder
)


class BaseTest(PlusTestCase):

    def setUp(self):
        self.user = self.make_user("eldarion")


class FolderTestCase(BaseTest):

    def test_cannot_have_duplicate_sibling_folder_names(self):
        Folder.objects.create(name="Foo", author=self.user, modified_by=self.user)
        with self.assertRaises(DuplicateFolderNameError):
            Folder.objects.create(name="Foo", author=self.user, modified_by=self.user)

    def test_can_have_duplicate_folder_names_at_different_paths(self):
        foo = Folder.objects.create(name="Foo", author=self.user, modified_by=self.user)
        bar = Folder.objects.create(name="Bar", parent=foo, author=self.user, modified_by=self.user)
        Folder.objects.create(name="Foo", parent=bar, author=self.user, modified_by=self.user)
        with self.assertRaises(DuplicateFolderNameError):
            Folder.objects.create(name="Bar", parent=foo, author=self.user, modified_by=self.user)


class DocumentTestCase(BaseTest):

    def test_cannot_have_duplicate_sibling_document_names(self):
        simple_file = SimpleUploadedFile("delicious.txt", b"something tasty")
        Document.objects.create(name="Foo", author=self.user, file=simple_file, modified_by=self.user)
        with self.assertRaises(DuplicateDocumentNameError):
            Document.objects.create(name="Foo", author=self.user, file=simple_file, modified_by=self.user)

    def test_can_have_duplicate_document_names_at_different_paths(self):
        simple_file = SimpleUploadedFile("delicious.txt", b"something tasty")
        foo = Folder.objects.create(name="Foo", author=self.user, modified_by=self.user)
        bar = Folder.objects.create(name="Bar", parent=foo, author=self.user, modified_by=self.user)
        Document.objects.create(name="Foo", author=self.user, file=simple_file, modified_by=self.user)
        Document.objects.create(name="Bar", folder=foo, author=self.user, file=simple_file, modified_by=self.user)
        Document.objects.create(name="Foo", folder=bar, author=self.user, file=simple_file, modified_by=self.user)
        with self.assertRaises(DuplicateDocumentNameError):
            Document.objects.create(name="Bar", folder=foo, author=self.user, file=simple_file, modified_by=self.user)
