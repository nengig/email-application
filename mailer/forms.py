from django import forms


class EmailCredentialForm(forms.Form):
    email = forms.EmailField(label="Email Address")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    smtp_server = forms.CharField(label="SMTP SERVER", initial="smtp.gmail.com")
    port = forms.IntegerField(label="Port", initial=465)
