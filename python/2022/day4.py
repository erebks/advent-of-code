#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Advent of Code 2022
import re
import pdb
import numpy as np
import copy

i = open("day4_in.txt", "r")
i_lines = i.readlines()
i.close()

# Testinput -> BLA BLA erwartung
dry_lines = [
    '2-4,6-8\n',
    '2-3,4-5\n',
    '5-7,7-9\n',
    '2-8,3-7\n',
    '6-6,4-6\n',
    '2-6,4-8\n',
]

def part1(dryRun = False):
    print(f"PART 1, dryRun {dryRun}")
    if dryRun:
        lines = dry_lines
    else:
        lines = i_lines

    fully = 0

    for l in lines:
        l = re.sub('\n', '', l)
        sec1, sec2 = [re.split('-', e) for e in re.split(',', l)]
        sec1 = list(map(int, sec1))
        sec2 = list(map(int, sec2))

        sec1 = [e for e in range(sec1[0], sec1[1]+1)]
        sec2 = [e for e in range(sec2[0], sec2[1]+1)]

        if (set(sec1) <= set(sec2) or
            set(sec1) >= set(sec2)):
            fully += 1

    print(f"Result: {fully}")

def part2(dryRun = False):
    print(f"PART 2, dryRun {dryRun}")
    if dryRun:
        lines = dry_lines
    else:
        lines = i_lines

    partial = 0

    for l in lines:
        l = re.sub('\n', '', l)
        sec1, sec2 = [re.split('-', e) for e in re.split(',', l)]
        sec1 = list(map(int, sec1))
        sec2 = list(map(int, sec2))

        sec1 = [e for e in range(sec1[0], sec1[1]+1)]
        sec2 = [e for e in range(sec2[0], sec2[1]+1)]

        if ((sec1[0] in sec2) or
            (sec1[-1] in sec2) or
            (sec2[0] in sec1) or
            (sec2[-1] in sec1)):
            partial += 1

    print(f"Result: {partial}")

if __name__=="__main__":
    part1(dryRun = False)
    part2(dryRun = False)
