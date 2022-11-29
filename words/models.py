from django.db import models

# Create your models here.
from django.urls import reverse


class Words(models.Model):
    word = models.CharField(max_length=255, verbose_name='words yahho')
    translation = models.CharField(max_length=255, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)
    starred = models.BooleanField(default=False)

    # for admin panel
    def __str__(self):
        return self.word

    def get_absolute_url(self):
        return reverse('words', kwargs=('word.id', self.pk))


    class Meta:
        verbose_name = 'words__'
        verbose_name_plural = 'words__'
        ordering = ['-pk',]

