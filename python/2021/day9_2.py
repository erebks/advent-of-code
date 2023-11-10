#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Advent of Code 2021 Day 9 part 2

import re
import numpy as np
import copy
import pdb

i = open("day9_in.txt", "r")
lines = i.readlines()
i.close()

"""
# Testinput
# Top left Basin: size 3
# Top right basin: size 9
# middle basin: size 14
# bottom-right basin: size 9
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

for l in lines:
    l = re.sub("\n","",l)
    row=[]
    for entry in l:
        row.append(int(entry))
    maps.append(row)

maps = np.array(maps)
print(maps)

minima = []

for row in range(len(maps)):
    for col in range(len(maps[0])):
        N = (row-1 if row != 0 else row+1, col)
        S = (row+1 if row != len(maps)-1 else row-1, col)
        W = (row, col-1 if col != 0 else col+1)
        E = (row, col+1 if col != len(maps[0])-1 else col-1)
        print("Loc: %s -> N: %s, E: %s, S: %s, W: %s"%((row,col),N, E, S, W))
        if ( (maps[row,col] < maps[N]) and
             (maps[row,col] < maps[E]) and
             (maps[row,col] < maps[S]) and
             (maps[row,col] < maps[W])):
            # Minima found -> Save location -1 because we'll resize the matrix
            minima.append((row,col))

print(minima)

basins = []

# np.diff...?

# go N,E,S,W around pixel add to candidates with ID (row*(len(cols))+col)
# If N+E set -> check NE
# If ...
# Add to list of newpixels, and check if ID already is present -> omit
# Go through list of newpixels and do the same, if done -> add to list of done pixels

matrix_len = len(maps[0])

def convRowColToId(rowcol):
    return rowcol[0]*matrix_len + rowcol[1]

def convIdToRowCol(idn):
    col = int(idn%matrix_len)
    row = int((idn-col)/matrix_len)
    return (row, col)

sizes = []

for minimum in minima:
    pixels_searched = {}
    pixels_todo = []
    i = 0

    pixels_searched[str(convRowColToId(minimum))] = True # minimum itself is known

    row = minimum[0]
    col = minimum[1]

    N = (row-1 if row != 0 else row+1, col)
    S = (row+1 if row != len(maps)-1 else row-1, col)
    W = (row, col-1 if col != 0 else col+1)
    E = (row, col+1 if col != len(maps[0])-1 else col-1)

    if (maps[N] != 9):
        pixels_todo.append(N)
    else:
        pixels_searched[str(convRowColToId(N))] = False

    if (maps[E] != 9):
        pixels_todo.append(E)
    else:
        pixels_searched[str(convRowColToId(E))] = False

    if (maps[S] != 9):
        pixels_todo.append(S)
    else:
        pixels_searched[str(convRowColToId(S))] = False

    if (maps[W] != 9):
        pixels_todo.append(W)
    else:
        pixels_searched[str(convRowColToId(W))] = False

    print("minimum: %s -> pixels_todo: %s, pixels_searched: %s" %(minimum, pixels_todo, pixels_searched))
    while (len(pixels_todo) != 0):
        row, col = pixels_todo.pop()
        N = (row-1 if row != 0 else row+1, col)
        S = (row+1 if row != len(maps)-1 else row-1, col)
        W = (row, col-1 if col != 0 else col+1)
        E = (row, col+1 if col != len(maps[0])-1 else col-1)

        pixels_searched[str(convRowColToId((row,col)))] = True

        if (maps[N] != 9):
            # Check if alrady in pix_searched
            try:
                pix = pixels_searched[str(convRowColToId(N))]
            except KeyError:
                pixels_todo.append(N)
        else:
            pixels_searched[str(convRowColToId(N))] = False

        if (maps[E] != 9):
            try:
                pix = pixels_searched[str(convRowColToId(E))]
            except KeyError:
                pixels_todo.append(E)
        else:
            pixels_searched[str(convRowColToId(E))] = False

        if (maps[S] != 9):
            try:
                pix = pixels_searched[str(convRowColToId(S))]
            except KeyError:
                pixels_todo.append(S)
        else:
            pixels_searched[str(convRowColToId(S))] = False

        if (maps[W] != 9):
            try:
                pix = pixels_searched[str(convRowColToId(W))]
            except KeyError:
                pixels_todo.append(W)
        else:
            pixels_searched[str(convRowColToId(W))] = False

        i += 1
        print("Round: %d, pix_searched: %s, pix_todo: %s"%(i, pixels_searched, pixels_todo))

    siz = 0
    for idn in pixels_searched:
        if (pixels_searched[idn] == True):
            siz += 1
    sizes.append(siz)


print("Sizes: %s"%sizes)

sizes = np.sort(np.array(sizes))

print("Answer: %d" % (sizes[-1] * sizes[-2] * sizes[-3]))
