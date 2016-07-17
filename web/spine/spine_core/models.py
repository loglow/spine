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

from datetime import datetime
from os import path
import humanize
import magic

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from spine_core.misc import md5sum

class Repo(models.Model):
    name = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    path = models.CharField(max_length=200)
    REPO_TYPE_CHOICES = (
        ('NONE', 'None'),
        ('SVN', 'Subversion'),
        ('MERC', 'Mercurial'),
        ('GIT', 'Git'),
    )
    type = models.CharField(
        max_length=8,
        choices=REPO_TYPE_CHOICES,
        default='NONE',
    )

    def __str__(self):
        return self.name

class Project(models.Model):
    name = models.CharField(max_length=200)
    repos = models.ManyToManyField(Repo)
    users = models.ManyToManyField(User)

    def __str__(self):
        return self.name

class File(models.Model):
    path = models.CharField(max_length=200)
    repo = models.ForeignKey(Repo, on_delete=models.CASCADE)
    version = models.CharField(max_length=20)
    modified = models.DateTimeField(null=True)
    type = models.CharField(max_length=200)
    mime = models.CharField(max_length=50)
    size = models.PositiveIntegerField(null=True)
    hash = models.CharField(max_length=32)
    online = models.NullBooleanField()

    def __str__(self):
        return self.path

    def get_full_path(self):
        """Return fully qualified path to file on local storage."""
        return path.join(self.repo.path, self.path)

    def get_pretty_size(self):
        """Return file size in human-readable natural language."""
        if self.size:
            return humanize.naturalsize(self.size)
        else:
            return None

    def update_stats(self):
        """Check if file exists on disk and if so, update its metadata."""
        full_path = self.get_full_path()
        try:
            self.modified = timezone.make_aware(datetime.fromtimestamp(path.getmtime(full_path)))
            self.size = path.getsize(full_path)
            self.hash = md5sum(full_path)
            self.type = magic.from_file(full_path)
            self.mime = magic.from_file(full_path, mime=True)
        except FileNotFoundError:
            self.online = False
        else:
            self.online = True
        self.save()
        return self.online

class Depend(models.Model):
    master_file = models.ForeignKey(File, on_delete=models.CASCADE, related_name='master_set')
    depend_file = models.ForeignKey(File, on_delete=models.CASCADE, related_name='depend_set')
    master_version = models.CharField(max_length=20)
    depend_version = models.CharField(max_length=20)
    master_modified = models.DateTimeField(null=True)
    depend_modified = models.DateTimeField(null=True)

    def __str__(self):
        return str(self.master_file)+' \u2192 '+str(self.depend_file)

class AssetType(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Asset(models.Model):
    name = models.CharField(max_length=200)
    files = models.ManyToManyField(File)
    type = models.ForeignKey(AssetType, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class TaskType(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Task(models.Model):
    name = models.CharField(max_length=200)
    desc = models.TextField()
    assets = models.ManyToManyField(Asset)
    type = models.ForeignKey(TaskType, on_delete=models.CASCADE)
    duration = models.DurationField(null=True)
    assigned_to = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, blank=True)
    TASK_STATUS_CHOICES = (
        ('NOT_STARTED', 'Not Started'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETE', 'Complete'),
    )
    status = models.CharField(
        max_length=16,
        choices=TASK_STATUS_CHOICES,
        default='NOT_STARTED',
    )

    def __str__(self):
        return self.name