#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Advent of Code 2022
import re
import pdb
import numpy as np
import copy

i = open("day2_in.txt", "r")
i_lines = i.readlines()
i.close()

# Testinput -> total score 15
dry_lines = [
    'A Y\n',
    'B X\n',
    'C Z\n',
]

wl = [
    [3, 0, 6],
    [6, 3, 0],
    [0, 6, 3],
]

def part1(dryRun = False):
    print(f"PART 1, dryRun {dryRun}")
    if dryRun:
        lines = dry_lines
    else:
        lines = i_lines

    total_score = 0
    for l in lines:
        score = ord(l[2])-ord('X')+1 + wl[ord(l[2])-ord('X')][ord(l[0])-ord('A')]
        print(f"P1: {l[0]}, P2: {l[2]} -> wl: {wl[ord(l[2])-ord('X')][ord(l[0])-ord('A')]} score: {score}")

        total_score += score

    print(f"Total score: {total_score}")

rps = [
    [3, 1, 2],
    [1, 2, 3],
    [2, 3, 1],
]

def part2(dryRun = False):
    print(f"PART 2, dryRun {dryRun}")
    if dryRun:
        lines = dry_lines
    else:
        lines = i_lines

    total_score = 0
    for l in lines:
        score = (ord(l[2])-ord('X'))*3 + rps[ord(l[2])-ord('X')][ord(l[0])-ord('A')]
        print(f"P1: {l[0]}, wl: {l[2]} -> P2: {rps[ord(l[2])-ord('X')][ord(l[0])-ord('A')]} score: {score}")

        total_score += score

    print(f"Total score: {total_score}")


if __name__=="__main__":
    part1(dryRun = False)
    part2(dryRun = False)
