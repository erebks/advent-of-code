#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Advent of Code 2021 Day 7 part 1

import re
import numpy as np
import copy

i = open("day7_in.txt", "r")
lines = i.readlines()
i.close()

# Test input -> Should yield pos 2 with total fuel of 37

"""
lines = [
    "16,1,2,0,4,2,7,1,2,14\n",
]
"""

for l in lines:
    initial = re.split("\D", re.sub("\n","",l))
    initial = list(map(int,initial))
    initial = np.array(initial)
    print("Input vector: "+str(initial))
    crabs = np.array(initial)

median = np.median(crabs)

print("Median is: "+str(median))

fuel = 0

for crab in crabs:
    fuel += abs(crab-median)

print("Answer: "+str(fuel))
