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


import os
import bpy
import json
import magic
from collections import defaultdict

from . import topsort


LIBRARY_FILE = "library.json"
DEPENDS_FILE = "dependencies.json"
CONFIG_FILE = "config.json"
STANDARD_FOLDER_IGNORES = ['.svn']


def is_blendfile(filepath):
    """ Check that a file is a blend file """
    return filepath.endswith('.blend')


def abspath_path(filepath, rootpath):
    """ Return absolute path from relative to root or just normalize """
    normalized = os.path.normpath(filepath) # Assume root is normalized
    if not rootpath in normalized:
        normalized = os.path.join(root, normalized)
    return normalized


def relpath_path(filepath, rootpath):
    """ Return absolute path based on root """
    normalized = os.path.normpath(filepath)
    if rootpath in normalized:
        return os.path.relpath(normalized, rootpath)
    else:
        return normalized


def walker(fn):

    def wrapped(self, *args, **kwargs):
        for check_dir in os.walk(self.root):
            if all(folder not in check_dir[0] for folder in self.ignores):
                for filename in check_dir[2]:
                    fn(self, os.path.join(check_dir[0],filename))
    return wrapped


class ProjectCrawler():
    """ Crawl Over Entire Project Generating Dependency Graph """

    def __init__(self, path):
        self.root = os.path.normpath(path)
        self.depedencies_file = os.path.join(self.root, DEPENDS_FILE)
        self.config_file = os.path.join(self.root, CONFIG_FILE)
        try:
            self.data = json.loads(open(self.depedencies_file).read())
        except:  # File doesn't exist use correct error
            self._empty_data()
        try:
            self.config = json.loads(open(self.config_file).read())
        except:  # File doesn't exist use correct error
            self._default_configs()
        self.ignores = STANDARD_FOLDER_IGNORES + self.config['ignore_folders']

    def _default_configs(self):
        self.config = {'ignore_folders': []}
        json.

    def _empty_data(self):
        pass

    def _relpath(self, path):
        return relpath_path(path, self.root)

    def _abspath(self, path):
        return abspath_path(path, self.root)

    def _add_deps(self, main, dependencies):
        node = {'path': main}
        for dependency in dependencies:
            self.network.add_edge(node, {'path': dependency})

    def get_blendfile_dependencies(self, blend_file):
        normalized = self._abs_path(blend_file)
        if is_blendfile(normalized):
            bpy.ops.wm.open_mainfile(filepath=normalized)
            paths = (
                bpy.path.abspath(path)
                for path in bpy.utils.blend_paths(absolute=True))
            node = {'path':normalized, 'filetype': 'BLEND'}
            self.network.add_node(node)
            for dependency in paths:
                self.network.add_edge(
                    node,
                    {
                        'path':self._relpath(dependency),
                        'filetype':get_file_type(dependency)})

    def check_file_dependencies(self, filepath):
        normalized = self._abspath(filepath)
        relative = self._relpath(normalized)
        paths = checks[file_type(normalized)]
        self._add_deps(relative, (self._relpath(path) for path in paths))

    @walker
    def get_all_blend_dependencies(self, blend_file):
        self.get_blendfile_dependencies(blend_file)
