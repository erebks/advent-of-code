#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Advent of Code 2022
import re
import pdb
import numpy as np
import copy

i = open("day10_in.txt", "r")
i_lines = i.readlines()
i.close()

# Testinput -> BLA BLA erwartung
small_test = [
    'noop\n',
    'addx 3\n',
    'addx -5\n',
]

big_test = [
    'addx 15\n',
    'addx -11\n',
    'addx 6\n',
    'addx -3\n',
    'addx 5\n',
    'addx -1\n',
    'addx -8\n',
    'addx 13\n',
    'addx 4\n',
    'noop\n',
    'addx -1\n',
    'addx 5\n',
    'addx -1\n',
    'addx 5\n',
    'addx -1\n',
    'addx 5\n',
    'addx -1\n',
    'addx 5\n',
    'addx -1\n',
    'addx -35\n',
    'addx 1\n',
    'addx 24\n',
    'addx -19\n',
    'addx 1\n',
    'addx 16\n',
    'addx -11\n',
    'noop\n',
    'noop\n',
    'addx 21\n',
    'addx -15\n',
    'noop\n',
    'noop\n',
    'addx -3\n',
    'addx 9\n',
    'addx 1\n',
    'addx -3\n',
    'addx 8\n',
    'addx 1\n',
    'addx 5\n',
    'noop\n',
    'noop\n',
    'noop\n',
    'noop\n',
    'noop\n',
    'addx -36\n',
    'noop\n',
    'addx 1\n',
    'addx 7\n',
    'noop\n',
    'noop\n',
    'noop\n',
    'addx 2\n',
    'addx 6\n',
    'noop\n',
    'noop\n',
    'noop\n',
    'noop\n',
    'noop\n',
    'addx 1\n',
    'noop\n',
    'noop\n',
    'addx 7\n',
    'addx 1\n',
    'noop\n',
    'addx -13\n',
    'addx 13\n',
    'addx 7\n',
    'noop\n',
    'addx 1\n',
    'addx -33\n',
    'noop\n',
    'noop\n',
    'noop\n',
    'addx 2\n',
    'noop\n',
    'noop\n',
    'noop\n',
    'addx 8\n',
    'noop\n',
    'addx -1\n',
    'addx 2\n',
    'addx 1\n',
    'noop\n',
    'addx 17\n',
    'addx -9\n',
    'addx 1\n',
    'addx 1\n',
    'addx -3\n',
    'addx 11\n',
    'noop\n',
    'noop\n',
    'addx 1\n',
    'noop\n',
    'addx 1\n',
    'noop\n',
    'noop\n',
    'addx -13\n',
    'addx -19\n',
    'addx 1\n',
    'addx 3\n',
    'addx 26\n',
    'addx -30\n',
    'addx 12\n',
    'addx -1\n',
    'addx 3\n',
    'addx 1\n',
    'noop\n',
    'noop\n',
    'noop\n',
    'addx -9\n',
    'addx 18\n',
    'addx 1\n',
    'addx 2\n',
    'noop\n',
    'noop\n',
    'addx 9\n',
    'noop\n',
    'noop\n',
    'noop\n',
    'addx -1\n',
    'addx 2\n',
    'addx -37\n',
    'addx 1\n',
    'addx 3\n',
    'noop\n',
    'addx 15\n',
    'addx -21\n',
    'addx 22\n',
    'addx -6\n',
    'addx 1\n',
    'noop\n',
    'addx 2\n',
    'addx 1\n',
    'noop\n',
    'addx -10\n',
    'noop\n',
    'noop\n',
    'addx 20\n',
    'addx 1\n',
    'addx 2\n',
    'addx 2\n',
    'addx -6\n',
    'addx -11\n',
    'noop\n',
    'noop\n',
    'noop\n',
]

def part1(dryRun = False):
    print(f"PART 1, dryRun {dryRun}")
    if dryRun:
        lines = big_test
    else:
        lines = i_lines

    x = [1]

    for l in lines:
        if (l[0:4] == 'noop'):
            x.append(x[-1])
        elif (l[0:4] == 'addx'):
            x.append(x[-1])
            x.append(x[-1] + int(l[5:]))

    sum_strength = 0
    for i in range(20, 221, 40):
        strength = x[i-1]*i
        sum_strength += strength

    print(f"Answer: {sum_strength}")

def part2(dryRun = False):
    print(f"PART 2, dryRun {dryRun}")
    if dryRun:
        lines = big_test
    else:
        lines = i_lines

    x = [1]

    for l in lines:
        if (l[0:4] == 'noop'):
            x.append(x[-1])
        elif (l[0:4] == 'addx'):
            x.append(x[-1])
            x.append(x[-1] + int(l[5:]))

    display = []
    for crt in range(0, 240):
        if crt%40 in range(x[crt]-1, x[crt]+2):
            display.append('#')
        else:
            display.append(' ')

    print(f"{''.join(display[0:40])}")
    print(f"{''.join(display[40:80])}")
    print(f"{''.join(display[80:120])}")
    print(f"{''.join(display[120:160])}")
    print(f"{''.join(display[160:200])}")
    print(f"{''.join(display[200:240])}")

if __name__=="__main__":
    part1(dryRun = False)
    part2(dryRun = False)
