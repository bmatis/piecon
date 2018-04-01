from django import forms

from .models import Pie, Game

class PieForm(forms.ModelForm):
    class Meta:
        model = Pie
        fields = ['text']
        labels = {'text': ''}
