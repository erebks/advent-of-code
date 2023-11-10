#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Advent of Code 2022
import re
import pdb
import numpy as np
import copy

i = open("day6_in.txt", "r")
i_lines = i.readlines()
i.close()

# Testinput -> BLA BLA erwartung
dry_lines = [
    'mjqjpqmgbljsphdztnvjfqwrcgsmlb\n',
    'bvwbjplbgvbhsrlpgdmjqwftvncz\n',
    'nppdvjthqldpwncqszvftbrmjlhg\n',
    'nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg\n',
    'zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw\n',
]

def part1(dryRun = False):
    print(f"PART 1, dryRun {dryRun}")
    if dryRun:
        lines = dry_lines
    else:
        lines = i_lines

    for l in lines:
        msg = l[:-1]

        for idx in range(len(msg)-3):
            kernel = [msg[i] for i in range(idx, idx+4)]
            if len(set(kernel)) == len(kernel):
                print(f"SOP: {kernel}, index last char: {idx+4}")
                break

def part2(dryRun = False):
    print(f"PART 2, dryRun {dryRun}")
    if dryRun:
        lines = dry_lines
    else:
        lines = i_lines

    for l in lines:
        msg = l[:-1]

        for idx in range(len(msg)-13):
            kernel = [msg[i] for i in range(idx, idx+14)]
            if len(set(kernel)) == len(kernel):
                print(f"SOP: {kernel}, index last char: {idx+14}")
                break

if __name__=="__main__":
    part1(dryRun = False)
    part2(dryRun = False)
