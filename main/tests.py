from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.urls import reverse
#from django.db import IntegrityError
from datetime import timedelta

from .models import Pie, Game, Convention

def createConvention(roman_num='I', tagline="Tagline", days=0):
    """
    Make a convention that we can assign new games and pies to. Times based on
    the given 'days' offset, use negative value to be in the past, positive
    to be in the future.
    """
    start_date = timezone.now() + timedelta(days=days)
    end_date = start_date + timedelta(days=3)
    convention = Convention.objects.create(
        roman_num=roman_num,
        tagline=tagline,
        start_date=start_date,
        end_date=end_date)
    return convention

def createTestUser(username):
    """
    Try to make a user with the given username. If they already exist, just
    return the pre-existing one.
    """
    # TODO: refactor how I'm dealing with user creation for these tests. It's
    # kind of kludgey right now...
    user, created = User.objects.get_or_create(
        username=username)
    if created:
        user.set_password('12345')
        user.save()
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

class ConventionModelTests(TestCase):
    def test_create_convention(self):
        new_convention = createConvention()
        self.assertEqual(new_convention.tagline, 'Tagline')

class GameModelTests(TestCase):
    def setUp(self):
        old_con = createConvention(roman_num='I', tagline="OldCon", days=-365)
        current_con = createConvention(roman_num='II', tagline="NewCon", days=10)

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

    def test_is_displayed_function_when_game_suppressed(self):
        """
        A game can be set to suppressed and then the is_displayed() method
        will return False.
        """
        game = createGame()
        current_con = Convention.objects.latest('start_date')
        game.convention = current_con
        game.suppress_from_display = True
        self.assertEqual(game.is_displayed(), False)

    def test_is_displayed_function_when_game_is_old(self):
        """
        A game that was part of an old convention will have its is_displayed()
        method return False.
        """
        game = createGame(days=-367)
        old_con = Convention.objects.get(roman_num='I')
        game.convention = old_con
        self.assertEqual(game.convention.roman_num, 'I')
        self.assertEqual(Convention.objects.latest('start_date').roman_num, 'II')
        self.assertEqual(game.is_displayed(), False)

    def test_is_displayed_function_for_new_game(self):
        """
        A game that is newly created will have its is_displayed() method return
        True.
        """
        game = createGame()
        current_con = Convention.objects.latest('start_date')
        game.convention = current_con
        self.assertEqual(game.is_displayed(), True)

class GameEditViewTests(TestCase):
    def test_cannot_access_edit_game_when_logged_out(self):
        """
        Trying to access edit screen for a user's game when not logged in will
        redirect user to login page that has a next parameter for getting back
        to edit screen after successful login.
        """
        # Create a new game, with default values.
        game = createGame()

        # Attempt to access edit screen for the newly created game.
        desired_url = reverse('main:edit_game', kwargs={'game_id': game.id})
        response = self.client.get(desired_url)

        # Expect to be sent to login screen with a 'next' parameter for
        # getting to the edit screen for the game.
        expected_redirect = reverse('users:login') + '?next=' + desired_url
        self.assertRedirects(response, expected_redirect, status_code=302)

    def test_user_cannot_access_edit_for_another_users_game(self):
        """
        Trying to access edit screen for another user's game when logged in as
        someone else should return a 404 error.
        """
        # Create a new game, by a user with username 'user1'
        game = createGame(username='user1')

        # Create a second user, with username 'user2'
        user2 = createTestUser(username='user2')

        # Login as user2
        login = self.client.login(username='user2', password='12345')

        # Attempt to access the edit screen for the game created by user1.
        desired_url = reverse('main:edit_game', kwargs={'game_id': game.id})
        response = self.client.get(desired_url)

        # Expect to get a 404 error.
        self.assertEqual(response.status_code, 404)

    def test_user_can_access_edit_for_own_game(self):
        """
        Trying to access edit screen for your own game will work.
        """
        # Create a new game, by a user with username 'user1'
        game = createGame(username='user1')

        # Login as user1
        self.client.login(username='user1', password='12345')

        # Attempt to access the edit screen for the game created by user1.
        desired_url = reverse('main:edit_game', kwargs={'game_id': game.id})
        response = self.client.get(desired_url)

        # Expect to get a success response.
        self.assertEqual(response.status_code, 200)

class GameCreateViewTests(TestCase):
    def test_user_cannot_access_create_game_when_logged_out(self):
        """
        When not logged in, attempting to access the page for creating a new
        game should result in redirect to login page with a 'next' param for
        getting to new game page once logged in.
        """
        # Attempt to access creat game screen.
        desired_url = reverse('main:new_game')
        response = self.client.get(desired_url)

        # Expect to be sent to login screen with a 'next' parameter for
        # getting to the new game screen.
        expected_redirect = reverse('users:login') + '?next=' + desired_url
        self.assertRedirects(response, expected_redirect, status_code=302)

    def test_user_can_access_create_game_when_logged_in(self):
        """
        When logged in, user can successfully access screen for creating a new
        game.
        """
        # Create a test user and login as them.
        testuser = createTestUser(username='testuser')
        self.client.login(username='testuser', password='12345')

        # Attempt to access create game screen.
        desired_url = reverse('main:new_game')
        response = self.client.get(desired_url)

        # Expect to receive a success response.
        self.assertEqual(response.status_code, 200)

class PieModelTests(TestCase):
    def setUp(self):
        old_con = createConvention(roman_num='I', tagline="OldCon", days=-365)
        current_con = createConvention(roman_num='II', tagline="NewCon", days=10)

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
    def setUp(self):
        old_con = createConvention(roman_num='I', tagline="OldCon", days=-365)
        current_con = createConvention(roman_num='II', tagline="NewCon", days=10)

    def test_no_pies(self):
        """If no pies exist, an appropriate message is displayed."""
        response = self.client.get(reverse('main:pies'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No pies registered yet")
        self.assertQuerysetEqual(response.context['pies'], [])

    def test_old_pie_does_not_appear(self):
        """
        If only a pie from a prior con exists, the pie list is empty.
        """
        old_con = Convention.objects.get(roman_num='I')

        old_pie = createPie(text='old pie', days=-365)
        old_pie.convention = old_con
        old_pie.save()

        response = self.client.get(reverse('main:pies'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No pies registered yet")
        self.assertQuerysetEqual(response.context['pies'], [])

    def test_new_pie_appears(self):
        """
        If a pie from the current year exists, it appears on the pie list.
        """
        new_pie = createPie(text='new pie', days=0)
        new_pie.convention = Convention.objects.latest('start_date')
        new_pie.save()

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
        current_con = Convention.objects.latest('start_date')
        pie1.convention = current_con
        pie2.convention = current_con
        pie1.save()
        pie2.save()

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
