#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Advent of Code 2021 Day 7 part 2

import re
import numpy as np
import copy

i = open("day7_in.txt", "r")
lines = i.readlines()
i.close()

# Test input -> Should yield pos 5 with total fuel of 168

"""
lines = [
    "16,1,2,0,4,2,7,1,2,14\n",
]
"""

def little_gaus(n):
    return (n*(n+1))/2

for l in lines:
    crabs = re.split("\D", re.sub("\n","",l))
    crabs = list(map(int,crabs))
    crabs = np.array(crabs)
    print("Input vector: "+str(crabs))

fuel = []

for i in range(np.amax(crabs)):
    cons = 0
    for crab in crabs:
        cons += little_gaus(abs(crab-i))
    fuel.append(cons)

min_fuel = np.amin(fuel)
pos = np.where(fuel == min_fuel)

print("Answer: "+str(np.amin(fuel))+" @: "+str(pos))
