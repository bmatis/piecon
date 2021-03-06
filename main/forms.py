from django import forms

from .models import Pie, Game

class PieForm(forms.ModelForm):
    class Meta:
        model = Pie
        fields = [
            'person_name',
            'text'
            ]
        labels = {
            'person_name': 'Your Name',
            'text': 'Pie (or snack)'
            }
        widgets =  {
            'person_name': forms.TextInput(attrs={'placeholder':
                'Who are you?'}),
            'text': forms.TextInput(attrs={'placeholder':
                'What pie or snack are you bringing?'})
        }

class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = [
            'title',
            'gamemaster',
            'system',
            'num_players',
            'length',
            'description'
            ]
        labels = {
            'title': 'Game Title',
            'gamemaster': 'Gamemaster(s)',
            'system': 'Game System',
            'num_players': 'Number of Players',
            'length': 'Length of game (in hours)',
            'description': 'Description',
            }
        widgets = {
            'title': forms.TextInput(attrs={'placeholder':
                'What\'s the title of your game?'}),
            'gamemaster': forms.TextInput(attrs={'placeholder':
                'Who\'s running the game?'}),
            'system': forms.TextInput(attrs={'placeholder':
                'What game system are you using?'}),
            'num_players': forms.TextInput(attrs={'placeholder':
                '#'}),
            'length': forms.TextInput(attrs={'placeholder':
                '#'}),
            'description': forms.Textarea(attrs={'placeholder':
                'Describe your game.'}),
            }
