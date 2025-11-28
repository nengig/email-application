from django.db import models
from django.core.validators import validate_email

# Create your models here.

# track emails sent    
class Emails(models.Model):
        subject = models.CharField(max_length=500)
        message = models.TextField(max_length=500)
        email = models.EmailField()
        created_at = models.DateTimeField(auto_now_add=True)
        edited_at = models.DateTimeField(auto_now=True)

        def __str__(self):
            return self.subject

class Attachment(models.Model):
    # foreign key to relate to the Emails model, so each email can have multiple attachments
    email = models.ForeignKey(Emails, related_name='attachments', on_delete=models.CASCADE)
    file = models.FileField(upload_to='email_attachments/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name
