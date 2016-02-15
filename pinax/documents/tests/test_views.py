from mock import patch

from django.core.files.uploadedfile import SimpleUploadedFile

from ..models import (
    Document,
    Folder,
)
from .test import TestCase


class TestViews(TestCase):

    def setUp(self):
        """
        Create default Folders and Documents.
        """
        # Mock "messages" app.
        patcher = patch('django.contrib.messages.success')
        self.addCleanup(patcher.stop)
        patcher.start()

        self.user = self.make_user("eldarion")

        self.fruit_folder = Folder.objects.create(name="Fruit", author=self.user)
        self.apple_folder = Folder.objects.create(name="Apples", author=self.user,
                                                  parent=self.fruit_folder)
        self.orange_folder = Folder.objects.create(name="Oranges", author=self.user,
                                                   parent=self.fruit_folder)

        apple_file = SimpleUploadedFile("honeycrisp.txt",
                                        "Honeycrisp apple")

        # Create one Document in the Apples Folder.
        self.apple_doc = Document.objects.create(name="Honeycrisp",
                                                 author=self.user,
                                                 folder=self.apple_folder,
                                                 file=apple_file,
                                                 )


class TestFolders(TestViews):

    def setUp(self):
        super(TestFolders, self).setUp()
        self.create_urlname = "documents_folder_create"
        self.detail_urlname = "documents_folder_detail"

    def test_get_create_without_parent(self):
        """
        Ensure GET does not return a 'parent' folder in context.
        """
        with self.login(self.user):
            response = self.get(self.create_urlname)
            self.response_200(response)
            self.assertContext("parent", None)

    def test_get_create_with_parent(self):
        """
        Ensure GET returns a valid 'parent' folder in context.
        """
        querystring_data = {"p": self.fruit_folder.pk}
        with self.login(self.user):
            response = self.get(self.create_urlname, data=querystring_data)
            self.response_200(response)
            self.assertContext("parent", self.fruit_folder)

    def test_get_create_with_illegal_parent(self):
        """
        Ensure GET fails if "p" querystring is invalid.
        """
        querystring_data = {"p": 555}
        with self.login(self.user):
            response = self.get(self.create_urlname, data=querystring_data)
            self.response_404(response)

    def test_post_create_without_parent(self):
        """
        Ensure POST creates folder without a parent.
        """
        folder_name = "Spindle"
        post_args = {"name": folder_name}
        with self.login(self.user):
            response = self.post(self.create_urlname, data=post_args, follow=True)
            self.response_200(response)
            created = self.get_context("object")
            self.assertFalse(created.parent)
            self.assertTrue(Folder.objects.get(name=folder_name))

    def test_post_create_with_parent(self):
        """
        Ensure POST creates folder with a parent.
        """
        folder_name = "Spindle"
        post_args = {"name": folder_name, "parent": self.fruit_folder.pk}
        with self.login(self.user):
            response = self.post(self.create_urlname, data=post_args, follow=True)
            self.response_200(response)
            created = self.get_context("object")
            self.assertEqual(created.parent, self.fruit_folder)
            self.assertTrue(Folder.objects.get(name=folder_name))

    def test_post_create_with_illegal_parent(self):
        """
        Ensure POST does not creates folder with invalid parent.
        """
        folder_name = "Spindle"
        post_args = {"name": folder_name, "parent": 555}
        with self.login(self.user):
            response = self.post(self.create_urlname, data=post_args, follow=True)
            self.response_200(response)
            self.assertFalse("object" in self.last_response.context)
            self.assertFalse(Folder.objects.filter(name=folder_name))

    def test_detail(self):
        """
        Ensure we can see folder detail.
        """
        with self.login(self.user):
            self.get_check_200(self.detail_urlname, pk=self.fruit_folder.pk)
            folder = self.get_context("object")
            self.assertEqual(folder, self.fruit_folder)

    def test_duplicate_folder_name(self):
        """
        Do we allow Folders with the same name?
        """
        pass

    def test_delete(self):
        """
        Ensure we can delete a folder?
        """
        pass


class TestDocuments(TestViews):

    def setUp(self):
        super(TestDocuments, self).setUp()
        self.create_urlname = "documents_document_create"
        self.detail_urlname = "documents_document_detail"
        self.file = SimpleUploadedFile("delicious.txt",
                                       "Golden Delicious apple")


    def test_get_create_without_folder(self):
        """
        Ensure GET does not return a 'folder' in context.
        """
        with self.login(self.user):
            response = self.get(self.create_urlname)
            self.response_200(response)
            self.assertContext("folder", None)

    def test_get_create_with_folder(self):
        """
        Ensure GET returns a valid 'folder' in context.
        """
        querystring_data = {"f": self.orange_folder.pk}
        with self.login(self.user):
            response = self.get(self.create_urlname, data=querystring_data)
            self.response_200(response)
            self.assertContext("folder", self.orange_folder)

    def test_get_create_with_illegal_folder(self):
        """
        Ensure GET fails if "f" querystring is invalid.
        """
        querystring_data = {"f": 555}
        with self.login(self.user):
            response = self.get(self.create_urlname, data=querystring_data)
            self.response_404(response)

    def test_post_create_without_folder(self):
        """
        Ensure POST creates document without a folder.
        """
        post_args = {"name": "file", "file": self.file}
        with self.login(self.user):
            response = self.post(self.create_urlname, data=post_args, follow=True)
            self.response_200(response)
            created = self.get_context("object")
            self.assertFalse(created.folder)
            self.assertTrue(Document.objects.get(name=self.file.name))

    def test_post_create_with_parent(self):
        """
        Ensure POST creates document associated with a folder.
        """
        post_args = {"name": "file", "file": self.file, "folder": self.apple_folder.pk}
        with self.login(self.user):
            response = self.post(self.create_urlname, data=post_args, follow=True)
            self.response_200(response)
            created = self.get_context("object")
            self.assertEqual(created.folder, self.apple_folder)
            self.assertTrue(Document.objects.get(name=self.file.name))

    def test_post_create_with_illegal_parent(self):
        """
        Ensure POST does not create a document with invalid folder.
        """
        post_args = {"name": "file", "file": self.file, "folder": 555}
        with self.login(self.user):
            response = self.post(self.create_urlname, data=post_args, follow=True)
            self.response_200(response)
            self.assertFalse("object" in self.last_response.context)
            self.assertFalse(Document.objects.filter(name=self.file.name))

    def test_detail(self):
        """
        Ensure we can see document detail.
        """
        with self.login(self.user):
            self.get_check_200(self.detail_urlname, pk=self.apple_doc.pk)
            document = self.get_context("object")
            self.assertEqual(document, self.apple_doc)

    def test_valid_delete(self):
        """
        Ensure we can delete a valid Document.
        """
        doc_pk = self.apple_doc.pk
        with self.login(self.user):
            response = self.post("documents_document_delete", pk=doc_pk, follow=True)
            self.response_200(response)
            self.assertFalse(Document.objects.filter(pk=doc_pk))

            # TODO: Ensure the actual file is removed from storage.
            self.assertTrue(False)

    def test_invalid_delete(self):
        """
        Ensure we get error trying to delete an invalid Document.
        """
        doc_pk = 555
        with self.login(self.user):
            response = self.post("documents_document_delete", pk=doc_pk, follow=True)
            self.response_404(response)
