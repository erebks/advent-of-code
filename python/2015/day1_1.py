#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Advent of Code 2015 Day 1 part 1 & 2

import re
import pdb
import numpy as np
import copy

i = open("day1_in.txt", "r")
lines = i.readlines()
i.close()

for l in lines:
    l = re.sub("\n","",l)
    row = []

i = lines[0]

floor = 0

for count, e in enumerate(i):
    if e == '(':
        floor += 1
    elif e == ')':
        floor -= 1
    else:
        print("ERROR")

print("PART1: Santa is at floor {0}".format(floor))


floor = 0

for count, e in enumerate(i):
    if e == '(':
        floor += 1
    elif e == ')':
        floor -= 1
    else:
        print("ERROR")

    ### DAY 1 part 2
    if floor < 0:
        break

print("PART2: Santa is at floor {0} at pos {1}".format(floor, count+1))
