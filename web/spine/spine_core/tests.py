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
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from spine_core.models import Project, Repo, File, Depend, Asset, AssetType, Task, TaskType
from spine_core.misc import Url, url_qs

class Login_and_Logout_Tests(TestCase):

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
        self.assertRedirects(response, reverse('spine_core:project'))
        self.assertTemplateUsed('spine_core/list.html')
        self.assertEqual(response.context['user'].is_authenticated(), True)
        self.assertEqual(response.context['header'], 'Projects')

    def test_login_while_already_logged_in(self):
        """Requesting the login page while already logged in should still display the login page."""
        self.client.login(username='test_user', password='test_password')
        response = self.client.get(reverse('spine_core:login'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('spine_core/login.html')
        self.assertEqual(response.context['user'].is_authenticated(), True)

    def test_logout_while_not_logged_in(self):
        """Logging out when not logged in should redirect to the login page and display the logout message."""
        response = self.client.get(reverse('spine_core:logout'), follow=True)
        self.assertRedirects(response, url_qs(reverse('spine_core:login'), msg='logout'))
        self.assertTemplateUsed('spine_core/login.html')
        self.assertEqual(response.context['user'].is_authenticated(), False)

    def test_logout_while_logged_in(self):
        """Logging out after being logged in should also redirect to the login page and display the logout message."""
        self.client.login(username='test_user', password='test_password')
        response = self.client.get(reverse('spine_core:logout'), follow=True)
        self.assertRedirects(response, url_qs(reverse('spine_core:login'), msg='logout'))
        self.assertTemplateUsed('spine_core/login.html')
        self.assertEqual(response.context['user'].is_authenticated(), False)

    def test_index_while_not_logged_in(self):
        """The index should redirect to the login page when there isn't a user logged in."""
        response = self.client.get(reverse('spine_core:index'), follow=True)
        self.assertRedirects(response, reverse('spine_core:login'))
        self.assertTemplateUsed('spine_core/login.html')
        self.assertEqual(response.context['user'].is_authenticated(), False)

    def test_index_while_logged_in(self):
        """The index should redirect to the projects page when a user is logged in."""
        self.client.login(username='test_user', password='test_password')
        response = self.client.get(reverse('spine_core:index'), follow=True)
        self.assertRedirects(response, reverse('spine_core:project'))
        self.assertTemplateUsed('spine_core/list.html')
        self.assertEqual(response.context['user'].is_authenticated(), True)
        self.assertEqual(response.context['header'], 'Projects')

    def test_other_restricted_page_while_not_logged_in(self):
        """Other restricted pages should redirect to the login page with the 'next' variable set."""
        response = self.client.get(reverse('spine_core:project'), follow=True)
        self.assertRedirects(response, url_qs(reverse('spine_core:login'), next=reverse('spine_core:project')))
        self.assertTemplateUsed('spine_core/login.html')
        self.assertEqual(response.context['user'].is_authenticated(), False)
        
class List_and_Detail_View_Tests(TestCase):

    def setUp(self):
        """Create test model instances and relationships of all types."""
        user_1 = User.objects.create_user('user_1', 'user_1@example.com', 'user_1_password')
        user_2 = User.objects.create_user('user_2', 'user_2@example.com', 'user_2_password')
        project_1 = Project.objects.create(name="project_1")
        project_2 = Project.objects.create(name="project_2")
        project_1.users.add(user_1)
        project_2.users.add(user_2)
        repo_1 = Repo.objects.create(name='repo_1', path='/repo_1/')
        repo_2 = Repo.objects.create(name='repo_2', path='/repo_2/')
        project_1.repos.add(repo_1)
        project_2.repos.add(repo_2)
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

    def test_project_detail_page_with_associated_user(self):
        """The project detail page should only display info if the current user is associated."""
        project = Project.objects.get(name="project_1")
        response = self.client.get(reverse('spine_core:project', kwargs={'pk': project.id}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('spine_core/project.html')
        self.assertEqual(response.context['object'], project)

    def test_repo_detail_page_with_associated_user(self):
        """The repo detail page should only display info if the current user is associated."""
        repo = Repo.objects.get(name="repo_1")
        response = self.client.get(reverse('spine_core:repo', kwargs={'pk': repo.id}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('spine_core/repo.html')
        self.assertEqual(response.context['object'], repo)

    def test_file_detail_page_with_associated_user(self):
        """The file detail page should only display info if the current user is associated."""
        file = File.objects.get(path="file_1")
        response = self.client.get(reverse('spine_core:file', kwargs={'pk': file.id}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('spine_core/file.html')
        self.assertEqual(response.context['object'], file)

    def test_depend_detail_page_with_associated_user(self):
        """The depend detail page should only display info if the current user is associated."""
        file = File.objects.get(path="file_1")
        depend = Depend.objects.get(master_file=file)
        response = self.client.get(reverse('spine_core:depend', kwargs={'pk': depend.id}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('spine_core/depend.html')
        self.assertEqual(response.context['object'], depend)

    def test_asset_detail_page_with_associated_user(self):
        """The asset detail page should only display info if the current user is associated."""
        asset = Asset.objects.get(name="asset_1")
        response = self.client.get(reverse('spine_core:asset', kwargs={'pk': asset.id}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('spine_core/asset.html')
        self.assertEqual(response.context['object'], asset)

    def test_task_detail_page_with_associated_user(self):
        """The task detail page should only display info if the current user is associated."""
        task = Task.objects.get(name="task_1")
        response = self.client.get(reverse('spine_core:task', kwargs={'pk': task.id}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('spine_core/task.html')
        self.assertEqual(response.context['object'], task)

    def test_project_detail_page_with_unassociated_user(self):
        """The project detail page should redirect to the login page if the current user is not associated."""
        project = Project.objects.get(name="project_2")
        response = self.client.get(reverse('spine_core:project', kwargs={'pk': project.id}), follow=True)
        self.assertEqual(response.redirect_chain[-1][1], 302)
        self.assertEqual(Url(response.redirect_chain[-1][0]), Url(url_qs(reverse('spine_core:login'), msg='auth', next=reverse('spine_core:project', kwargs={'pk': project.id}))))
        self.assertTemplateUsed('spine_core/login.html')

    def test_repo_detail_page_with_unassociated_user(self):
        """The repo detail page should redirect to the login page if the current user is not associated."""
        repo = Repo.objects.get(name="repo_2")
        response = self.client.get(reverse('spine_core:repo', kwargs={'pk': repo.id}), follow=True)
        self.assertEqual(response.redirect_chain[-1][1], 302)
        self.assertEqual(Url(response.redirect_chain[-1][0]), Url(url_qs(reverse('spine_core:login'), msg='auth', next=reverse('spine_core:repo', kwargs={'pk': repo.id}))))
        self.assertTemplateUsed('spine_core/login.html')

    def test_file_detail_page_with_unassociated_user(self):
        """The file detail page should redirect to the login page if the current user is not associated."""
        file = File.objects.get(path="file_3")
        response = self.client.get(reverse('spine_core:file', kwargs={'pk': file.id}), follow=True)
        self.assertEqual(response.redirect_chain[-1][1], 302)
        self.assertEqual(Url(response.redirect_chain[-1][0]), Url(url_qs(reverse('spine_core:login'), msg='auth', next=reverse('spine_core:file', kwargs={'pk': file.id}))))
        self.assertTemplateUsed('spine_core/login.html')

    def test_depend_detail_page_with_unassociated_user(self):
        """The depend detail page should redirect to the login page if the current user is not associated."""
        file = File.objects.get(path="file_3")
        depend = Depend.objects.get(master_file=file)
        response = self.client.get(reverse('spine_core:depend', kwargs={'pk': depend.id}), follow=True)
        self.assertEqual(response.redirect_chain[-1][1], 302)
        self.assertEqual(Url(response.redirect_chain[-1][0]), Url(url_qs(reverse('spine_core:login'), msg='auth', next=reverse('spine_core:depend', kwargs={'pk': depend.id}))))
        self.assertTemplateUsed('spine_core/login.html')

    def test_asset_detail_page_with_unassociated_user(self):
        """The asset detail page should redirect to the login page if the current user is not associated."""
        asset = Asset.objects.get(name="asset_2")
        response = self.client.get(reverse('spine_core:asset', kwargs={'pk': asset.id}), follow=True)
        self.assertEqual(response.redirect_chain[-1][1], 302)
        self.assertEqual(Url(response.redirect_chain[-1][0]), Url(url_qs(reverse('spine_core:login'), msg='auth', next=reverse('spine_core:asset', kwargs={'pk': asset.id}))))
        self.assertTemplateUsed('spine_core/login.html')

    def test_task_detail_page_with_unassociated_user(self):
        """The task detail page should redirect to the login page if the current user is not associated."""
        task = Task.objects.get(name="task_2")
        response = self.client.get(reverse('spine_core:task', kwargs={'pk': task.id}), follow=True)
        self.assertEqual(response.redirect_chain[-1][1], 302)
        self.assertEqual(Url(response.redirect_chain[-1][0]), Url(url_qs(reverse('spine_core:login'), msg='auth', next=reverse('spine_core:task', kwargs={'pk': task.id}))))
        self.assertTemplateUsed('spine_core/login.html')