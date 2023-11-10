#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Advent of Code 2022
import re
import pdb
import numpy as np
import copy

i = open("day3_in.txt", "r")
i_lines = i.readlines()
i.close()

# Testinput -> BLA BLA erwartung
dry_lines = [
    'vJrwpWtwJgWrhcsFMMfFFhFp\n',
    'jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL\n',
    'PmmdzqPrVvPwwTWBwg\n',
    'wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn\n',
    'ttgJtRGJQctTZtZT\n',
    'CrZsJsPPZsGzwwsLwLmpwMDw\n',
]

def getPrio(item):
    if (ord(item) >= ord('a') and ord(item) <= ord('z')):
        return ord(item)-ord('a')+1

    elif (ord(item) >= ord('A') and ord(item) <= ord('Z')):
        return ord(item)-ord('A')+27

def part1(dryRun = False):
    print(f"PART 1, dryRun {dryRun}")
    if dryRun:
        lines = dry_lines
    else:
        lines = i_lines

    score = 0

    for l in lines:
        l = re.sub('\n', "", l)

        c1 = l[:int(len(l)/2)]
        c2 = l[int(len(l)/2):]

        item = None
        for ele in c1:
            if ele in c2:
                item = ele
                score += getPrio(item)
                break

    print(f"Score: {score}")


def part2(dryRun = False):
    print(f"PART 2, dryRun {dryRun}")
    if dryRun:
        lines = dry_lines
    else:
        lines = i_lines

    score = 0
    for idx in range(0, len(lines), 3):
        r1 = sorted(set(re.sub('\n', "", lines[idx])), key=str.lower)
        r2 = sorted(set(re.sub('\n', "", lines[idx+1])), key=str.lower)
        r3 = sorted(set(re.sub('\n', "", lines[idx+2])), key=str.lower)

        for ele in r1:
            if ele in r2 and ele in r3:
                score += getPrio(ele)

    print(f"Total score: {score}")

if __name__=="__main__":
    part1(dryRun = False)
    part2(dryRun = False)
