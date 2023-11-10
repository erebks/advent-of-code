#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Advent of Code 2022
import re
import pdb
import numpy as np
import copy

i = open("day18_in.txt", "r")
i_lines = i.readlines()
i.close()

# Testinput -> BLA BLA erwartung
dry_lines = [
    '2,2,2\n',
    '1,2,2\n',
    '3,2,2\n',
    '2,1,2\n',
    '2,3,2\n',
    '2,2,1\n',
    '2,2,3\n',
    '2,2,4\n',
    '2,2,6\n',
    '1,2,5\n',
    '3,2,5\n',
    '2,1,5\n',
    '2,3,5\n',
]

def part1(dryRun = False):
    print(f"PART 1, dryRun {dryRun}")
    if dryRun:
        lines = dry_lines
    else:
        lines = i_lines

def part2(dryRun = False):
    print(f"PART 2, dryRun {dryRun}")
    if dryRun:
        lines = dry_lines
    else:
        lines = i_lines

if __name__=="__main__":
    part1(dryRun = True)
    part2(dryRun = True)
