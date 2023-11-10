#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Advent of Code 2022
import re
import pdb
import numpy as np
import copy

i = open("day7_in.txt", "r")
i_lines = i.readlines()
i.close()

# Testinput -> BLA BLA erwartung
dry_lines = [
    '$ cd /\n',
    '$ ls\n',
    'dir a\n',
    '14848514 b.txt\n',
    '8504156 c.dat\n',
    'dir d\n',
    '$ cd a\n',
    '$ ls\n',
    'dir e\n',
    '29116 f\n',
    '2557 g\n',
    '62596 h.lst\n',
    '$ cd e\n',
    '$ ls\n',
    '584 i\n',
    '$ cd ..\n',
    '$ cd ..\n',
    '$ cd d\n',
    '$ ls\n',
    '4060174 j\n',
    '8033020 d.log\n',
    '5626152 d.ext\n',
    '7214296 k\n',
]

filesystem = {'/': {'dirsize': None, 'files':[]}}

def getPathsOfSubdirs(filesystem, start):
    paths = [k for k in filesystem]

    paths.sort()

    relevant = []
    for path in paths:
        if re.match(start+".+", path):
            relevant.append(path)

    return relevant

def getSizeOfDirWithSubdirs(filesystem, start):
    totsize = sum([f['size'] for f in filesystem[start]['files']])
    for path in getPathsOfSubdirs(filesystem, start):
        totsize += sum([f['size'] for f in filesystem[path]['files']])

    filesystem[start]['dirsize'] = totsize
    return totsize

def part1(dryRun = False):
    print(f"PART 1, dryRun {dryRun}")
    if dryRun:
        lines = dry_lines
    else:
        lines = i_lines

    pos = ['/',]

    for l in lines:
        p = re.split(' ', re.sub('\n', '',l))
        abspath = '/'+'/'.join(pos[1:])
        if p[0] == '$':
            if p[1] == 'cd':
                d = p[2]
                print(f"Got command: {p[1]} {d}")

                if p[2] == '..':
                    print(f"\tleaving dir {pos.pop()}")
                elif p[2] == '/':
                    pos = ['/',]
                    abspath = '/'.join(pos[1:])
                    print(f"\tTo the top. Pos: {abspath}")
                else:
                    pos.append(p[2])
                    abspath = '/'+'/'.join(pos[1:])
                    if abspath not in filesystem:
                        print(f"\tAdding new directory in: {abspath}")
                        filesystem[abspath] = {'dirsize': None, 'files':[]}

#            elif p[1] == 'ls':
#                print(f"{p[1]}")

        else:
            if (p[0] == 'dir'):
                continue

            print(f"File: {p[1]} Size: {p[0]}")

            print(f"\tAdding new file at pos: {abspath}")
            f = {'name':p[1], 'size':int(p[0])}
            filesystem[abspath]['files'].append(f)

    print(f"FS:{filesystem}")


    paths = sorted([k for k in filesystem], key=len, reverse=True)

    sizUnder100k = 0
    for path in paths:
        siz = getSizeOfDirWithSubdirs(filesystem, path)
        if siz < 100000:
            sizUnder100k += siz
        print(f"Dir: {path}: {getSizeOfDirWithSubdirs(filesystem, path)}")

    print(f"Result: {sizUnder100k}")

def part2(dryRun = False):
    print(f"PART 2, dryRun {dryRun}")
    if dryRun:
        lines = dry_lines
    else:
        lines = i_lines

    spaceFree = 70000000 - getSizeOfDirWithSubdirs(filesystem, '/')
    spaceNeeded = 30000000 - spaceFree
    # Calculate size to free:
    print(f"SpaceFree: {spaceFree}, Needed: {spaceNeeded}")

    # Directory just above speceNeeded

    dirs = sorted([(key, val['dirsize']) for key, val in filesystem.items() if val['dirsize'] > spaceNeeded], key=lambda a: a[1])

    print(f"Answer: Deleting {dirs[0][0]} frees: {dirs[0][1]}")

if __name__=="__main__":
    part1(dryRun = False)
    part2(dryRun = False)
