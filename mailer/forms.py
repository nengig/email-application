from django import forms
from django.forms import ClearableFileInput, ModelForm
from .models import *


class EmailCredentialForm(forms.Form):
    email = forms.EmailField(label="Email Address", required=True)
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    smtp_server = forms.CharField(label="SMTP SERVER", initial="smtp.gmail.com")
    port = forms.IntegerField(label="Port", initial=465)

#  widget to handle multiple file uploads
class MultipleFileInput(ClearableFileInput):
    allow_multiple_selected = True

# Custom FileField to handle multiple file uploads
class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        # handle multiple files (list/tuple of files)
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result
   
class EmailForm(forms.Form):
    email = forms.EmailField()
    subject = forms.CharField(max_length=500)
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}))
    
    attachments = MultipleFileField(
        required=False, 
        label="Attachments"
    )
   
    

