from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required

from .models import Pie, Game
from .forms import PieForm

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

@login_required
def new_pie(request):
    """Add a new pie."""
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = PieForm()
    else:
        # POST data submitted; process data.
        form = PieForm(request.POST)
        if form.is_valid():
            new_pie = form.save(commit=False)
            new_pie.owner = request.user
            new_pie.save()
            return HttpResponseRedirect(reverse('main:pies'))

    context = {'form': form}
    return render(request, 'main/new_pie.html', context)


def about(request):
    """The about page for the PieCon site."""
    return render(request, 'main/about.html')

def volunteer(request):
    """The volunteer page for the PieCon site."""
    return render(request, 'main/volunteer.html')
