from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

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
    date_added = models.DateTimeField()
    suppress_from_display = models.BooleanField(default=False)

    # Is just so the Game list on the admin site can easily show if a game will
    # show up on the site or not.
    def is_displayed(self):
        current_year = timezone.now()
        current_year = current_year.year
        return ((self.date_added.year == current_year) and
            (self.suppress_from_display == False))

    is_displayed.admin_order_field = 'date_added'
    is_displayed.boolean = True
    is_displayed.short_description = 'Show on site?'

    def __str__(self):
        """Return a string representation of the model."""
        return self.title

class Convention(models.Model):
    """Data model for representing a specific PieCon convention e.g. year."""
    roman_num = models.CharField(max_length=10)
    tagline = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        """Return a string representation of the model."""
        return "PieCon " + self.roman_num + " - " + self.tagline
