from django.db import models
from django.contrib.auth.models import User

class Pie(models.Model):
    """Data model for Pies/Snacks"""
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """Return a string representation of the model."""
        return self.text

class Game(models.Model):
    """Data model for Games."""
    title = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    gamemaster = models.CharField(max_length=200)
    system = models.CharField(max_length=200)
    num_players = models.CharField(max_length=6)
    length = models.CharField(max_length=2)
    description = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a string representation of the model."""
        return self.title
