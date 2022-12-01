from django.contrib import admin

# Register your models here.

from .models import *


class WordsAdmin(admin.ModelAdmin):
    list_display = ('word', 'translation', 'time_created', 'starred', 'user')
    list_display_links = ('word',)
    search_fields = ('word', 'translation')
    list_filter = ('word', 'translation')
    list_editable = ('translation', 'starred')


admin.site.register(Words, WordsAdmin)
