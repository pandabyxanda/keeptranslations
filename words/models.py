from django.db import models

# Create your models here.

class Words(models.Model):
    word = models.CharField(max_length=255)
    translation = models.CharField(max_length=255, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)
    starred = models.BooleanField(default=False)


