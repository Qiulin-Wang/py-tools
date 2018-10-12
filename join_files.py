# -*- coding: utf-8 -*-

# Copyright © 2018 by IBPort. All rights reserved.
# @Author: Neal Wong
# @Email: ibprnd@gmail.com

import os
import sys
import argparse

parser = argparse.ArgumentParser(description='Join two files by column.')
parser.add_argument('--i1', help='Input file 1.')
parser.add_argument('--i2', help='Input file 2.')
parser.add_argument('--f1', type=int, default=1, help='Join on this field of file 1, default is 1.')
parser.add_argument('--f2', type=int, default=1, help='Join on this field of file 2, default is 1.')
parser.add_argument('--s1', default='\t', help='Separator of file 1, default is tab.')
parser.add_argument('--s2', default='\t', help='Separator of file, default is tab.')
parser.add_argument('--so', default='\t', help='Separator of output file, default is tab.')
parser.add_argument(
    '-r', '--reserve_order', action='store_true',
    help='Whether reserve line order according to file 1.')
parser.add_argument('-o', '--output', help='Ouput file.')
args = parser.parse_args()

reserve_order = args.reserve_order
file1 = os.path.abspath(os.path.expanduser(args.i1))
file2 = os.path.abspath(os.path.expanduser(args.i2))
for f in [file1, file2]:
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

f1 = args.f1
f2 = args.f2
s1 = args.s1
s2 = args.s2
so = args.so
records = dict()
lines_cnt = 0
with open(file1, encoding='utf-8', errors='ignore') as fh:
    idx = 1
    for line in fh:
        parts = line.strip().split(s1)
        n_parts = len(parts)
        if n_parts < f1:
            print('ERROR: Columns are less than expected! Expected: %d, Actual: %d' % (f1, n_parts))
            continue

        key = parts[f1 - 1]
        if key in records:
            records[key]['data'].append({idx: list(parts)})
        else:
            records[key] = {'mapped': False, 'data': [{idx: list(parts)}]}

        idx += 1
    lines_cnt = idx - 1

max_col_cnt = 0
with open(file2, encoding='utf-8', errors='ignore') as ih:
    for line in ih:
        parts = line.strip().split(s2)
        n_parts = len(parts)
        if n_parts < f2:
            print('ERROR: Columns are less than expected! Expected: %d, Actual: %d' % (f2, n_parts))
            continue

        if n_parts > max_col_cnt:
            max_col_cnt = n_parts

        key = parts[f2 - 1]
        if key in records:
            if not records[key]['mapped']:
                records[key]['addition'] = list(parts)
                records[key]['mapped'] = True

if os.path.isfile(output_path):
    os.remove(output_path)

with open(output_path, 'a', encoding='utf-8', errors='ignore') as oh:
    fake_addition = []
    for i in range(0, max_col_cnt):
        fake_addition.append('')

    if reserve_order:
        lines = dict()

        for items in records.values():
            mapped = items.pop('mapped')
            data = items.pop('data')
            addition = items.pop('addition', fake_addition)
            for item in data:
                idx, line = item.popitem()
                line.extend(addition)
                lines[idx] = so.join(line)

        for idx in range(1, lines_cnt + 1):
            oh.write(lines[idx])
            oh.write("\n")
    else:
        for items in records.values():
            mapped = items.pop('mapped')
            data = items.pop('data')
            addition = items.pop('addition', fake_addition)
            for item in data:
                _, line = item.popitem()
                line.extend(addition)
                oh.write(so.join(line))
                oh.write("\n")
