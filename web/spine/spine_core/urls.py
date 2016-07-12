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

from . import views

app_name = 'spine_core'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^project/(?P<pk>[0-9]+)/$', views.ProjectView.as_view(), name='project'),
    url(r'^repo/(?P<pk>[0-9]+)/$', views.RepoView.as_view(), name='repo'),
    url(r'^file/(?P<pk>[0-9]+)/$', views.FileView.as_view(), name='file'),
    url(r'^depend/(?P<pk>[0-9]+)/$', views.DependView.as_view(), name='depend'),
    url(r'^asset/(?P<pk>[0-9]+)/$', views.AssetView.as_view(), name='asset'),
    url(r'^task/(?P<pk>[0-9]+)/$', views.TaskView.as_view(), name='task'),
]