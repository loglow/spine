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

import magic
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from os.path import join, getsize, getmtime
from hashlib import md5
from datetime import datetime
from humanize import naturalsize

def md5sum(filename, blocksize=65536):
    hash = md5()
    with open(filename, "rb") as f:
        for block in iter(lambda: f.read(blocksize), b""):
            hash.update(block)
    return hash.hexdigest()

class Repo(models.Model):
    REPO_TYPE_CHOICES = (
        ('NONE', 'None'),
        ('SVN', 'Subversion'),
        ('MERC', 'Mercurial'),
        ('GIT', 'Git'),
    )
    path = models.CharField(max_length=200)
    type = models.CharField(
        max_length=8,
        choices=REPO_TYPE_CHOICES,
        default='NONE',
    )
    url = models.CharField(max_length=200)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Project(models.Model):
    name = models.CharField(max_length=200)
    repos = models.ManyToManyField(Repo)

    def __str__(self):
        return self.name

class File(models.Model):
    path = models.CharField(max_length=200)
    repo = models.ForeignKey(Repo, on_delete=models.CASCADE)
    version = models.CharField(max_length=20)
    modified = models.DateTimeField()
    type = models.CharField(max_length=200)
    mime = models.CharField(max_length=50)
    size = models.PositiveIntegerField(null=True)
    hash = models.CharField(max_length=32, null=True)
    online = models.NullBooleanField()

    def __str__(self):
        return self.path

    def get_full_path(self):
        """Return fully qualified path to file on local storage."""
        return join(self.repo.path, self.path)

    def get_pretty_size(self):
        """Return file size in human-readable natural language."""
        return naturalsize(self.size)

    def update_stats(self):
        """Check if file exists on disk and if so, update its metadata."""
        full_path = self.get_full_path()
        try:
            self.modified = timezone.make_aware(datetime.fromtimestamp(getmtime(full_path)))
            self.size = getsize(full_path)
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
    master_version = models.PositiveIntegerField()
    depend_version = models.PositiveIntegerField()
    master_modified = models.DateTimeField()
    depend_modified = models.DateTimeField()

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
    TASK_STATUS_CHOICES = (
        ('NOT_STARTED', 'Not Started'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETE', 'Complete'),
    )
    name = models.CharField(max_length=200)
    desc = models.TextField()
    assets = models.ManyToManyField(Asset)
    type = models.ForeignKey(TaskType, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=16,
        choices=TASK_STATUS_CHOICES,
        default='NOT_STARTED',
    )
    duration = models.DurationField()
    assigned_to = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, blank=True)

    def __str__(self):
        return self.name