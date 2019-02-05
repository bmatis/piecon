"""Defines URL patterns for users"""

from django.urls import path
from django.contrib.auth.views import login

from . import views

app_name = 'users'

urlpatterns = [
    # Login page
    path('login/', login, {'template_name': 'users/login.html'}, name='login'),

    # Logout action
    path('logout/', views.logout_view, name='logout'),

    # Create a new account
    path('new_account/', views.new_account, name='new_account'),

    # Get to the user's settings page
    path('settings/', views.settings, name='settings'),

    # Get to the user's change password page
    path('change_password/', views.change_password, name='change_password'),
]
