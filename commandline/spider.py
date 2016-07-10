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

"""
Subversion Partial Inter-Dependency Ranger
Spider does the following:
  Perform a sparse directory-only checkout from project svn
  Provide an api for extracting a specific file via update
  Use of dependencies (cached?) to extract a thing
"""

"""
checkout only the top level folder of a project, includes:
library.json , some kind of dependency tree
to check out a file

some ideas:
- initial 'smarts' are in data and on client side
- each project needs a unique project ID
- automatic dependency crawlers, potentially using bpy, gimp api, others
- manual dependency addition
- external project ID based recognition for future cross project dependencies
- untracked 'generated' folder management with own method of retreiving caches  (if available) or regenerating based on recepies (if available)
- metadata for generated files, problem with reproducability

start with:
- enhance library.json by nesting asset data one deeper, allowing extra data
- implement crawler api + blend based crawler
- ignore generated issue
- ignore cross project deps but:
- create project ID

reference desk enhancements
- update reference desk to be smarter with data types *
- generic posthooks *
- image previews *
- compatibility with library.json changes
- project browser and:
- commit capability
- update capability

initial commit issues:
- single file based commit (easy from blender)
- easy show uncommited files

* these options unrelelated to spider

"""

import pysvn
import os
import json


class ProjectTree():
    """ Smart subversion wrapper with knowledge of project depedencies """

    def __init__(self, path, url=None, user=None, password=None):
        def get_login():
            pass
        self.client = pysvn.Client()
        self.client.callback_get_login = self._get_login
        self.root = os.path.normpath(path)
        if not os.path.exists(self.root):
            self.url = url
            self._checkout_empty_project()
        self.url = self._get_url(url)
        self.user = user
        self.password = password

    def _get_url(self, url):
        return self.client.info(self.root).url

    def _get_login(self, realm, username, may_save):
        available = all(
            prop is not None for prop in (self.user, self.password))
        return availabe, self.user, self.password, True

    def _checkout_empty_project(self):
        self.client.checkout(self.url, self.root, recurse=False)

    def _update_path(self, path):
        full_path = self._abs_path(self._rel_path(path))
        self.client.update(
            full_path,
            depth=pysvn.depth.empty,
            make_parents=True)

    def _rel_path(self, path):
        norm = os.path.normpath(path)
        if norm.startswith(self.root):
            return os.path.relpath(norm, self.root)
        else:
            return norm

    def _abs_path(self, path):
        return os.path.abspath(os.path.join(self.root, os.path.normpath(path)))

    def all_files(self):
        """ Return all the files in SVN """
        bases = (
            p[0].repos_path[1:]
            for p in self.client.list(self.url, recurse=True))
        return (
            f[1:] for f in bases if f and os.path.isfile(self._abs_path(f[1:])))
