import smtplib
import ssl
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import *
from django.core.mail import EmailMessage
from .models import Emails, Attachment
from django.views.generic import FormView

class EmailView(FormView):
    template_name = "mail_form.html"
    context_object_name = 'mydata'
    model = Emails
    form_class = EmailForm
    success_url = "/compose/"
    
    def form_valid(self, form):
        my_subject = form.cleaned_data['subject']
        my_message = form.cleaned_data['message']
        my_recipient=form.cleaned_data['email']
        
        # Retrieve credentials from session
        email = self.request.session.get("email")
        password = self.request.session.get("password")
        smtp_server = self.request.session.get("smtp_server")
        port = self.request.session.get("port")
        
        if not email or not password or not smtp_server or not port:
            # If credentials aren't available in session, redirect to login page
            messages.error(self.request, "You need to log in first!")
            return redirect('verify_credentials')
        
        email_msg = EmailMessage(
            subject=my_subject,
            body=my_message,
            to=[my_recipient],
            from_email=email
        )
        
        # attach files if uploaded
        files = self.request.FILES.getlist('attachments')
        for f in files:
            email_msg.attach(f.name, f.read(), f.content_type)
        
        #    save to db 
        email_obj=Emails(
            subject=my_subject,
            message=my_message,
            email=my_recipient
        )
        email_obj.save()
        
        for f in files:
            attachment = Attachment(
                email=email_obj,
                file=f
            )
            attachment.save() 
        
         # Sending the email using smtplib
        try:
            context = ssl.create_default_context()

            # Use SSL if port is 465, or TLS if port is 587
            if port == 465:
                with smtplib.SMTP_SSL(smtp_server, port, context=context) as smtp:
                    smtp.login(email, password)  # Login with the session credentials
                    smtp.sendmail(email, my_recipient, email_msg.message().as_string())
            else:  # Use TLS for port 587
                with smtplib.SMTP(smtp_server, port) as smtp:
                    smtp.starttls(context=context)  # Start TLS encryption
                    smtp.login(email, password)  # Login with the session credentials
                    smtp.sendmail(email, my_recipient, email_msg.message().as_string())

            # If successful, notify the user
            messages.success(self.request, "Email sent successfully!")
            return super().form_valid(form)
        
        except Exception as e:
            # Log exception details for debugging
            print(f"Error: {str(e)}")  # Log the error
            messages.error(self.request, f"Failed to send email: {str(e)}")
            return super().form_invalid(form)

 
    # email history display
    def get_context_data(self, **kwargs):
            # include form context first
            context = super().get_context_data(**kwargs)
            # add all Emails to context
            context['mydata'] = Emails.objects.all().order_by('-created_at')
            return context
   
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
                return redirect("my_form_view")
            except Exception as e:
                messages.error(request, f"Login Failed: {str(e)}")
    else:
        form = EmailCredentialForm()
        
    return render(request, "verify_credential.html",
                  {"form": form})
