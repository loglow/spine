#!/usr/bin/python3
import sys
import argparse

import cli



def main():
    parser = argparse.ArgumentParser(description='Get Files From SVN')
    parser.add_argument(
        'path', type=str, help="Path to Get", default="")
    args = parser.parse_args()
    config = cli.get_configs()
    updater = cli.Hierarchy(
                path=config['root'],
                url=config['url'],
                user=config['user'],
                password=config['password'])
    updater.update(args.path)

if __name__ == "__main__":
    main()

