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
import subprocess
from collections import defaultdict
from bpy.utils import blend_paths

from topsort import Network


LIBRARY_FILE = "library.json"
DEPENDS_FILE = "dependencies.json"
CONFIG_FILE = "config.json"
STANDARD_FOLDER_IGNORES = ['.svn']


def is_blendfile(filepath):
    """ Check that a file is a blend file """
    return filepath.endswith('.blend')


def file_type(filepath):
    if is_blendfile(filepath): return "blend"
    return "other"


def get_blend_dependencies(filepath):
    """ currently stupid as it does not take libs into account """
    bpy.ops.wm.open_mainfile(filepath=filepath)
    paths = (
        p for p in blend_paths(absolute=True, packed=False, local=True)
        if p not in ("/", "\\"))
    return paths


checks = {"blend": get_blend_dependencies}


def abspath_path(filepath, rootpath):
    """ Return absolute path from relative to root or just normalize """
    normalized = os.path.normpath(filepath) # Assume root is normalized
    if not rootpath in normalized:
        normalized = os.path.join(rootpath, normalized)
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


class ProjectCrawler(Network):
    """ Crawl Over Entire Project Generating Dependency Graph """

    def __init__(self, path):
        super().__init__()
        self.root = os.path.normpath(path)
        self.dependencies_file = os.path.join(self.root, DEPENDS_FILE)
        self.config_file = os.path.join(self.root, CONFIG_FILE)
        try:
            data = json.loads(open(self.depedencies_file).read())
        except:  # File doesn't exist use correct error
            self._dependencies_write()
        else:
            self.nodes = set(data['nodes'])
            for node in data['edges']:
                self.edges[node] = set(data['edges'][node])
        try:
            self.config = json.loads(open(self.config_file).read())
        except:  # File doesn't exist use correct error
            self._default_configs()
        self.ignores = STANDARD_FOLDER_IGNORES + self.config['ignore_folders']

    def _default_configs(self):
        self.config = {'ignore_folders': []}
        with open(self.config_file, mode='w') as config_file:
            config_file.write(
                json.dumps(self.config, sort_keys=True, indent=4))

    def _dependencies_write(self):
        with open(self.dependencies_file, mode='w') as dependencies_file:
            dependencies_file.write(json.dumps(
                {
                    'nodes':list(self.nodes),
                    'edges':{nd: list(self.edges[nd]) for nd in self.edges}},
                sort_keys=True, indent=4))

    def _relpath(self, path):
        return relpath_path(path, self.root)

    def _abspath(self, path):
        return abspath_path(path, self.root)

    def _add_deps(self, main, dependencies):
        for dependency in dependencies:
            self.add_edge(main, dependency)

    def check_file_dependencies(self, filepath):
        normalized = self._abspath(filepath)
        relative = self._relpath(normalized)
        try:
            paths = checks[file_type(normalized)](normalized)
        except KeyError:
            print("Can't check {}".format(file_type(normalized)))
        else:
            self._add_deps(relative, (self._relpath(path) for path in paths))

    def get_all_dependencies(self):
        for check_dir in os.walk(self.root):
            if all(folder not in check_dir[0] for folder in self.ignores):
                for filename in check_dir[2]:
                    print("Checking ", os.path.join(check_dir[0], filename))
                    self.check_file_dependencies(
                        os.path.join(check_dir[0], filename))
        
