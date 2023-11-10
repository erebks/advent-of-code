#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Advent of Code 2022
import re
import pdb
import numpy as np
import copy

i = open("day5_in.txt", "r")
i_lines = i.readlines()
i.close()

# Testinput -> BLA BLA erwartung
dry_lines = [
    '    [D]    \n',
    '[N] [C]    \n',
    '[Z] [M] [P]\n',
    ' 1   2   3 \n',
    '\n',
    'move 1 from 2 to 1\n',
    'move 3 from 1 to 3\n',
    'move 2 from 2 to 1\n',
    'move 1 from 1 to 2\n',
]

dry_stacks = [
    ['Z', 'N'],
    ['M', 'C', 'D'],
    ['P']
]

real_stacks = [
    ['Z', 'J', 'N', 'W', 'P', 'S'],
    ['G', 'S', 'T'],
    ['V', 'Q', 'R', 'L', 'H'],
    ['V', 'S', 'T', 'D'],
    ['Q', 'Z', 'T', 'D', 'B', 'M', 'J'],
    ['M', 'W', 'T', 'J', 'D', 'C', 'Z', 'L'],
    ['L', 'P', 'M', 'W', 'G', 'T', 'J'],
    ['N', 'G', 'M', 'T', 'B', 'F', 'Q', 'H'],
    ['R', 'D', 'G', 'C', 'P', 'B', 'Q', 'W'],
]

def part1(dryRun = False):
    print(f"PART 1, dryRun {dryRun}")
    if dryRun:
        lines = copy.deepcopy(dry_lines)
        stacks = copy.deepcopy(dry_stacks)
    else:
        lines = copy.deepcopy(i_lines)
        stacks = copy.deepcopy(real_stacks)

    print(f"Stacks initial: {stacks}")

    for l in lines:
        if l[0] != 'm':
            continue

        dummy1, cnt, dummy2, f, dummy3, t = re.split(' ', l[:-1])

        cnt = int(cnt)
        f = int(f)
        t = int(t)

        crane = [stacks[f-1].pop() for e in range(cnt)]
        stacks[t-1] += crane

    top = ""
    for e in stacks:
        top += str(e[-1])

    print(top)


def part2(dryRun = False):
    print(f"PART 2, dryRun {dryRun}")
    if dryRun:
        lines = copy.deepcopy(dry_lines)
        stacks = copy.deepcopy(dry_stacks)
    else:
        lines = copy.deepcopy(i_lines)
        stacks = copy.deepcopy(real_stacks)

    print(f"Stacks initial: {stacks}")

    for l in lines:
        if l[0] != 'm':
            continue

        dummy1, cnt, dummy2, f, dummy3, t = re.split(' ', l[:-1])

        cnt = int(cnt)
        f = int(f)-1
        t = int(t)-1

        stacks[t] += stacks[f][-cnt:]
        stacks[f] = stacks[f][:-cnt]

    top = ""
    for e in stacks:
        if len(e) > 0:
            top += str(e[-1])

    print(top)

if __name__=="__main__":
    part1(dryRun = False)
    part2(dryRun = False)
