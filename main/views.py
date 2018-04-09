from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.views import generic

from .models import Pie, Game, Convention
from .forms import PieForm, GameForm

def get_current_con():
    # Get the current upcoming convention.
    try:
        return Convention.objects.latest('start_date')
    except:
        return None

def index(request):
    """The home page for the PieCon site."""
    current_con = get_current_con()
    context = {'current_con': current_con}
    return render(request, 'main/index.html', context)

class GamesView(generic.ListView):
    """Page for showing all games for the current year's PieCon."""
    template_name = 'main/games.html'
    context_object_name = 'games'

    #current_con = get_current_con()

    def get_queryset(self):
        return Game.objects.filter(
            convention=get_current_con(),
            suppress_from_display=False).order_by('-date_added')


class PiesView(generic.ListView):
    """Page for showing all pies for the current year's PieCon."""
    template_name = 'main/pies.html'
    context_object_name = 'pies'

    #current_con = get_current_con()

    def get_queryset(self):
        #return Pie.objects.filter(date_added__year=current_year).order_by('-date_added')
        return Pie.objects.filter(convention=get_current_con()).order_by('-date_added')


@login_required
def edit_pie(request, pie_id):
    """Page for editing a pie."""

    pie = Pie.objects.get(id=pie_id)
    if pie.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # Initial request; pre-fill form with the current entry.
        form = PieForm(instance=pie)
    else:
        # POST data submitted; process data.
        form = PieForm(instance=pie, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('main:pies'))

    context = {'pie': pie, 'form': form}
    return render(request, 'main/edit_pie.html', context)


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
            new_pie.date_added = timezone.now()
            new_pie.convention = get_current_con()
            new_pie.save()
            return HttpResponseRedirect(reverse('main:pies'))

    context = {'form': form}
    return render(request, 'main/new_pie.html', context)

@login_required
def new_game(request):
    """Add a new game."""

    if request.method != 'POST':
        # No data submitted; create a blank form.
        testing = "this is just a test"
        form = GameForm()
    else:
        # POST data submitted; process data.
        form = GameForm(request.POST)
        if form.is_valid():
            new_game = form.save(commit=False)
            new_game.owner = request.user
            new_game.date_added = timezone.now()
            new_game.convention = get_current_con()
            new_game.save()
            return HttpResponseRedirect(reverse('main:games'))

    context = {'form': form}
    return render(request, 'main/new_game.html', context)

@login_required
def edit_game(request, game_id):
    """Edit an existing game."""

    game = Game.objects.get(id=game_id)
    if game.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # Initial request; pre-fill form with the current entry.
        form = GameForm(instance=game)
    else:
        # POST data submitted; process data.
        form = GameForm(instance=game, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('main:games'))

    context = {'game': game, 'form': form}
    return render(request, 'main/edit_game.html', context)


# DEPRECATED FUNCTIONS


# def about(request):
#     """The about page for the PieCon site."""
#     return render(request, 'main/about.html')

# def volunteer(request):
#     """The volunteer page for the PieCon site."""
#     return render(request, 'main/volunteer.html')

# def games(request):
#     """Page for showing all games for the current year's PieCon."""
#     games = Game.objects.filter(date_added__year=current_year).order_by('-date_added')
#     context = {'games': games}
#     return render(request, 'main/games.html', context)

# def pies(request):
#     """Page for showing all pies for the current year's PieCon."""
#     pies = Pie.objects.filter(date_added__year=current_year).order_by('-date_added')
#     context = {'pies': pies}
#     return render(request, 'main/pies.html', context)
