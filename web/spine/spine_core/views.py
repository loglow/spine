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
from .models import Repo, File, Depend

def index(request):
    repo_list = Repo.objects.all()
    file_list = File.objects.all()
    depend_list = Depend.objects.all()
    context = {
        'repo_list': repo_list,
        'file_list': file_list,
        'depend_list': depend_list,
    }
    return render(request, 'spine_core/index.html', context)

class RepoView(DetailView):
    model = Repo
    template_name = 'spine_core/repo.html'

class FileView(DetailView):
    model = File
    template_name = 'spine_core/file.html'

class DependView(DetailView):
    model = Depend
    template_name = 'spine_core/depend.html'

class TestsView(DetailView):
    model = Repo
    template_name = 'spine_core/repo_tests.html'
    # repo = get_object_or_404(Repo, pk=repo_id)
    # spider = ProjectTree(repo.root_path, url=repo.url)
    # return HttpResponse('<br>'.join(spider.all_files()))


def update(request, repo_id):
    repo = get_object_or_404(Repo, pk=repo_id)
    spider = ProjectTree(repo.root_path, url=repo.url)
    return HttpResponse('<br>'.join(spider.all_files()))
