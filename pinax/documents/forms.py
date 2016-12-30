from django import forms

try:
    from account.utils import user_display
except ImportError:
    def user_display(user):
        return user.username

from .hooks import hookset
from .models import (
    Document,
    Folder,
)


class FolderCreateForm(forms.ModelForm):

    class Meta:
        model = Folder
        fields = ["name", "parent"]
        widgets = {
            "parent": forms.HiddenInput,
        }

    def clean(self):
        name = self.cleaned_data["name"]
        parent = self.cleaned_data.get("parent")
        if Folder.already_exists(name, parent):
            raise forms.ValidationError("{} already exists.".format(name))

    def __init__(self, *args, **kwargs):
        folders = kwargs.pop("folders")
        super(FolderCreateForm, self).__init__(*args, **kwargs)
        self.fields["parent"].queryset = folders


class DocumentCreateForm(forms.ModelForm):

    class Meta:
        model = Document
        fields = ["folder", "file"]
        widgets = {
            "folder": forms.HiddenInput,
        }

    def __init__(self, *args, **kwargs):
        folders = kwargs.pop("folders")
        self.storage = kwargs.pop("storage")
        super(DocumentCreateForm, self).__init__(*args, **kwargs)
        self.fields["folder"].queryset = folders

    def clean_file(self):
        value = self.cleaned_data["file"]
        if (value.size + self.storage.bytes_used) > self.storage.bytes_total:
            raise forms.ValidationError("File will exceed storage capacity.")
        return value

    def clean(self):
        if "file" in self.cleaned_data:
            name = self.cleaned_data.get("file").name
            folder = self.cleaned_data.get("folder")
            if Document.already_exists(name, folder):
                raise forms.ValidationError(
                    hookset.already_exists_validation_message(name, folder)
                )


class DocumentCreateFormWithName(DocumentCreateForm):

    class Meta:
        model = Document
        fields = ["folder", "file", "name"]
        widgets = {
            "folder": forms.HiddenInput,
        }


class UserMultipleChoiceField(forms.ModelMultipleChoiceField):

    def label_from_instance(self, obj):
        return user_display(obj)


class FolderShareForm(forms.Form):

    participants = UserMultipleChoiceField(
        queryset=None,
        widget=forms.SelectMultiple(
            attrs={
                "class": "span6",
                "data-placeholder": "Choose participants... "
            }
        )
    )


class ColleagueFolderShareForm(FolderShareForm):

    def __init__(self, *args, **kwargs):
        colleagues = kwargs.pop("colleagues")
        super(ColleagueFolderShareForm, self).__init__(*args, **kwargs)
        self.fields["participants"].queryset = colleagues
