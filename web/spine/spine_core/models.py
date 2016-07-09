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
	root_path = models.CharField(max_length=200)
	repo_type = models.CharField(
		max_length=4,
		choices=REPO_TYPE_CHOICES,
		default='NONE',
	)

class File(models.Model):
	path = models.CharField(max_length=200)
	#type
	repo = models.ForeignKey(Repo, on_delete=models.CASCADE)
	#latest_version
	#version_control
	#status

class Edge(models.Model):
	main_file = models.ForeignKey(File, on_delete=models.CASCADE, related_name='main_set')
	depend_file = models.ForeignKey(File, on_delete=models.CASCADE, related_name='depend_set')
	main_version = models.PositiveIntegerField(default=0)
	depend_version = models.PositiveIntegerField(default=0)
	#generator