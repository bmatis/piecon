"""Defines URL patterns for the main piecon site."""

from django.urls import path

from . import views

urlpatterns = [
    # Home page
    path('', views.index, name='index')
]
