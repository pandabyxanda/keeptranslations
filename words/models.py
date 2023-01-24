from django.contrib.sessions.models import Session
from django.db import models

# Create your models here.
from django.urls import reverse

# to get django user model and add it to my model Words
from django.contrib.auth.models import User


class Words(models.Model):
    word = models.CharField(max_length=255, verbose_name='words yahho')
    translation = models.CharField(max_length=255, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)
    starred = models.BooleanField(default=False)

    starred1 = models.BooleanField(default=False)
    learned = models.BooleanField(default=False)
    learning_rating = models.IntegerField(default=10, blank=True)

    user_and_session = models.ForeignKey('User_And_Session', on_delete=models.PROTECT, blank=True, default=1)

    # for admin panel
    def __str__(self):
        return self.word

    def get_absolute_url(self):
        return reverse('words', kwargs=('word.id', self.pk))


    class Meta:
        verbose_name = 'words__'
        verbose_name_plural = 'words__'
        ordering = ['-pk',]

class User_And_Session(models.Model):
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, blank=True, default=None)
    session = models.ForeignKey(Session, null=True, on_delete=models.SET_NULL, blank=True, default=None)

# class Category(models.Model):
#     name = models.CharField(max_length=100, db_index=True, verbose_name='Категория')
#     slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')