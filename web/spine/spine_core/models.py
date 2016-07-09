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

from django.db import models

class Repo(models.Model):
	REPO_TYPE_CHOICES = (
		('NONE', 'None'),
		('SVN', 'Subversion'),
		('MERC', 'Mercurial'),
		('GIT', 'Git'),
	)
	root_path = models.CharField(max_length=200, default='/')
	repo_type = models.CharField(
		max_length=4,
		choices=REPO_TYPE_CHOICES,
		default='NONE',
	)

class File(models.Model):
	path = models.CharField(max_length=200)
	#type
	repo = models.ForeignKey(Repo, on_delete=models.CASCADE)
	last_version = models.CharField(max_length=20, default=0)
	last_edited = models.DateTimeField(null=True)
	#version_control
	#status

class Depend(models.Model):
	master = models.ForeignKey(File, on_delete=models.CASCADE, related_name='depend_from_set')
	dependency = models.ForeignKey(File, on_delete=models.CASCADE, related_name='depend_to_set')
	master_version = models.PositiveIntegerField(default=0)
	dependency_version = models.PositiveIntegerField(default=0)
	master_last_edited = models.DateTimeField(null=True)
	dependency_last_edited = models.DateTimeField(null=True)
	#generator