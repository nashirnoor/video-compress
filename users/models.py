from django.contrib.auth.models import AbstractUser
from django.db import models
from google.cloud import datastore

class User(AbstractUser):
    mobile = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    otp = models.CharField(max_length=6, null=True, blank=True)

    def save(self, *args, **kwargs):
        client = datastore.Client()
        key = client.key('User', self.username)
        entity = datastore.Entity(key=key)
        entity.update({
            'mobile': self.mobile,
            'email': self.email,
            'name': self.name,
            'otp': self.otp,
        })
        client.put(entity)

class Video(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='videos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        client = datastore.Client()
        key = client.key('Video', self.id)
        entity = datastore.Entity(key=key)
        entity.update({
            'user': self.user.username,
            'title': self.title,
            'file': str(self.file),
            'uploaded_at': self.uploaded_at,
        })
        client.put(entity)