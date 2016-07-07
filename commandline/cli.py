import sys
import json
import os

import spider
import topsort


ROOT="/home/bassam/projects/hamp/tube"
PATH = sys.argv[-1] #TODO should check errors once
svn = spider.ProjectTree(ROOT)
DEPENDS_FILE = "dependencies.json"
CONFIG_FILE = "config.json"
STANDARD_FOLDER_IGNORES = ['.svn', '.git']

class Hierarchy(topsort.Network):
    def __init__(self, path):
        super().__init__()
        self.root = os.path.normpath(path)
        self.dependencies_file = os.path.join(self.root, DEPENDS_FILE)
        self.config_file = os.path.join(self.root, CONFIG_FILE)
        data = json.loads(open(self.dependencies_file).read())
        self.nodes = set(data['nodes'])
        for node in data['edges']:
            self.edges[node] = set(data['edges'][node])
        self.config = json.loads(open(self.config_file).read())
        self.ignores = STANDARD_FOLDER_IGNORES + self.config['ignore_folders']


    def _deep_deps(self, filepath):
        # assume relative for now
        if filepath not in self.edges.keys():
            return {filepath}
        deps = self.edges[filepath]
        for dep in self.edges[filepath]: # Don't modify what you loop
            subdeps = self._deep_deps(dep)
            deps = deps.union(subdeps)
        deps.add(filepath)
        return deps


    def update(self, filepath):
        deps = _deep_deps(filepath)
                
