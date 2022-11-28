from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('1', index),
    path('about', about, name='about'),
    path('login', login, name='login'),
]

