#!/usr/bin/env python2

import os
import subprocess as sp
import argparse


def get_free_space_mb(dir):
    cmd = 'df -P {dir} | tail -1 | awk \'{{print $4}}\''.format(dir=dir)
    free_bytes = sp.check_output(cmd, shell=True).strip()
    free_mb = float(free_bytes) / 1000
    return int(round(free_mb, 0))


def get_timestamp_of_file(file):
    return os.path.getctime(file)


def get_files_sorted_by_date(dir):
    """
    Returns list of all non hidden files sorted by date (oldest file first)
    """
    files = sp.check_output("find {dir} -type f -not -path '*/\\.*'".format(dir=dir), shell=True)
    files = files.splitlines()
    return sorted(files, key=lambda f: os.path.getctime(f))


def free_up_space(megabytes, dir):
    files_by_date = get_files_sorted_by_date(dir)
    for file in files_by_date:
        if get_free_space_mb(dir) < megabytes:
            os.remove(file)
            print('Deleted {f} to reach minimum required free space of {space} MB'.format(
                f=file,
                space=megabytes
            ))
        else:
            return
    # last possible file has been deleted. check again if enough space freed up.
    if get_free_space_mb(dir) < megabytes:
        print('No more files left to delete. Cannot free up space of {mb}MB'.format(mb=megabytes))


def main():
    parser = argparse.ArgumentParser(description="""
    Warning: Use with caution!
    This script will delete as many files in the given directory until the desired minimum free space is available.
    Without further notice!!!
    The intention of this is to prevent the disk from running full.
    Surveillance would be an exemplary scenario where it is better to delete the oldest recordings on a full disk
    than to stop recording.
    Execute this script each time you save a new file to ensure there will be enough space for the next file.
    Or just execute it periodically via cron.
    """)
    parser.add_argument('--dir', '-d', type=str, required=True)
    parser.add_argument('--space', '-s', type=int, required=True, help='minimum space in MB to keep free', metavar='megabytes')
    args = parser.parse_args()
    free_up_space(args.space, args.dir)


if __name__ == '__main__':
    main()
