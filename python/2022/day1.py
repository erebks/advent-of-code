#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Advent of Code 2022
import re
import pdb
import numpy as np
import copy

i = open("day1_in.txt", "r")
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

    elves = []
    elves.append(0)

    for line in lines:
        if line == '\n':
            elves.append(0)
        else:
            elves[-1] += int(line)

    print(f"Elve with the highest calories: {max(elves)}")

def part2(dryRun = False):
    print(f"PART 2, dryRun {dryRun}")
    if dryRun:
        lines = dry_lines
    else:
        lines = i_lines

    elves = []
    elves.append(0)

    for line in lines:
        if line == '\n':
            elves.append(0)
        else:
            elves[-1] += int(line)

    elves = np.sort(np.array(elves))

    print(f"Calories of top 3 elves: {sum(elves[-3:])}")

if __name__=="__main__":
    part1(dryRun = False)
    part2(dryRun = False)
