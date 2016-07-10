#!/usr/bin/python3
import argparse

import cli


def main():
    parser = argparse.ArgumentParser(description='Get or Update Files From SVN')
    parser.add_argument(
        'path', type=str, help="Path/s to Get", nargs="+")
    args = parser.parse_args()
    config = cli.get_configs()
    updater = cli.Hierarchy(
                path=config['root'],
                url=config['url'],
                user=config['user'],
                password=config['password'])
    for p in args.path:
        updater.update(p)

if __name__ == "__main__":
    main()
