# -*- coding: utf-8 -*-

# Copyright © 2018 by IBPort. All rights reserved.
# @Author: Neal Wong
# @Email: ibprnd@gmail.com

import os
import sys
import argparse
import fnmatch
import codecs

PY2 = bool(sys.version_info.major == 2)

def parse_args():
    parser = argparse.ArgumentParser(description='Extract column from text files.')
    parser.add_argument('-p', '--path', help='File or directory path.')
    parser.add_argument(
        '-c', '--column', type=int, default=1, help='Column to extract, default is 1.')
    parser.add_argument(
        '-s', '--separator', default='\t', help='Column separator, default is tab.')
    parser.add_argument(
        '-f', '--file_pattern', default='*.txt', help='File pattern to match, default is *.txt.')
    parser.add_argument(
        '-r', '--reseve_header', default=False,
        action="store_true", help="Add -r to reserve header.")
    parser.add_argument('-o', '--output', help='Result output path.')
    command_args = parser.parse_args()

    return command_args

if __name__ == "__main__":
    args = parse_args()
    path = os.path.abspath(os.path.expanduser(args.path))
    if not os.path.exists(path):
        print("\"%s\" is not exist" % args.path)
        sys.exit(1)

    col = args.column - 1
    separator = args.separator
    file_pattern = args.file_pattern
    reseve_header = args.reseve_header

    output_path = os.path.abspath(os.path.expanduser(args.output))
    if os.path.isfile(output_path):
        os.remove(output_path)

    output_dir = os.path.dirname(output_path)
    if not os.path.isdir(output_dir):
        try:
            os.makedirs(output_dir)
        except:
            print("Could not create output directory: %s" % output_dir)
            sys.exit(1)

    files = []
    if os.path.isfile(path):
        files.append(path)
    else:
        for root, dirnames, filenames in os.walk(path):
            for filename in fnmatch.filter(filenames, file_pattern):
                files.append(os.path.join(root, filename))

    records = []
    for file_path in files:
        print("Processing %s" % file_path)
        try:
            if PY2:
                file_fh = codecs.open(file_path, encoding='utf-8', errors='ignore')
            else:
                file_fh = open(file_path, encoding='utf-8', errors='ignore')

            if not reseve_header:
                next(file_fh)

            for line in file_fh:
                columns = line.split(separator)
                n_cols = len(columns)
                if n_cols > col:
                    records.append(columns[col].strip())
                else:
                    continue
        finally:
            file_fh.close()

    unique_records = list({}.fromkeys(records).keys())
    with open(output_path, 'a') as output_fh:
        output_fh.write("\n".join(unique_records))
        output_fh.write("\n")

    print("Done!")