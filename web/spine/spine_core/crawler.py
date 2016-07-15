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
import magic  #XXX pip install python-magic
import subprocess
from collections import defaultdict
from bpy.utils import blend_paths

from topsort import Network

LIBRARY_FILE = "library.json"
DEPENDS_FILE = "dependencies.json"
CONFIG_FILE = "config.json"
STANDARD_FOLDER_IGNORES = ['.svn', '.git']


class BlendCheck():
    """ Blend File Support Code """
    extension = ".blend"

    @classmethod
    def poll(cls, filepath):
        """ Check that a file is a blend file """
        fm = magic.from_file(filepath)
        return (
            fm.startswith('Blender3D, saved') or
            (fm.startswith('gzip') and filepath.endswith(cls.extension)))

    @classmethod
    def deps(cls, filepath):
        """ Return file path dependencies list from filepath """
        try:
            bpy.ops.wm.open_mainfile(filepath=filepath)
        except RuntimeError:
            # raise RuntimeError("Not a Blend File!") #XXX shouldn't happen
            print("NOT A BLEND FILE:",filepath)
            return []
        return (
            p for p in blend_paths(absolute=True, packed=False, local=True)
            if p not in ("/", "\\"))


class FileSupport():
    """
    Convenience class allows us to dynamically wrap all our file-specific
    checks into one handy function
    """
    def __init__(self, support_list):
        self.checks = {cls.extension: cls.deps for cls in support_list}
        self.polls = {cls.extension: cls.poll for cls in support_list}

    def type(self, filepath):
        for extension in self.polls:
            if self.polls[extension](filepath):
                return extension

    def check(self, filepath):
        extension = self.type(filepath)
        if extension:
            return self.checks[extension](filepath)
        else:
            return []


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


class ProjectCrawler(Network):
    """ Crawl Over Entire Project Generating Dependency Graph """

    def __init__(self, path):
        super().__init__()
        self.root = os.path.normpath(path)
        self.file_support = FileSupport((BlendCheck,)) # TODO import checkers
        self.dependencies_file = os.path.join(self.root, DEPENDS_FILE)
        self.config_file = os.path.join(self.root, CONFIG_FILE)
        try:
            data = json.loads(open(self.dependencies_file).read())
        except FileNotFoundError:
            self.save()
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
        """ If no configs exist create an empty default file """
        self.config = {'ignore_folders': []}
        with open(self.config_file, mode='w') as config_file:
            config_file.write(
                json.dumps(self.config, sort_keys=True, indent=4))

    def clear(self):
        """ Flush old deps to start clean """
        self.nodes = set()
        self.edges = defaultdict(set)

    def save(self):
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
        self.add_node(main)
        for dependency in dependencies:
            self.add_edge(main, dependency)

    def check_file(self, filepath):
        """
        Check a single file in the project can be triggered on file changes,
        repository checks, etc.
        """
        normalized = self._abspath(filepath)
        relative = self._relpath(normalized)
        paths = self.file_support.check(normalized)
        #TODO For now we'll ignore missing or out of tree paths
        self._add_deps(relative, (
            self._relpath(path) for path in paths
            if self.root in path and os.path.isfile(path)))

    def check_files(self, filelist):
        """
        Check a list of files given from another source, e.g. svn status
        """
        for filepath in filelist:
            self.check_file(filepath)

    def check_project(self):
        """
        Walk over entire project folder finding deps for each file
        if those files are of types that have dependency checkers
        """
        for check_dir in os.walk(self.root):
            if all(folder not in check_dir[0] for folder in self.ignores):
                for filename in check_dir[2]:
                    self.check_file(
                        os.path.join(check_dir[0], filename))
