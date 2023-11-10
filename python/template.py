#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Advent of Code 2022
import re
import pdb
import numpy as np
import copy

i = open("dayx_in.txt", "r")
i_lines = i.readlines()
i.close()

# Testinput -> BLA BLA erwartung
dry_lines = [
    '1000\n',
    '2000\n',
    '3000\n',
    '\n',
    '4000\n',
    '\n',
    '5000\n',
    '6000\n',
    '\n',
    '7000\n',
    '8000\n',
    '9000\n',
    '\n',
    '10000\n',
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
