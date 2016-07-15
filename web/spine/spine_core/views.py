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

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.views.generic import DetailView
from .spider import ProjectTree
from .models import Project, Repo, File, Depend, Asset
from .tasks import list_current, dep_current

def index(request):
    project_list = Project.objects.all()
    repo_list = Repo.objects.all()
    file_list = File.objects.all()
    depend_list = Depend.objects.all()
    asset_list = Asset.objects.all()
    context = {
        'project_list': project_list,
        'repo_list': repo_list,
        'file_list': file_list,
        'depend_list': depend_list,
        'asset_list': asset_list,
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

class TestsView(DetailView):
    model = Repo
    template_name = 'spine_core/repo_tests.html'
    # repo = get_object_or_404(Repo, pk=repo_id)
    # spider = ProjectTree(repo.root_path, url=repo.url)
    # return HttpResponse('<br>'.join(spider.all_files()))


class AssetView(DetailView):
    model = Asset
    template_name = 'spine_core/asset.hmtl'


def update(request, repo_id):
    a = list_current.delay(repo_id)
    return HttpResponse('getting files')


def depmake(request, repo_id):
    a = dep_current.delay(repo_id)
    return HttpResponse('getting dependencies')
