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

from django.views.generic import DetailView, ListView
from django.contrib.auth.views import redirect_to_login
from django.core.urlresolvers import reverse
from django.shortcuts import redirect

from spine_core.misc import url_qs

def index(request):
    return redirect('spine_core:project')

class AuthListView(ListView):
    filter = None

    def get_queryset(self):
        return self.model.objects.filter(**{self.filter: self.request.user}).distinct()

    def get_context_data(self, **kwargs):
        context = super(AuthListView, self).get_context_data(**kwargs)
        context['header'] = self.model.__name__+'s'
        context['object_url'] = 'spine_core:'+self.model.__name__.lower()
        return context

class ProjectListView(AuthListView): pass
class RepoListView(AuthListView): pass
class FileListView(AuthListView): pass
class DependListView(AuthListView): pass
class AssetListView(AuthListView): pass
class TaskListView(AuthListView): pass

class AuthDetailView(DetailView):
    filter = None

    def dispatch(self, request, *args, **kwargs):
        if self.get_object() in self.model.objects.filter(**{self.filter: self.request.user}):
            return super(AuthDetailView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect_to_login(
                '/{model}/{pk}/'.format(
                    model=self.model.__name__.lower(),
                    pk=self.kwargs['pk'],
                ),
                login_url=url_qs(reverse('spine_core:login'), msg='auth'),
            )

class ProjectDetailView(AuthDetailView): pass
class RepoDetailView(AuthDetailView): pass
class DependDetailView(AuthDetailView): pass
class AssetDetailView(AuthDetailView): pass
class TaskDetailView(AuthDetailView): pass

class FileDetailView(AuthDetailView):

    def get_context_data(self, **kwargs):
        context = super(FileDetailView, self).get_context_data(**kwargs)
        context['file'].update_stats()
        return context