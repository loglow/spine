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

from django.contrib.admin import ModelAdmin, site

from .models import *

class RepoAdmin(ModelAdmin):
	list_display = (
        'name',
        'path',
        'type',
        'url',
    )

class FileAdmin(ModelAdmin):
	list_display = (
        'path',
        'type',
        'mime',
        'size',
        'hash',
        'repo',
        'version',
        'modified',
    )

class DependAdmin(ModelAdmin):
	list_display = (
        '__str__',
        'master_file',
        'master_version',
        'master_modified',
        'depend_file',
        'depend_version',
        'depend_modified',
    )

class TaskAdmin(ModelAdmin):
    list_display = (
        'name',
        'type',
        'status',
        'duration',
        'assigned_to',
    )

class AssetAdmin(ModelAdmin):
    list_display = (
        'name',
        'type',
    )

site.register(Project)
site.register(Asset, AssetAdmin)
site.register(AssetType)
site.register(Task, TaskAdmin)
site.register(TaskType)
site.register(Repo, RepoAdmin)
site.register(File, FileAdmin)
site.register(Depend, DependAdmin)