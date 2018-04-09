from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

class Convention(models.Model):
    """Data model for representing a specific PieCon convention e.g. year."""
    roman_num = models.CharField(max_length=10)
    tagline = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        """Return a string representation of the model."""
        return "PieCon " + self.roman_num

    def description(self):
        """
        Return a description with the tagline, like:
        PieCon XV - Pies of Future Past
        """
        return "PieCon " + self.roman_num + " - " + self.tagline

    def date_range_short(self):
        """
        Return timerange of convention in format like: April 20 - 22, 2018
        """
        start = self.start_date.strftime('%B %d')

        # check if end date in same month as start date and don't repeat the
        # month twice. Otherwise, show the end date's month as well.
        if self.end_date.month == self.start_date.month:
            end = self.end_date.strftime('%d')
        else:
            end = self.end_date.strftime('%B %d')

        year = self.end_date.strftime('%Y')
        timerange = start + " - " + end + ", " + year
        return timerange

    def date_range_long(self):
        """
        Return timerange of convention that includes the day of the week, like:
        Friday, April 20 - Sunday, April 22, 2018
        """
        start = self.start_date.strftime('%A, %B %d')
        end = self.end_date.strftime('%A, %B %d')
        year = self.end_date.strftime('%Y')
        timerange = start + " - " + end + ", " + year
        return timerange

class Pie(models.Model):
    """Data model for Pies/Snacks"""
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    convention = models.ForeignKey(Convention, on_delete=models.SET_NULL, blank=True, null=True)

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
    convention = models.ForeignKey(Convention, on_delete=models.SET_NULL, blank=True, null=True)

    # Is just so the Game list on the admin site can easily show if a game will
    # show up on the site or not.
    def is_displayed(self):
        current_year = timezone.now()
        current_year = current_year.year
        #current_con = Convention.objects.all().order_by('-start_date')[:1]
        current_con = Convention.objects.latest('start_date')


        return ((self.convention == current_con) and
            (self.suppress_from_display == False))
        return current_con

    is_displayed.admin_order_field = 'date_added'
    is_displayed.boolean = True
    is_displayed.short_description = 'Show on site?'

    def __str__(self):
        """Return a string representation of the model."""
        return self.title
