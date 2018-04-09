"""Defines URL patterns for the main piecon site."""

from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'main'

urlpatterns = [
    # Home page
    path('', views.index, name='index'),

    # Page for showing all games.
    # path('games/', views.games, name='games'),
    path('games/', views.GamesView.as_view(), name='games'),

    # Page for creating a new game.
    path('games/new_game', views.new_game, name='new_game'),

    # Page for editing a game.
    path('pies/<int:game_id>/edit_game/', views.edit_game, name='edit_game'),

    # Page for showing all pies.
    # path('pies/', views.pies, name='pies'),
    path('pies/', views.PiesView.as_view(), name='pies'),

    # Page for adding a new pie.
    path('pies/new_pie/', views.new_pie, name='new_pie'),

    # Page for editing a pie.
    path('pies/<int:pie_id>/edit_pie/', views.edit_pie, name='edit_pie'),

    # About page
    # path('about/', views.about, name='about'),
    path('about/', TemplateView.as_view(
        template_name="main/about.html"), name='about'),

    # Volunteer page
    #path('volunteer/', views.volunteer, name='volunteer'),
    path('volunteer/', TemplateView.as_view(
        template_name="main/volunteer.html"), name='volunteer'),
]
