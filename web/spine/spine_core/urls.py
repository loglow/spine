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

from django.conf.urls import url
from django.contrib import auth
from django.contrib.auth.decorators import login_required

from spine_core import views, forms, models

AUTH_FILTERS = {
    'project': 'users',
    'repo': 'project__users',
    'file': 'repo__project__users',
    'asset': 'files__repo__project__users',
    'task': 'assets__files__repo__project__users',
}

app_name = 'spine_core'
urlpatterns = [
    url(r'^$',
        login_required(
            views.index,
            redirect_field_name=None,
        ), name='index',
    ),
    url(r'^login/$',
        auth.views.login, {
            'authentication_form': forms.BootstrapAuthForm,
            'template_name': 'spine_core/login.html',
        }, name="login",
    ),
    url(r'^logout/$',
        auth.views.logout_then_login, {
            'login_url': '/login/?msg=logout',
        }, name="logout",
    ),
    url(r'^project/$',
        login_required(views.ProjectListView.as_view(
            model=models.Project,
            template_name='spine_core/list/project.html',
            filter=AUTH_FILTERS['project'],
        )), name='project',
    ),
    url(r'^repo/$',
        login_required(views.RepoListView.as_view(
            model=models.Repo,
            template_name='spine_core/list/repo.html',
            filter=AUTH_FILTERS['repo'],
        )), name='repo',
    ),
    url(r'^file/$',
        login_required(views.FileListView.as_view(
            model=models.File,
            template_name='spine_core/list/file.html',
            filter=AUTH_FILTERS['file'],
        )), name='file',
    ),
    url(r'^asset/$',
        login_required(views.AssetListView.as_view(
            model=models.Asset,
            template_name='spine_core/list/asset.html',
            filter=AUTH_FILTERS['asset'],
        )), name='asset',
    ),
    url(r'^task/$',
        login_required(views.TaskListView.as_view(
            model=models.Task,
            template_name='spine_core/list/task.html',
            filter=AUTH_FILTERS['task'],
        )), name='task',
    ),
    url(r'^project/(?P<pk>[0-9]+)/$',
        login_required(views.ProjectDetailView.as_view(
            model=models.Project,
            template_name='spine_core/detail/project.html',
            filter=AUTH_FILTERS['project'],
        )), name='project',
    ),
    url(r'^repo/(?P<pk>[0-9]+)/$',
        login_required(views.RepoDetailView.as_view(
            model=models.Repo,
            template_name='spine_core/detail/repo.html',
            filter=AUTH_FILTERS['repo'],
        )), name='repo',
    ),
    url(r'^file/(?P<pk>[0-9]+)/$',
        login_required(views.FileDetailView.as_view(
            model=models.File,
            template_name='spine_core/detail/file.html',
            filter=AUTH_FILTERS['file'],
        )), name='file',
    ),
    url(r'^asset/(?P<pk>[0-9]+)/$',
        login_required(views.AssetDetailView.as_view(
            model=models.Asset,
            template_name='spine_core/detail/asset.html',
            filter=AUTH_FILTERS['asset'],
        )), name='asset',
    ),
    url(r'^task/(?P<pk>[0-9]+)/$',
        login_required(views.TaskDetailView.as_view(
            model=models.Task,
            template_name='spine_core/detail/task.html',
            filter=AUTH_FILTERS['task'],
        )), name='task',
    ),
]