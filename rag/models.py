from django.db import models

class Document(models.Model):

    filename=models.CharField(max_length=255)

    uploaded_at=models.DateTimeField(auto_now_add=True)

    file=models.FileField(upload_to="documents/")