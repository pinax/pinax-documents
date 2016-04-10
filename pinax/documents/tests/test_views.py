import mock

from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpResponse

from ..models import (
    Document,
    Folder,
)
from .test import BaseTest


class TestFolders(BaseTest):

    def setUp(self):
        super(TestFolders, self).setUp()
        self.create_urlname = "pinax_documents:folder_create"
        self.detail_urlname = "pinax_documents:folder_detail"
        self.share_urlname = "pinax_documents:folder_share"
        self.delete_urlname = "pinax_documents:folder_delete"

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
        parent_folder = Folder.objects.create(name="Parent", author=self.user)

        querystring_data = {"p": parent_folder.pk}
        with self.login(self.user):
            response = self.get(self.create_urlname, data=querystring_data)
            self.response_200(response)
            self.assertContext("parent", parent_folder)

    def test_get_create_with_illegal_parent(self):
        """
        Ensure GET fails if "p" querystring is invalid.
        """
        querystring_data = {"p": 555}
        with self.login(self.user):
            response = self.get(self.create_urlname, data=querystring_data)
            self.response_404(response)

    @mock.patch("django.contrib.messages.success")
    def test_post_create_without_parent(self, mock_messages):
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
            self.assertTrue(mock_messages.called)

    @mock.patch("django.contrib.messages.success")
    def test_post_create_with_parent(self, mock_messages):
        """
        Ensure POST creates folder with a parent.
        """
        parent_folder = Folder.objects.create(name="Parent", author=self.user)

        folder_name = "Spindle"
        post_args = {"name": folder_name, "parent": parent_folder.pk}
        with self.login(self.user):
            response = self.post(self.create_urlname, data=post_args, follow=True)
            self.response_200(response)
            created = self.get_context("object")
            self.assertEqual(created.parent, parent_folder)
            self.assertTrue(Folder.objects.get(name=folder_name))
            self.assertTrue(mock_messages.called)

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

    def test_post_create_with_duplicate_name(self):
        """
        Ensure POST does not create a folder with duplicate name
        """
        folder_name = "Spindle"
        Folder.objects.create(name=folder_name, author=self.user, modified_by=self.user)
        post_args = {"name": folder_name}
        with self.login(self.user):
            response = self.post(self.create_urlname, data=post_args, follow=True)
            self.response_200(response)
            self.assertTrue("{} already exists.".format(folder_name) in str(response.context["form"].errors))
            self.assertFalse("object" in self.last_response.context)

    def test_detail(self):
        """
        Ensure we can see folder detail.
        """
        parent_folder = Folder.objects.create(name="Parent", author=self.user)

        with self.login(self.user):
            self.get_check_200(self.detail_urlname, pk=parent_folder.pk)
            folder = self.get_context("object")
            self.assertEqual(folder, parent_folder)

    def test_duplicate_folder_name(self):
        """
        Do we allow Folders with the same name?
        """
        pass

    @mock.patch("django.contrib.messages.success")
    def test_delete(self, mock_messages):
        """
        Ensure we can delete a folder.
        """
        parent_folder = Folder.objects.create(name="Parent", author=self.user)

        with self.login(self.user):
            response = self.get(self.delete_urlname, pk=parent_folder.pk)
            self.response_200(response)
            self.assertTrue('pinax/documents/folder_confirm_delete.html' in response.template_name)

            response = self.post(self.delete_urlname, pk=parent_folder.pk, follow=True)
            self.response_200(response)
            self.assertFalse(Folder.objects.filter(pk=parent_folder.pk))
            self.assertTrue(mock_messages.called)

            response = self.get(self.detail_urlname, pk=parent_folder.pk)
            self.response_404(response)

    @mock.patch("django.contrib.messages.success")
    def test_delete_recursive(self, mock_messages):
        """
        Ensure that when we delete a folder with contents, those contents are also deleted.
        """
        parent_folder = Folder.objects.create(name="Parent", author=self.user)
        child_folder = Folder.objects.create(name="Child", author=self.user, parent=parent_folder)
        Folder.objects.create(name="Grand Child", author=self.user, parent=child_folder)

        child_file = SimpleUploadedFile("child.txt", b"Child document")
        child_document = Document.objects.create(name="Child Doc",
                                                 author=self.user,
                                                 file=child_file,
                                                 folder=parent_folder,
                                                 )
        grand_child_file = SimpleUploadedFile("grand_child.txt", b"Grand Child document")
        grand_child_document = Document.objects.create(name="Grand Child Doc",
                                                       author=self.user,
                                                       file=grand_child_file,
                                                       folder=child_folder,
                                                       )

        with self.login(self.user):
            response = self.post(self.delete_urlname, pk=parent_folder.pk, follow=True)
            self.response_200(response)
            self.assertFalse(Folder.objects.all())
            self.assertFalse(Document.objects.all())

            self.assertTrue(mock_messages.called)

            response = self.get("pinax_documents:document_detail", pk=child_document.pk)
            self.response_404(response)
            response = self.get("pinax_documents:document_detail", pk=grand_child_document.pk)
            self.response_404(response)

    def test_get_share(self):
        """
        Ensure sharing users are present in GET context.
        """
        sharing_user = self.make_user("sharing")
        folder = Folder.objects.create(name="Not Mine", author=self.user)
        folder.save()
        folder.share([sharing_user])
        # Add another user who is not sharing `folder`.
        self.make_user("nonsharing")

        with self.login(self.user):
            self.get(self.share_urlname, pk=folder.pk)
            self.assertInContext("participants")
            self.assertSequenceEqual(self.last_response.context["participants"], [sharing_user])

    @mock.patch("django.contrib.messages.success")
    def test_share_valid(self, mock_messages):
        """
        Ensure we can share a Folder with a valid user.
        """
        other_user = self.make_user("other")
        folder = Folder.objects.create(name="Mine", author=self.user)
        folder.save()

        post_args = {"participants": [other_user.pk]}
        with self.login(self.user):
            response = self.post(self.share_urlname, pk=folder.pk, data=post_args, follow=True)
            self.response_200(response)
            self.assertTrue(folder.shared)
            self.assertTrue(folder.shared_with(other_user))
            self.assertTrue(mock_messages.called)

    def test_share_non_author(self):
        """
        Ensure we cannot share a Folder we didn't author.
        """
        other_user = self.make_user("other")
        folder = Folder.objects.create(name="Not Mine", author=other_user)
        folder.save()
        folder.share([self.user])

        # `folder` is now associated with self.user, but he did not
        #  author `folder` and should not be able to share it.
        post_args = {"participants": [other_user]}
        with self.login(self.user):
            response = self.post(self.share_urlname, pk=folder.pk, data=post_args, follow=True)
            self.response_404(response)


class TestDocuments(BaseTest):

    def setUp(self):
        super(TestDocuments, self).setUp()
        self.create_urlname = "pinax_documents:document_create"
        self.detail_urlname = "pinax_documents:document_detail"
        self.download_urlname = "pinax_documents:document_download"

        self.file_contents = b"Golden Delicious apple"

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
        parent_folder = Folder.objects.create(name="Parent", author=self.user)

        querystring_data = {"f": parent_folder.pk}
        with self.login(self.user):
            response = self.get(self.create_urlname, data=querystring_data)
            self.response_200(response)
            self.assertContext("folder", parent_folder)

    def test_get_create_with_illegal_folder(self):
        """
        Ensure GET fails if "f" querystring is invalid.
        """
        querystring_data = {"f": 555}
        with self.login(self.user):
            response = self.get(self.create_urlname, data=querystring_data)
            self.response_404(response)

    @mock.patch("django.contrib.messages.success")
    def test_post_create_without_folder(self, mock_messages):
        """
        Ensure POST creates document without a folder.
        """
        simple_file = SimpleUploadedFile("delicious.txt", self.file_contents)

        post_args = {"name": "file", "file": simple_file}
        with self.login(self.user):
            response = self.post(self.create_urlname, data=post_args, follow=True)
            self.response_200(response)
            created = self.get_context("object")
            self.assertFalse(created.folder)
            self.assertTrue(Document.objects.get(name=simple_file.name))
            self.assertTrue(mock_messages.called)

    @mock.patch("django.contrib.messages.success")
    def test_post_create_with_parent(self, mock_messages):
        """
        Ensure POST creates document associated with a folder.
        """
        parent_folder = Folder.objects.create(name="Parent", author=self.user)
        simple_file = SimpleUploadedFile("delicious.txt", self.file_contents)

        post_args = {"name": "file", "file": simple_file, "folder": parent_folder.pk}
        with self.login(self.user):
            response = self.post(self.create_urlname, data=post_args, follow=True)
            self.response_200(response)
            created = self.get_context("object")
            self.assertEqual(created.folder, parent_folder)
            self.assertTrue(Document.objects.get(name=simple_file.name))
            self.assertTrue(mock_messages.called)

    def test_post_create_with_illegal_parent(self):
        """
        Ensure POST does not create a document with invalid folder.
        """
        simple_file = SimpleUploadedFile("delicious.txt", self.file_contents)

        post_args = {"name": "file", "file": simple_file, "folder": 555}
        with self.login(self.user):
            response = self.post(self.create_urlname, data=post_args, follow=True)
            self.response_200(response)
            self.assertFalse("object" in self.last_response.context)
            self.assertFalse(Document.objects.filter(name=simple_file.name))

    def test_post_create_with_duplicate_name(self):
        """
        Ensure POST does not create a document with duplicate name
        """
        simple_file = SimpleUploadedFile("delicious.txt", self.file_contents)
        Document.objects.create(name="delicious.txt", author=self.user, file=simple_file, modified_by=self.user)
        simple_file = SimpleUploadedFile("delicious.txt", self.file_contents)
        post_args = {"name": "file", "file": simple_file}
        with self.login(self.user):
            response = self.post(self.create_urlname, data=post_args, follow=True)
            self.response_200(response)
            self.assertTrue("delicious.txt already exists." in str(response.context["form"].errors))
            self.assertFalse("object" in self.last_response.context)

    def test_detail(self):
        """
        Ensure we can see document detail.
        """
        simple_file = SimpleUploadedFile("delicious.txt", self.file_contents)
        document = Document.objects.create(name="Honeycrisp",
                                           author=self.user,
                                           file=simple_file,
                                           )

        with self.login(self.user):
            self.get_check_200(self.detail_urlname, pk=document.pk)
            context_document = self.get_context("object")
            self.assertEqual(context_document, document)

    @mock.patch("django.contrib.messages.success")
    def test_valid_delete(self, mock_messages):
        """
        Ensure we can delete a valid Document.
        """
        simple_file = SimpleUploadedFile("delicious.txt", self.file_contents)
        document = Document.objects.create(name="Honeycrisp",
                                           author=self.user,
                                           file=simple_file,
                                           )

        doc_pk = document.pk
        with self.login(self.user):
            response = self.get(document.delete_url())
            self.response_200(response)
            self.assertTrue('pinax/documents/document_confirm_delete.html' in response.template_name)

            response = self.post("pinax_documents:document_delete", pk=doc_pk, follow=True)
            self.response_200(response)
            self.assertFalse(Document.objects.filter(pk=doc_pk))
            self.assertTrue(mock_messages.called)

            response = self.get(self.download_urlname, pk=document.pk)
            self.response_404(response)

    def test_invalid_delete(self):
        """
        Ensure we get error trying to delete an invalid Document.
        """
        doc_pk = 555
        with self.login(self.user):
            response = self.post("documents_document_delete", pk=doc_pk, follow=True)
            self.response_404(response)

    def test_download(self):
        """
        Ensure the requested Document file is served.
        """
        simple_file = SimpleUploadedFile("delicious.txt", self.file_contents)
        document = Document.objects.create(name="Honeycrisp",
                                           author=self.user,
                                           file=simple_file,
                                           )
        document.save()

        with self.login(self.user):
            # Verify `django.views.static.serve` is called to serve up the file.
            # See related note in .views.DocumentDownload.get().
            with mock.patch("django.views.static.serve") as serve:
                serve.return_value = HttpResponse()
                self.get_check_200(self.download_urlname, pk=document.pk)
                self.assertTrue(serve.called)
