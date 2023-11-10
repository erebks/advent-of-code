#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Advent of Code 2021 Day 13 part 1 and 2

import re
import pdb
import numpy as np

i = open("day13_in.txt", "r")
lines = i.readlines()
i.close()

# Testinput
"""
lines = [ # After first fold yields 17 points
    "6,10\n",
    "0,14\n",
    "9,10\n",
    "0,3\n",
    "10,4\n",
    "4,11\n",
    "6,0\n",
    "6,12\n",
    "4,1\n",
    "0,13\n",
    "10,12\n",
    "3,4\n",
    "3,0\n",
    "8,4\n",
    "1,10\n",
    "2,14\n",
    "8,10\n",
    "9,0\n",
    "\n",
    "fold along y=7\n",
    "fold along x=5\n",
]
"""

points = []
instructions = []

maxX = 0
maxY = 0

for l in lines:
    s = re.sub('\n',"",l)
    # check if parsable as x,y
    try:
        x, y = re.split("\D",s)
        x = int(x)
        y = int(y)
        maxX = max(x,maxX)
        maxY = max(y,maxY)
        points.append((y,x)) # y,x for matrix
    except ValueError:
        # Check if parsable as "fold along axis=num"
        try:
            s = re.sub('fold along ',"",s)
            axis, num = re.split("=", s)
            instructions.append([axis, int(num)])
        except:
            pass

print(points)
print(instructions)

# Build matrix
mat = np.zeros((maxY+1, maxX+1), int)

# Fill matrix
for point in points:
    mat[point] = 1

print(mat)

# Fold
for inst in instructions:
    print("Instruction: %s"% inst)
    if inst[0] == 'x':
        # Fold vertically
        for i in range(len(mat[0])-inst[1]):
            mat[:,inst[1]-i] += mat[:,inst[1]+i]
        # Slice
        mat = mat[:,0:inst[1]]
    elif inst[0] == 'y':
        # Fold horizontally
        for i in range(len(mat)-inst[1]):
            mat[inst[1]-i,:] += mat[inst[1]+i,:]
        # Slice
        mat = mat[0:inst[1],:]
    else:
        raise ValueError("")
#    print(mat)

mat[mat>0] = 1

print(mat)

print("Answer: %d" %np.count_nonzero(mat>0))

# For pretty printing
for row in mat:
    row_str = ""
    for e in row:
        if e == 0:
            row_str += " "
        else:
            row_str += "#"
    print(row_str)

print(display)
