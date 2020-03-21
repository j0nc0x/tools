#!/usr/bin/python

# script to reorganise my photo library to work better with lightroom
# ie. store raws at top level of each project directory, archive .xmps
# created in darktable to /darktable/xmp/ subdirectory and .jpgs created
# in darktable to /darktable/jpg subdirectory


import sys
import os
import shutil
import argparse
import re

def rename(path, dryrun=True):
    new_path = path.replace(" ", "_")
    if new_path != path:
        if not dryrun:
            shutil.move(path, new_path)
        print("{path} renamed to {newpath}.{dryrun}".format(path=path,
                                                            newpath=new_path,
                                                            dryrun=" (dryrun)" if dryrun else ""))
    return path if dryrun else new_path

def archive_jpg(path, dryrun=True):
    # Make sure the darktable/jpg directory exists
    jpg_path = os.path.join(path, "darktable/jpg")
    if not os.path.exists(jpg_path):
        if not dryrun:
            os.makedirs(jpg_path)
        print("{path} created.{dryrun}".format(path=jpg_path,
                                               dryrun=" (dryrun)" if dryrun else ""))

    # Now copy any jpgs found into that directory
    files = os.listdir(path)
    files = [f for f in files if not f.endswith(".jpg")]
    files = [f for f in files if os.path.isfile(os.path.join(path,f))]
    print files
    

def restructure(library, dryrun=True):
    dirs = os.listdir(library)
    dirs.sort()
    dirs = [d for d in dirs if re.match("^[0-9][0-9][0-9] .*", d)]
    dirs = [os.path.join(library,d) for d in dirs if os.path.isdir(os.path.join(library, d))]
    for filename in dirs:
        print("-------------------------------------------")
        # Rename directories to get rid of any spaces
        path = rename(filename, dryrun=dryrun)

        # Archive jpgs to the darktable/jpg sub-directory
        archive_jpg(path, dryrun=dryrun)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Restructure image library')
    parser.add_argument('library', metavar='l', type=str, nargs='+', help='Library root path')
    parser.add_argument('--dryrun', dest='dryrun', action='store_const', const=True, default=False)
    args = parser.parse_args()
    restructure(args.library[0], dryrun=args.dryrun)
