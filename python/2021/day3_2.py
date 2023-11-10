#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Advent of Code 2021 Day 3 part 2

import numpy as np
import copy

i = open("day3_in.txt", "r")
lines = i.readlines()
i.close()
mat = []

"""
# Test input -> Should yield oxygen_gen = 23; co2_scrubber = 10
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

# Convert to bool-matrix

for l in lines:
    row = []
    for bit in l:
        try:
            row.append(bool(int(bit)))
        except:
            continue

    mat.append(row)

# convert to np array
mat = np.array(mat)

# Numpy magic in use:
# bool(np.bincount(arr[:,2]).argmax()) -> Majority and False when equal
# ~bool(np.bincount(arr[:,2]).argmax()) -> Minority and True when equal
# arr[np.where(arr[:,0] == True)] -> select only rows with True in first bla

def boolMajority(arr):
    c = np.bincount(arr)
    if len(c) > 1:
        if c[0] == c[1]:
            return True

    return bool(c.argmax())

def boolMinority(arr):
    maj = boolMajority(arr)
    if maj == True:
        return False
    else:
        return True

# Oxygen generator rating
# Keep only rows with most common bit
# If equal -> keep values with 1
# Stop when only one left

oxygen_mat = copy.deepcopy(mat)
for i in range(len(oxygen_mat[0])):

    if len(oxygen_mat) == 1:
        break

    majority = boolMajority(oxygen_mat[:,i])
    print("Col: "+str(i)+" -> "+str(oxygen_mat[:,i])+", Majority: "+str(majority))
    oxygen_mat = oxygen_mat[np.where(oxygen_mat[:,i] == majority)]
    print(oxygen_mat)

# Convert array of bit to int
oxygen_gen = 0
for bit in oxygen_mat[0]:
    oxygen_gen = (oxygen_gen << 1) | bit

print(oxygen_gen)

# CO2 scrubber rating
# Keep only rows with least common bit
# If equal -> keep only values with 0
# Stop when only one left

co2_mat = copy.deepcopy(mat)

for i in range(len(co2_mat[0])):

    if len(co2_mat) == 1:
        break

    minority = boolMinority(co2_mat[:,i])
    print("Col: "+str(i)+" -> "+str(co2_mat[:,i])+", Minority: "+str(minority))
    co2_mat = co2_mat[np.where(co2_mat[:,i] == minority)]
    print(co2_mat)

# Convert array of bit to int
co2_gen = 0
for bit in co2_mat[0]:
    co2_gen = (co2_gen << 1) | bit

print(co2_gen)


print("oxygen_gen: "+str(oxygen_gen)+", co2_gen: "+str(co2_gen)+", Answer: "+str(co2_gen*oxygen_gen))
