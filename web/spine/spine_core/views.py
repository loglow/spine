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

from django.shortcuts import render
from django.views.generic import DetailView, ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

from spine_core.models import *

@login_required(redirect_field_name=None)
def index(request):
    return redirect('spine_core:project')

class ProjectListView(LoginRequiredMixin, ListView):
    template_name = 'spine_core/list.html'

    def get_queryset(self):
        return Project.objects.filter(users=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(ProjectListView, self).get_context_data(**kwargs)
        context['header'] = 'Projects'
        context['object_url'] = 'spine_core:project'
        return context

class RepoListView(LoginRequiredMixin, ListView):
    model = Repo
    template_name = 'spine_core/list.html'

    def get_context_data(self, **kwargs):
        context = super(RepoListView, self).get_context_data(**kwargs)
        context['header'] = 'Repo'
        context['object_url'] = 'spine_core:repo'
        return context

class FileListView(LoginRequiredMixin, ListView):
    model = File
    template_name = 'spine_core/list.html'

    def get_context_data(self, **kwargs):
        context = super(FileListView, self).get_context_data(**kwargs)
        context['header'] = 'File'
        context['object_url'] = 'spine_core:file'
        return context

class DependListView(LoginRequiredMixin, ListView):
    model = Depend
    template_name = 'spine_core/list.html'

    def get_context_data(self, **kwargs):
        context = super(DependListView, self).get_context_data(**kwargs)
        context['header'] = 'Depend'
        context['object_url'] = 'spine_core:depend'
        return context

class AssetListView(LoginRequiredMixin, ListView):
    model = Asset
    template_name = 'spine_core/list.html'

    def get_context_data(self, **kwargs):
        context = super(AssetListView, self).get_context_data(**kwargs)
        context['header'] = 'Asset'
        context['object_url'] = 'spine_core:asset'
        return context

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'spine_core/list.html'

    def get_context_data(self, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)
        context['header'] = 'Task'
        context['object_url'] = 'spine_core:task'
        return context

class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'spine_core/project.html'

class RepoDetailView(LoginRequiredMixin, DetailView):
    model = Repo
    template_name = 'spine_core/repo.html'

class FileDetailView(LoginRequiredMixin, DetailView):
    model = File
    template_name = 'spine_core/file.html'

    def get_context_data(self, **kwargs):
        context = super(FileView, self).get_context_data(**kwargs)
        context['file'].update_stats()
        return context

class DependDetailView(LoginRequiredMixin, DetailView):
    model = Depend
    template_name = 'spine_core/depend.html'

class AssetDetailView(LoginRequiredMixin, DetailView):
    model = Asset
    template_name = 'spine_core/asset.html'

class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'spine_core/task.html'