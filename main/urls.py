"""Defines URL patterns for the main piecon site."""

from django.urls import path

from . import views

app_name = 'main'

urlpatterns = [
    # Home page
    path('', views.index, name='index'),

    # Page for showing all games.
    # path('games/', views.games, name='games'),
    path('games/', views.GamesView.as_view(), name='games'),

    # Page for showing all pies.
    # path('pies/', views.pies, name='pies'),
    path('pies/', views.PiesView.as_view(), name='pies'),

    # Page for adding a new pie.
    path('pies/new_pie/', views.new_pie, name='new_pie'),

    # Page for editing a pie.
    path('pies/edit_pie/<int:pie_id>/', views.edit_pie, name='edit_pie'),

    # About page
    path('about/', views.about, name='about'),

    # Volunteer page
    path('volunteer/', views.volunteer, name='volunteer'),
]
