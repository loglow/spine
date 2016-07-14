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

from spine_core.forms import *
from spine_core.views import *

app_name = 'spine_core'
urlpatterns = [
    url(r'^$', index, name='index'),
    # User auth views
    url(r'^login/$', auth.views.login, {
        'authentication_form': BootstrapAuthForm,
        'template_name': 'spine_core/login.html',
    }, name="login"),
    url(r'^logout/$', auth.views.logout_then_login, name="logout"),
    # Model-based list views
    url(r'^project/$', ProjectListView.as_view(), name='project'),
    url(r'^repo/$', RepoListView.as_view(), name='repo'),
    url(r'^file/$', FileListView.as_view(), name='file'),
    url(r'^depend/$', DependListView.as_view(), name='depend'),
    url(r'^asset/$', AssetListView.as_view(), name='asset'),
    url(r'^task/$', TaskListView.as_view(), name='task'),
    # Model-based detail views
    url(r'^project/(?P<pk>[0-9]+)/$', ProjectDetailView.as_view(), name='project'),
    url(r'^repo/(?P<pk>[0-9]+)/$', RepoDetailView.as_view(), name='repo'),
    url(r'^file/(?P<pk>[0-9]+)/$', FileDetailView.as_view(), name='file'),
    url(r'^depend/(?P<pk>[0-9]+)/$', DependDetailView.as_view(), name='depend'),
    url(r'^asset/(?P<pk>[0-9]+)/$', AssetDetailView.as_view(), name='asset'),
    url(r'^task/(?P<pk>[0-9]+)/$', TaskDetailView.as_view(), name='task'),
]