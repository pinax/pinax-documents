from django import forms

try:
    from account.utils import user_display
except ImportError:
    def user_display(user):
        return user.username

from .models import Folder


class FolderCreateForm(forms.Form):

    name = forms.CharField(max_length=140)
    parent = forms.ModelChoiceField(
        queryset=Folder.objects.none(),
        widget=forms.HiddenInput,
        required=False,
    )

    def __init__(self, *args, **kwargs):
        folders = kwargs.pop("folders")
        super(FolderCreateForm, self).__init__(*args, **kwargs)
        self.fields["parent"].queryset = folders


class DocumentCreateForm(forms.Form):

    folder = forms.ModelChoiceField(
        queryset=Folder.objects.none(),
        widget=forms.HiddenInput,
        required=False,
    )
    file = forms.FileField()

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
