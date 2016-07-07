#!/usr/bin/python3
import sys
import json
import os
import argparse

import spider
import topsort


DEPENDS_FILE = "dependencies.json" # Lives in Project Root
CONFIG_FILE = "config.json" # Project Config, lives in project root
STANDARD_FOLDER_IGNORES = ['.svn', '.git']

CONFIGS = "cliconfigs.json"

class Hierarchy(topsort.Network, spider.ProjectTree):
    def __init__(self, path, url=None, user=None, password=None):
        spider.ProjectTree.__init__(self, path, url, user, password)
        topsort.Network.__init__(self)
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
        deps = self._deep_deps(filepath)
        for dep in deps:
            print("Getting ", dep)
            self._update_path(dep)


def get_configs():
    try:
        config = json.loads(open(os.path.join(
            os.path.dirname(__file__),
            CONFIGS)).read())
    except FileNotFoundError:
        print("Error: No Config")
        print()
        print("       Create a {} file in {}".format(
            CONFIGS,
            os.path.dirname(__file__)))
        print("       with the following contents, including quotes:")
        print("")
        print('{"password": "your_svn_password","root": "project/root/folder", "url": "svn://url", "user": "your_svn_username"}')
        print()
        print()
        raise FileNotFoundError("Exiting")
    else:
        return config


if __name__ == "__main__":
    print("Command Line Tools for JSON Temp Experiments")
