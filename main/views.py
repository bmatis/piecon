from django.shortcuts import render
from .models import Pie
from .models import Game

current_year = 2018

def index(request):
    """The home page for the PieCon site."""
    return render(request, 'main/index.html')

def games(request):
    """Page for showing all games for the current year's PieCon."""
    games = Game.objects.filter(date_added__year=current_year).order_by('-date_added')
    context = {'games': games}
    return render(request, 'main/games.html', context)

def pies(request):
    """Page for showing all pies for the current year's PieCon."""
    pies = Pie.objects.filter(date_added__year=current_year).order_by('-date_added')
    context = {'pies': pies}
    return render(request, 'main/pies.html', context)

def about(request):
    """The about page for the PieCon site."""
    return render(request, 'main/about.html')

def volunteer(request):
    """The volunteer page for the PieCon site."""
    return render(request, 'main/volunteer.html')
