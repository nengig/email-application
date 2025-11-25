import smtplib
import ssl
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import EmailCredentialForm


# Create your views here.

def verify_credentials(request):
    message = None

    if request.method == "POST":
        form = EmailCredentialForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            smtp_server = form.cleaned_data["smtp_server"]
            port = form.cleaned_data["port"]

            context = ssl.create_default_context()
            try:
                if port == 465:
                    # SSL connection
                    with smtplib.SMTP_SSL(smtp_server, port, context=context) as smtp:
                        smtp.login(email, password)
                else:
                    # TLS connection
                    with smtplib.SMTP(smtp_server, port) as smtp:
                        smtp.starttls(context=context)
                        smtp.login(email, password)

                # Save session to use to send email later
                request.session["email"] = email
                request.session["password"] = password
                request.session["smtp_server"] = smtp_server
                request.session["port"] = port

                messages.success(request, "Login Succesful")
                return redirect("compose_email")
            except Exception as e:
                messages.error(request, f"Login Failed: {str(e)}")
    else:
        form = EmailCredentialForm()

    return render(request, "verify_credential.html",
                  {"form": form})
