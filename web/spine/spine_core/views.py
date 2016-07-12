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
from django.views.generic import DetailView

from .models import Project, Repo, File, Depend, Asset, Task

def index(request):
    projects = Project.objects.all()
    repos = Repo.objects.all()
    files = File.objects.all()
    depends = Depend.objects.all()
    assets = Asset.objects.all()
    tasks = Task.objects.all()
    context = {
        'projects': projects,
        'repos': repos,
        'files': files,
        'depends': depends,
        'assets': assets,
        'tasks': tasks,
    }
    return render(request, 'spine_core/index.html', context)

class ProjectView(DetailView):
    model = Project
    template_name = 'spine_core/project.html'

class RepoView(DetailView):
    model = Repo
    template_name = 'spine_core/repo.html'

class FileView(DetailView):
    model = File
    template_name = 'spine_core/file.html'

    def get_context_data(self, **kwargs):
        context = super(FileView, self).get_context_data(**kwargs)
        context['file'].update_stats()
        return context

class DependView(DetailView):
    model = Depend
    template_name = 'spine_core/depend.html'

class AssetView(DetailView):
    model = Asset
    template_name = 'spine_core/asset.html'

class TaskView(DetailView):
    model = Task
    template_name = 'spine_core/task.html'