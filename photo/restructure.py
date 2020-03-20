#!/usr/bin/python

# script to reorganise my photo library to work better with lightroom
# ie. store raws at top level of each project directory, archive .xmps
# created in darktable to /darktable/xmp/ subdirectory and .jpgs created
# in darktable to /darktable/jpg subdirectory


import sys
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Restructure image library')
    parser.add_argument('--dryrun', dest='dryrun', action='store_const', const=True, default=False)
    args = parser.parse_args()
    print(args.dryrun)
