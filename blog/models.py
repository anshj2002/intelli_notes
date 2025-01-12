from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now) 
    author = models.ForeignKey(User, on_delete=models.CASCADE) 
    image = models.ImageField(default='',upload_to='images',blank=True,null=True)
    audio = models.FileField(default='',upload_to='audio',blank=True,null=True)

    def __str__(self):
        return self.title

    # defining a URL for a new entry
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
