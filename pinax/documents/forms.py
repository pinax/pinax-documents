from django import forms

try:
    from account.utils import user_display
except ImportError:
    def user_display(user):
        return user.username

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
