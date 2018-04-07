from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

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

class SettingsPageTests(TestCase):
    def test_settings_page_doesnt_load_for_logged_out_user(self):
        """
        When a logged out visitor tries to access settings page, they are
        redirected to login with a 'next' param that would get them to settings
        once logged in.
        """
        desired_url = reverse('users:settings')
        response = self.client.get(desired_url)

        # Expect to be sent to login screen with a 'next' parameter for
        # getting to the edit screen for the game.
        expected_redirect = reverse('users:login') + '?next=' + desired_url
        self.assertRedirects(response, expected_redirect, status_code=302)

    def test_settings_page_loads_for_logged_in_user(self):
        """
        When a logged in user tries to access settings page, they are able
        to access it.
        """
        # Create test user and login as them.
        createTestUser(username='testuser')
        login = self.client.login(username='testuser', password='12345')

        # Attempt to get to settings page.
        desired_url = reverse('users:settings')
        response = self.client.get(desired_url)

        # Expect successful response.
        self.assertEqual(response.status_code, 200)
