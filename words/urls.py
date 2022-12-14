from django.urls import path

from .views import *

urlpatterns = [
    # path('', index, name='home'),
    path('', index, name='home'),
    # path('1', index),
    path('saved/', saved, name='saved'),
    path('about/', about, name='about'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
]

