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
        max_length=8,
        choices=REPO_TYPE_CHOICES,
        default='NONE',
    )
    url = models.CharField(max_length=200)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class File(models.Model):
    FILE_TYPE_CHOICES = (
        ('3D Media', (
            ('BLEND', 'Blender'),
            ('MA', 'Maya ASCII'),
            ('MB', 'Maya Binary'),
            ('OBJ', 'Wavefront'),
        )),
        ('2D Media', (
            ('PNG', 'Portable Network Graphics'),
            ('KRA', 'Krita'),
            ('XCF', 'GIMP'),
            ('PSD', 'Adobe Photoshop'),
            ('AI', 'Adobe Illustrator'),
            ('SVG', 'Scalable Vector Graphics'),
            ('TIFF', 'Tagged Image File Format'),
            ('JPG', 'JPEG'),
            ('EXR', 'OpenEXR'),
        )),
        ('Text Data', (
            ('TXT', 'Plain Text'),
            ('PY', 'Python'),
            ('MD', 'Markdown'),
            ('HTML', 'Hypertext Markup Language'),
            ('CSS', 'Cascading Style Sheets'),
        )),
        ('OTHER', 'Other'),
    )
    path = models.CharField(max_length=200)
    repo = models.ForeignKey(Repo, on_delete=models.CASCADE)
    last_version = models.CharField(max_length=20)
    last_edited = models.DateTimeField()
    file_type = models.CharField(
        max_length=8,
        choices=FILE_TYPE_CHOICES,
        default='OTHER',
    )

    def __str__(self):
        return self.path

class Depend(models.Model):
    master_file = models.ForeignKey(File, on_delete=models.CASCADE, related_name='master_set')
    depend_file = models.ForeignKey(File, on_delete=models.CASCADE, related_name='depend_set')
    master_version = models.PositiveIntegerField()
    depend_version = models.PositiveIntegerField()
    master_last_edited = models.DateTimeField()
    depend_last_edited = models.DateTimeField()

    def __str__(self):
        return str(self.master_file)+' \u2192 '+str(self.depend_file)