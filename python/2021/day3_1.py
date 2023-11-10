#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Advent of Code 2021 Day 3 part 1

import numpy as np

i = open("day3_in.txt", "r")
lines = i.readlines()
i.close()
o = []
o_inverted = []

"""
# Test input -> Should yield gamma = 22; epsilon = 9; multiply -> 198
lines = [
    "00100\n",
    "11110\n",
    "10110\n",
    "10111\n",
    "10101\n",
    "01111\n",
    "00111\n",
    "11100\n",
    "10000\n",
    "11001\n",
    "00010\n",
    "01010\n",
]
"""

# Convert to matrix

for l in lines:
    row = []
    for bit in l:
        try:
            row.append(int(bit))
        except:
            continue

    o.append(row)

    row = []
    for bit in l:
        try:
            row.append(int(bit)^0x1)
        except:
            continue

    o_inverted.append(row)

# convert to np array
o = np.array(o)
o_inverted = np.array(o_inverted)

gamma_array = []
epsilon_array = []

for i in range(len(o[0])):
    gamma_array.append(int(np.round(np.average(o[:,i]), 0)))
    epsilon_array.append(int(np.round(np.average(o_inverted[:,i]), 0)))

# Convert array of bit to int
gamma = 0
for bit in gamma_array:
    gamma = (gamma << 1) | bit

epsilon = 0
for bit in epsilon_array:
    epsilon = (epsilon << 1) | bit


print(gamma)
print(epsilon)

print("gamma: "+str(gamma)+", epsilon: "+str(epsilon)+", Answer: "+str(gamma*epsilon))
