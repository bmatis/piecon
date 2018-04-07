from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
#from django.db import IntegrityError
from datetime import timedelta

from .models import Pie, Game

def createTestUser(username):
    """
    Try to make a user with the given username. If they already exist, just
    return the pre-existing one.
    """
    user, created = User.objects.get_or_create(
        username=username, password='12345')
    return user

def createPie(text, days, username='testuser'):
    """
    Create a pie with the given 'text' and published the given number of
    'days' offset to now (negative for pies published in the past, positive
    for pies published in the future.)
    """
    user = createTestUser(username)
    time = timezone.now() + timedelta(days=days)
    pie = Pie.objects.create(text=text, date_added=time, owner=user)
    return pie

def createGame(title='Test Game', gamemaster='GM', system='Game System',
    num_players='5', length='5', description='Game Description',
    days=0, username='testuser'):
    """
    Create a new game with the given information. Days value provides an offset
    to now (negative for games submitted in the past, positive for future, and
    it defaults to now.) Owner of game defaults to 'testuser' if not specified.
    """
    owner = createTestUser(username)
    time = timezone.now() + timedelta(days=days)
    game = Game.objects.create(
        title=title, owner=owner, gamemaster=gamemaster,
        system=system, num_players=num_players, length=length,
        description=description, date_added=time)
    return game

class GameModelTests(TestCase):
    def test_game_created(self):
        """A new game can be created."""
        game = createGame()
        self.assertEqual(game.title, "Test Game")
        self.assertEqual(game.owner.username, 'testuser')

    def test_game_update(self):
        """A game can be updated."""
        game = createGame()
        game.title = "edited game title"
        self.assertEqual(game.title, 'edited game title')

    def test_is_displayed_when_game_suppressed(self):
        """
        A game can be set to suppressed and then the is_displayed() method
        will return False.
        """
        game = createGame()
        game.suppress_from_display = True
        self.assertEqual(game.is_displayed(), False)

    def test_is_displayed_when_game_is_old(self):
        """
        A game that was submitted over a year ago will have its is_displayed()
        method return False.
        """
        game = createGame(days=-367)
        self.assertEqual(game.is_displayed(), False)

    def test_is_displayed_for_new_game(self):
        """
        A game that is newly created will have its is_displayed() method return
        True.
        """
        game = createGame(days=-5)
        self.assertEqual(game.is_displayed(), True)

class PieModelTests(TestCase):
    def test_pie_created(self):
        """A new pie can be created."""
        pie = createPie(text='test pie', days=0)
        self.assertEqual(pie.text,'test pie')
        self.assertEqual(pie.owner.username, 'testuser')

    def test_pie_update(self):
        """A pie can be updated."""
        pie = createPie(text='original pie', days=0)
        pie.text = 'edited pie'
        self.assertEqual(pie.text, 'edited pie')

class PieListViewTests(TestCase):
    def test_no_pies(self):
        """If no pies exist, an appropriate message is displayed."""
        response = self.client.get(reverse('main:pies'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No pies registered yet")
        self.assertQuerysetEqual(response.context['pies'], [])

    def test_old_pie_does_not_appear(self):
        """
        If only a pie from last year exists, it doesn't appear on the pies list.
        """
        old_pie = createPie(text='old pie', days=-365)
        response = self.client.get(reverse('main:pies'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No pies registered yet")
        self.assertQuerysetEqual(response.context['pies'], [])

    def test_new_pie_appears(self):
        """
        If a pie from the current year exists, it appears on the pie list.
        """
        new_pie = createPie(text='new pie', days=0)
        response = self.client.get(reverse('main:pies'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,
            "<strong>testuser</strong> is bringing <strong>new pie</strong>")
        self.assertQuerysetEqual(response.context['pies'], ['<Pie: new pie>'])

    def test_two_pies(self):
        """
        If more than one pie is created, they both appear on the pie list.
        """
        pie1 = createPie(text='pie1', days=-5)
        pie2 = createPie(text='pie2', days=0, username='different_user')
        response = self.client.get(reverse('main:pies'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,
            "<strong>testuser</strong> is bringing <strong>pie1</strong>")
        self.assertContains(response,
            "<strong>different_user</strong> is bringing <strong>pie2</strong>")

class ContentPagesTests(TestCase):
    """
    Some tests for the 'content pages', e.g. About, Volunteer, etc. Just to
    make sure that the URL mapping is set up right and the pages are rendering.
    """

    def test_about_page_loads(self):
        """Test that the about page appears when requested."""
        response = self.client.get(reverse('main:about'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<h2>About</h2>")

    def test_volunteer_page_load(self):
        """Test that the volunteer page appears when requested."""
        response = self.client.get(reverse('main:volunteer'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<h2>Volunteer</h2>")

    def test_login_page_loads(self):
        """Test that the login page appears when requested."""
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<h2>Login to your account</h2>")
