#!/usr/bin/python3
import argparse
import cli


def main():
    print("Warning: doesn't check that low res maps exist")
    parser = argparse.ArgumentParser(
        description='Get low rez Versions of existing maps')
    args = parser.parse_args()
    config = cli.get_configs()
    updater = cli.Hierarchy(
                path=config['root'],
                url=config['url'],
                user=config['user'],
                password=config['password'])
    for p in updater.all_files():
        if p.startswith('lib/maps/'):
            q = p.replace('lib/maps/', 'lib/maps_low/')
            updater.update(q)

if __name__ == "__main__":
    main()

