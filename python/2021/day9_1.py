#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Advent of Code 2021 Day 9 part 1

import re
import numpy as np
import copy
import pdb

i = open("day9_in.txt", "r")
lines = i.readlines()
i.close()

"""
# Testinput -> output -> Sum of minima: 15
lines = [
    "2199943210\n",
    "3987894921\n",
    "9856789892\n",
    "8767896789\n",
    "9899965678\n",
]
"""

maps = [] # Holds matrix with 0 at the edges

# Determine len of row
l = re.sub("\n","",lines[0])
maps.append([int(9) for i in range(len(l)+2)])

for l in lines:
    l = re.sub("\n","",l)
    row=[]
    row.append(9)
    for entry in l:
        row.append(int(entry))
    row.append(9)
    maps.append(row)

maps.append([int(9) for i in range(len(maps[0]))])
maps = np.array(maps)
print(maps)

minima = []
sum_of_minima = 0

for row in range(1,len(maps)-1):
    for col in range(1,len(maps[0])-1):
        if ( (maps[row,col] < maps[row-1,col]) and
             (maps[row,col] < maps[row+1,col]) and
             (maps[row,col] < maps[row,col-1]) and
             (maps[row,col] < maps[row,col+1])):
            minima.append((row,col))
            sum_of_minima += maps[row,col]+1
print(minima)

print("Answer: "+str(sum_of_minima))
