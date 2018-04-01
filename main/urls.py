"""Defines URL patterns for the main piecon site."""

from django.urls import path

from . import views

app_name = 'main'

urlpatterns = [
    # Home page
    path('', views.index, name='index'),

    # Page for showing all games.
    path('games/', views.games, name='games'),

    # Page for showing all pies.
    path('pies/', views.pies, name='pies'),

    # Page for adding a new pie.
    path('pies/new_pie/', views.new_pie, name='new_pie'),

    # About page
    path('about/', views.about, name='about'),

    # Volunteer page
    path('volunteer/', views.volunteer, name='volunteer'),
]
