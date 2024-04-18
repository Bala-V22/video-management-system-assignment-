from django.db import models
from django.contrib.auth.models import User
import uuid


class Video(models.Model):
    name = models.CharField(max_length=100)
    video_file = models.FileField(upload_to='videos')
    url = models.CharField(max_length=255)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
