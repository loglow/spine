import sys
import json
import os

import crawler
import spider
import topsort


ROOT="/home/bassam/projects/hamp/tube"
PATH = sys.argv[-1] #TODO should check errors once
svn = spider.ProjectTree(ROOT)
DEPENDS_FILE = "depedencies.json"
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

    def update(self, filepath):
        # assume relative for now
        
