from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sex', views.sex, name='sex_controller'),
    path('type', views.type, name='type_controller'),
    path('artist', views.artist, name='artist_controller'),
    path('pm', views.pm, name='pm_controller'),
    path('artwork', views.artwork, name='artwork_controller')
]