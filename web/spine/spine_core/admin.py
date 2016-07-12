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

from django.contrib import admin

from .models import Project, Repo, File, Depend, Asset

class RepoAdmin(admin.ModelAdmin):
	list_display = (
        'name',
        'root_path',
        'repo_type',
        'url',
    )

class FileAdmin(admin.ModelAdmin):
	list_display = (
        'path',
        'file_type',
        'mime_type',
        'size_in_bytes',
        'md5_hash',
        'repo',
        'last_version',
        'last_edited',
    )

class DependAdmin(admin.ModelAdmin):
	list_display = (
        '__str__',
        'master_file',
        'master_version',
        'master_last_edited',
        'depend_file',
        'depend_version',
        'depend_last_edited',
    )

admin.site.register(Project)
admin.site.register(Asset)
admin.site.register(Repo, RepoAdmin)
admin.site.register(File, FileAdmin)
admin.site.register(Depend, DependAdmin)