#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Advent of Code 2022
import re
import pdb
import numpy as np
import copy

i = open("day8_in.txt", "r")
i_lines = i.readlines()
i.close()

# Testinput -> BLA BLA erwartung
dry_lines = [
    '30373\n',
    '25512\n',
    '65332\n',
    '33549\n',
    '35390\n',
]

def part1(dryRun = False):
    print(f"PART 1, dryRun {dryRun}")
    if dryRun:
        lines = dry_lines
    else:
        lines = i_lines

    forrest = []
    for l in lines:
        forrest.append([int(t) for t in l[:-1]])

    forrest = np.array(forrest)

    visibleInterior = 0

    for row in range(1, len(forrest)-1):
        for col in range(1, len(forrest)-1):
            treeHeight = forrest[row,col]

            #print(f"North: {forrest[:row,col]}, South: {forrest[row+1:,col]}, East: {forrest[row,:col]}, West: {forrest[row,col+1:]}")
            north = max(forrest[:row,col])
            south = max(forrest[row+1:,col])
            east = max(forrest[row,:col])
            west = max(forrest[row,col+1:])

            if (treeHeight > north or
                treeHeight > south or
                treeHeight > east or
                treeHeight > west):
                #print(f"Tree @{row},{col} with height: {treeHeight} is visible")
                visibleInterior += 1

    visible = visibleInterior + 4*len(forrest)-4
    print(f"Answer: {visible}")


def part2(dryRun = False):
    print(f"PART 2, dryRun {dryRun}")
    if dryRun:
        lines = dry_lines
    else:
        lines = i_lines

    forrest = []
    for l in lines:
        forrest.append([int(t) for t in l[:-1]])

    forrest = np.array(forrest)

    bestTreeSize = 0

    #if you reach an edge or at the first tree that is the same height or taller
    for row in range(1, len(forrest)-1):
        for col in range(1, len(forrest)-1):
            treeHeight = forrest[row,col]

            north = np.flip(forrest[:row,col])
            south = forrest[row+1:,col]
            east = forrest[row,col+1:]
            west = np.flip(forrest[row,:col])

            northSteps = 0
            southSteps = 0
            eastSteps = 0
            westSteps = 0

#            print(f"North: {north}, South: {south}, East: {east}, West: {west}")

            # Find nearest tree in north
            try:
                northSteps = np.where(north >= treeHeight)[0][0] + 1
            except IndexError:
                # No tree bocks -> full length
                northSteps = len(north)

            # Find nearest tree in south
            try:
                southSteps = np.where(south >= treeHeight)[0][0] + 1
            except IndexError:
                # No tree found -> assume 1
                southSteps = len(south)

            # Find nearest tree in east
            try:
                eastSteps = np.where(east >= treeHeight)[0][0] + 1
            except IndexError:
                # No tree found -> assume 1
                eastSteps = len(east)

            # Find nearest tree in west
            try:
                westSteps = np.where(west >= treeHeight)[0][0] + 1
            except IndexError:
                # No tree found -> assume 1
                westSteps = len(west)

            size = northSteps * southSteps * eastSteps * westSteps
#            print(f"Size: {size}")

            if size > bestTreeSize:
                bestTreeSize = size

    print(f"Answer: {bestTreeSize}")

if __name__=="__main__":
    part1(dryRun = False)
    part2(dryRun = False)
