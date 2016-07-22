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

from django.views.generic import View, DetailView, ListView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.views import redirect_to_login
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.utils import timezone

from spine_core.models import Asset, Comment
from spine_core.forms import NewCommentForm
from spine_core.misc import url_qs

def index(request):
    return redirect('spine_core:project')

class AuthListView(ListView):
    filter = None

    def get_queryset(self):
        return self.model.objects.filter(**{self.filter: self.request.user}).distinct()

class ProjectListView(AuthListView): pass
class RepoListView(AuthListView): pass
class FileListView(AuthListView): pass
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
class TaskDetailView(AuthDetailView): pass

class FileDetailView(AuthDetailView):

    def get_context_data(self, **kwargs):
        context = super(FileDetailView, self).get_context_data(**kwargs)
        context['file'].update_stats()
        return context

class AssetDetailView(AuthDetailView):

    def get_context_data(self, **kwargs):
        context = super(AssetDetailView, self).get_context_data(**kwargs)
        context['form'] = NewCommentForm()
        return context

    def post(self, request, *args, **kwargs):
        view = AssetDetailPost.as_view()
        return view(request, *args, **kwargs)

class AssetDetailPost(View, SingleObjectMixin):
    model = Asset

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if 'new_comment' in self.request.POST:
            comment = Comment.objects.create(
                user=self.request.user,
                text=self.request.POST['new_comment'],
                time=timezone.now(),
            )
            comment.save()
            self.object.comments.add(comment)
        elif 'delete_comment' in self.request.POST:
            id = self.request.POST['delete_comment']
            comment = Comment.objects.get(id=id)
            comment.delete()
        return redirect('spine_core:asset', pk=self.object.pk)