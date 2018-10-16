# -*- coding: utf-8 -*-

# Copyright © 2018 by IBPort. All rights reserved.
# @Author: Neal Wong
# @Email: ibprnd@gmail.com

import os
import sys
import argparse

parser = argparse.ArgumentParser(description='Filter duplicate records by column.')
parser.add_argument('--i1', help='File to filter.')
parser.add_argument('--i2', help='File that filters against.')
parser.add_argument('--c1', type=int, default=1, help='Column of file 1 to filter, default is 1.')
parser.add_argument(
    '--c2', type=int, default=1, help='Column of file 2 to filter against, default is 1.')
parser.add_argument('--s1', default='\t', help='Separator of file 1, default is tab.')
parser.add_argument('--s2', default='\t', help='Separator of file 2, default is tab.')
parser.add_argument(
    '-v', '--invert_match', action='store_true', help='Invert match, select non-matching lines.')
parser.add_argument('-o', '--output', help='Ouput file.')
args = parser.parse_args()

input_path = os.path.abspath(os.path.expanduser(args.i1))
file_path = os.path.abspath(os.path.expanduser(args.i2))
for f in [input_path, file_path]:
    if not os.path.isfile(f):
        print('ERROR: File not found - %s!' % f)
        sys.exit(1)

output_path = os.path.abspath(os.path.expanduser(args.output))
output_dir = os.path.dirname(output_path)
if not os.path.isdir(output_dir):
    try:
        os.makedirs(output_dir)
    except:
        print('ERROR: Could not create output directory!')
        sys.exit(1)

i_col = args.c1
f_col = args.c2
i_sep = args.s1
f_sep = args.s2
invert_match = args.invert_match
records = dict()
with open(file_path, encoding='utf-8', errors='ignore') as fh:
    for line in fh:
        parts = line.strip().split(f_sep)
        n_parts = len(parts)
        if n_parts < f_col:
            print('ERROR: Columns are less than expected! Expected: %d, Actual: %d' % (f_col, n_parts))
            continue

        records[parts[f_col - 1]] = None

if os.path.isfile(output_path):
    os.remove(output_path)

with open(output_path, 'a', encoding='utf-8', errors='ignore') as oh:
    with open(input_path, encoding='utf-8', errors='ignore') as ih:
        for line in ih:
            parts = line.strip().split(i_sep)
            n_parts = len(parts)
            if n_parts < i_col:
                print('ERROR: Columns are less than expected! Expected: %d, Actual: %d' % (i_col, n_parts))
                continue

            if invert_match:
                if parts[i_col - 1] in records:
                    oh.write(line)
            else:
                if parts[i_col - 1] not in records:
                    oh.write(line)
