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

def raw_exists(path):
    exists = False
    if os.path.isdir(os.path.join(path, "raw")):
        exists = True
    if os.path.isdir(os.path.join(path, "RAW")):
        exists = True
    if os.path.isdir(os.path.join(path, "Raw")):
        exists = True
    return exists

def archive_videos(path, dryrun=True):
    # See if there are any video files
    files = os.listdir(path)
    files = [os.path.join(path, f) for f in files if f.endswith(".MOV") or f.endswith(".mov") or f.endswith(".MP4") or f.endswith(".mp4") or f.endswith(".THM")]

    # Make sure the videos directory exists
    video_path = os.path.join(path, "videos")
    if files and not os.path.exists(video_path):
        if not dryrun:
            os.makedirs(video_path)
        print("{path} created.{dryrun}".format(path=video_path,
                                               dryrun=" (dryrun)" if dryrun else ""))

    # Move the videos into video directory
    for f in files:
        if not dryrun:
            shutil.move(f, video_path)
        print("Moving {video} to {video_dir}.{dryrun}".format(video=f,
                                                              video_dir=video_path,
                                                              dryrun=" (dryrun)" if dryrun else ""))


def archive_jpg(path, dryrun=True):
    # Make sure the darktable/jpg directory exists
    jpg_path = os.path.join(path, "darktable/jpg")
    if not os.path.exists(jpg_path):
        if not dryrun:
            os.makedirs(jpg_path)
        print("{path} created.{dryrun}".format(path=jpg_path,
                                               dryrun=" (dryrun)" if dryrun else ""))

    # Now move any jpgs found into that directory
    files = os.listdir(path)
    files = [f for f in files if f.endswith(".jpg") or f.endswith(".JPG") or f.endswith(".ini") or f.endswith(".db") or f.endswith(".db:encryptable") or f.endswith(".PNG") or f.endswith(".GIF") or f.endswith(".gif") or f.endswith(".xcf") or f.endswith(".TIF") or f.endswith(".tif") or f.endswith(".DS_Store")]
    files = [os.path.join(path,f) for f in files if os.path.isfile(os.path.join(path,f))]

    # Move the image files
    for f in files:
        if not dryrun:
            shutil.move(f, jpg_path)
        print("Moving {image} to {jpg_dir}.{dryrun}".format(image=f,
                                                            jpg_dir=jpg_path,
                                                            dryrun=" (dryrun)" if dryrun else ""))

def move_raws(path,dryrun=True):
    raw = None
    if os.path.isdir(os.path.join(path, "raw")):
        raw = os.path.join(path, "raw")
    if os.path.isdir(os.path.join(path, "RAW")):
        raw = os.path.join(path, "RAW")
    if os.path.isdir(os.path.join(path, "Raw")):
        raw = os.path.join(path, "Raw")

    # Make sure the darktable/edit directory exists
    edit_path = os.path.join(path, "darktable/edit")
    if not os.path.exists(edit_path):
        if not dryrun:
            os.makedirs(edit_path)
        print("{path} created.{dryrun}".format(path=edit_path,
                                               dryrun=" (dryrun)" if dryrun else ""))

    # Now copy any files found other than CR2s into that directory
    files = os.listdir(raw)
    files = [f for f in files if not f.endswith(".CR2")]
    files = [os.path.join(raw, f) for f in files]

    # Move the edit files
    for f in files:
        if not dryrun:
            shutil.move(f, edit_path)
        print("Moving {image} to {edit_dir}.{dryrun}".format(image=f,
                                                             edit_dir=edit_path,
                                                             dryrun=" (dryrun)" if dryrun else ""))

    # Now copy any CR2 files found into the root directory
    files = os.listdir(raw)
    files = [f for f in files if f.endswith(".CR2")]
    files = [os.path.join(raw, f) for f in files if os.path.isfile(os.path.join(raw, f))]

    # Move the raw files
    for f in files:
        if not dryrun:
            shutil.move(f, path)
        print("Moving {image} to {root}.{dryrun}".format(image=f,
                                                         root=path,
                                                         dryrun=" (dryrun)" if dryrun else ""))
    
    # Remove the raw directory
    if not dryrun:
        os.rmdir(raw)
    print("Removing raw directory {raw}.{dryrun}".format(raw=raw,
                                                         dryrun=" (dryrun)" if dryrun else ""))

def restructure(library, dryrun=True):
    dirs = os.listdir(library)
    dirs.sort()
    print dirs
    dirs = [d for d in dirs if re.match("^[0-9][0-9][0-9]_.*", d)]
    print dirs
    dirs = [os.path.join(library,d) for d in dirs if os.path.isdir(os.path.join(library, d))]
    for filename in dirs:
        print("---------------------------------------------------------------------------")
        print(filename)
        # Rename directories to get rid of any spaces
        path = rename(filename, dryrun=dryrun)

        # check if a raw sub-directory exists. We only want to process these directories
        raw = raw_exists(path)
        if not raw:
            continue

        # Archive video files
        archive_videos(path, dryrun=dryrun)

        # Archive jpgs to the darktable/jpg sub-directory
        archive_jpg(path, dryrun=dryrun)

        # Move raws to root directory
        move_raws(path, dryrun=dryrun)




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Restructure image library')
    parser.add_argument('library', metavar='l', type=str, nargs='+', help='Library root path')
    parser.add_argument('--dryrun', dest='dryrun', action='store_const', const=True, default=False)
    args = parser.parse_args()
    restructure(args.library[0], dryrun=args.dryrun)
