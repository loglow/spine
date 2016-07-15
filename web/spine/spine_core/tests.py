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
        
class UserTests(TestCase):

    def setUp(self):
        """Create test model instances and relationships of all necessary types."""
        user_1 = User.objects.create_user('user_1', 'user_1@example.com', 'user_1_password')
        user_2 = User.objects.create_user('user_2', 'user_2@example.com', 'user_2_password')
        project_1 = Project.objects.create(name="project_1")
        project_2 = Project.objects.create(name="project_2")
        project_1.users.add(user_1)
        repo_1 = Repo.objects.create(name='repo_1', path='/repo_1/')
        repo_2 = Repo.objects.create(name='repo_2', path='/repo_2/')
        project_1.repos.add(repo_1)
        file_1 = File.objects.create(path='file_1', repo=repo_1)
        file_2 = File.objects.create(path='file_2', repo=repo_1)
        file_3 = File.objects.create(path='file_3', repo=repo_2)
        file_4 = File.objects.create(path='file_4', repo=repo_2)
        depend_1 = Depend.objects.create(master_file=file_1, depend_file=file_2)
        depend_2 = Depend.objects.create(master_file=file_3, depend_file=file_4)
        asset_type_1 = AssetType.objects.create(name='asset_type_1')
        asset_1 = Asset.objects.create(name='asset_1', type=asset_type_1)
        asset_2 = Asset.objects.create(name='asset_2', type=asset_type_1)
        asset_1.files.add(file_1, file_2)
        asset_2.files.add(file_3, file_4)
        task_type_1 = TaskType.objects.create(name='task_type_1')
        task_1 = Task.objects.create(name='task_1', type=task_type_1)
        task_2 = Task.objects.create(name='task_2', type=task_type_1)
        task_1.assets.add(asset_1)
        task_2.assets.add(asset_2)
        self.client.login(username='user_1', password='user_1_password')

    def test_project_list_page(self):
        """The project list page should only display projects associated with the current user."""
        response = self.client.get(reverse('spine_core:project'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('spine_core/list.html')
        self.assertEqual(response.context['header'], 'Projects')
        self.assertQuerysetEqual(response.context['object_list'], ['<Project: project_1>'])

    def test_repo_list_page(self):
        """The repo list page should only display repos associated with the current user."""
        response = self.client.get(reverse('spine_core:repo'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('spine_core/list.html')
        self.assertEqual(response.context['header'], 'Repos')
        self.assertQuerysetEqual(response.context['object_list'], ['<Repo: repo_1>'])

    def test_file_list_page(self):
        """The file list page should only display files associated with the current user."""
        response = self.client.get(reverse('spine_core:file'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('spine_core/list.html')
        self.assertEqual(response.context['header'], 'Files')
        self.assertQuerysetEqual(response.context['object_list'], ['<File: file_1>', '<File: file_2>'], ordered=False)

    def test_depend_list_page(self):
        """The depend list page should only display depends associated with the current user."""
        response = self.client.get(reverse('spine_core:depend'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('spine_core/list.html')
        self.assertEqual(response.context['header'], 'Depends')
        self.assertQuerysetEqual(response.context['object_list'], ['<Depend: file_1 \u2192 file_2>'])

    def test_asset_list_page(self):
        """The asset list page should only display assets associated with the current user."""
        response = self.client.get(reverse('spine_core:asset'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('spine_core/list.html')
        self.assertEqual(response.context['header'], 'Assets')
        self.assertQuerysetEqual(response.context['object_list'], ['<Asset: asset_1>'])

    def test_task_list_page(self):
        """The task list page should only display tasks associated with the current user."""
        response = self.client.get(reverse('spine_core:task'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('spine_core/list.html')
        self.assertEqual(response.context['header'], 'Tasks')
        self.assertQuerysetEqual(response.context['object_list'], ['<Task: task_1>'])