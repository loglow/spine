#!/usr/bin/python3
import argparse
import cli


def main():
    parser = argparse.ArgumentParser(description='Update checked out files')
    args = parser.parse_args()
    config = cli.get_configs()
    updater = cli.Hierarchy(
                path=config['root'],
                url=config['url'],
                user=config['user'],
                password=config['password'])
    for p in updater.all_files():
        updater.update(p)

if __name__ == "__main__":
    main()

