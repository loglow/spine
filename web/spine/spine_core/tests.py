# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from spine_core.models import *

class AuthTests(TestCase):

    def setUp(self):
        """Create a test user."""
        test_user = User.objects.create_user('test_user', 'test_user@example.com', 'test_password')

    def test_login_with_fake_username(self):
        """Logging in with a username that doesn't exist should leave us at the login page."""
        response = self.client.post(reverse('spine_core:login'), {'username': 'fake_user', 'password': 'test_password'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('spine_core/login.html')
        self.assertEqual(response.context['user'].is_authenticated(), False)

    def test_login_with_wrong_password(self):
        """Logging in with an incorrect password should leave us at the login page."""
        response = self.client.post(reverse('spine_core:login'), {'username': 'test_user', 'password': 'wrong_password'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('spine_core/login.html')
        self.assertEqual(response.context['user'].is_authenticated(), False)

    def test_login_with_correct_password(self):
        """Logging in with the correct username and password should redirect us to the projects page."""
        response = self.client.post(reverse('spine_core:login'), {'username': 'test_user', 'password': 'test_password'}, follow=True)
        self.assertRedirects(response, '/project/')
        self.assertTemplateUsed('spine_core/list.html')
        self.assertEqual(response.context['user'].is_authenticated(), True)
        self.assertEqual(response.context['header'], 'Projects')

    def test_login_while_already_logged_in(self):
        """Requesting the login page while already logged in should redirect us to the projects page.
        Since we are using the built-in login view, we handle the redirect in the login.html template,
        which means we won't see a 302 redirect in this case, and both templates will appear to be used."""
        self.client.login(username='test_user', password='test_password')
        response = self.client.get(reverse('spine_core:login'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('spine_core/login.html')
        self.assertTemplateUsed('spine_core/list.html')
        self.assertEqual(response.context['user'].is_authenticated(), True)

    def test_logout_while_not_logged_in(self):
        """Logging out when not logged in should redirect to the login page."""
        response = self.client.get(reverse('spine_core:logout'), follow=True)
        self.assertRedirects(response, '/login/')
        self.assertTemplateUsed('spine_core/login.html')
        self.assertEqual(response.context['user'].is_authenticated(), False)

    def test_logout_while_logged_in(self):
        """Logging out after being logged in should also redirect to the login page."""
        self.client.login(username='test_user', password='test_password')
        response = self.client.get(reverse('spine_core:logout'), follow=True)
        self.assertRedirects(response, '/login/')
        self.assertTemplateUsed('spine_core/login.html')
        self.assertEqual(response.context['user'].is_authenticated(), False)

    def test_index_while_not_logged_in(self):
        """The index should redirect to the login page when there isn't a user logged in."""
        response = self.client.get(reverse('spine_core:index'), follow=True)
        self.assertRedirects(response, '/login/')
        self.assertTemplateUsed('spine_core/login.html')
        self.assertEqual(response.context['user'].is_authenticated(), False)

    def test_index_while_logged_in(self):
        """The index should redirect to the projects page when a user is logged in."""
        self.client.login(username='test_user', password='test_password')
        response = self.client.get(reverse('spine_core:index'), follow=True)
        self.assertRedirects(response, '/project/')
        self.assertTemplateUsed('spine_core/list.html')
        self.assertEqual(response.context['user'].is_authenticated(), True)
        self.assertEqual(response.context['header'], 'Projects')

    def test_other_restricted_page_while_not_logged_in(self):
        """Other restricted pages should redirect to the login page with the 'next' variable set."""
        response = self.client.get(reverse('spine_core:project'), follow=True)
        self.assertRedirects(response, '/login/?next=/project/')
        self.assertTemplateUsed('spine_core/login.html')
        self.assertEqual(response.context['user'].is_authenticated(), False)
        
class ProjectTests(TestCase):

    def setUp(self):
        """Create a user and two projects, assign the user to only one of the projects, then login."""
        test_user = User.objects.create_user('test_user', 'test_user@example.com', 'test_password')
        test_project_without_user = Project.objects.create(name="test_project_without_user")
        test_project_with_user = Project.objects.create(name="test_project_with_user")
        test_project_with_user.users.add(test_user)
        self.client.login(username='test_user', password='test_password')

    def test_projects_list_page(self):
        """The projects list page should only display projects that the current user is associated with."""
        response = self.client.get(reverse('spine_core:project'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('spine_core/list.html')
        self.assertEqual(response.context['header'], 'Projects')
        self.assertQuerysetEqual(response.context['object_list'], ['<Project: test_project_with_user>'])