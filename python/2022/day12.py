#!/usr/bin/env python3
# Advent of Code 2022

import re
import pdb
import numpy as np
import copy
import sys
import math

i = open("day12_in.txt", "r")
i_lines = i.readlines()
i.close()

# Testinput -> BLA BLA erwartung
dry_lines = [
    'Sabqponm\n',
    'abcryxxl\n',
    'accszExk\n',
    'acctuvwj\n',
    'abdefghi\n',
]

def getPossibleSteps(field, pos, maxElevationDiff=1):
    # Exactly up, down, left, right
    possibleSteps = []

    elevation = field[pos[0], pos[1]]

    # right
    if (pos[1]+1 < len(field[0])):
        posStep = (pos[0], pos[1]+1)
        el = field[posStep]
        if (elevation+maxElevationDiff >= el and not (elevation >= 2 and el == 0)):
            possibleSteps.append(posStep)

    # up
    if (pos[0] != 0):
        posStep = (pos[0]-1, pos[1])
        el = field[posStep]
        if (elevation+maxElevationDiff >= el and not (elevation >= 2 and el == 0)):
            possibleSteps.append(posStep)

    # low
    if (pos[0]+1 < len(field)):
        posStep = (pos[0]+1, pos[1])
        el = field[posStep]
        if (elevation+maxElevationDiff >= el and not (elevation >= 2 and el == 0)):
            possibleSteps.append(posStep)

    # left
    if (pos[1] != 0):
        posStep = (pos[0], pos[1]-1)
        el = field[posStep]
        if (elevation+maxElevationDiff >= el and not (elevation >= 2 and el == 0)):
            possibleSteps.append(posStep)

    return possibleSteps

def breadth_first_search(field, pos, end):

    v = {'parent': None, 'pos': pos}

    visited = [pos]
    explore = [v]

    while len(explore) > 0:
        v = explore.pop(0)

        if (v['pos'][0] == end[0] and v['pos'][1] == end[1]):
            return v

        for step in getPossibleSteps(field, v['pos']):
            if step not in visited:
                w = {'parent': v, 'pos': step}
                explore.append(w)
                visited.append(step)

    return []

def printPath(field, path):
    field = list(field)
    nfield = []

    for row in field:
        nrow = [chr(a + ord('a')) for a in list(row)]
        nfield.append(nrow)

    for node in path:
        nfield[node[0]][node[1]] = chr(field[node[0]][node[1]] + ord('A'))

    for row in nfield:
        print(''.join(row))

def part1(dryRun = False):
    print(f"PART 1, dryRun {dryRun}")
    if dryRun:
        lines = dry_lines
    else:
        lines = i_lines

    field = []
    start = []
    end = []

    # parse to matrix

    for row in range(len(lines)):
        field.append([])
        for col in range(len(lines[0])-1):
            if lines[row][col] == 'S':
                start = (row, col)
                field[row].append(0)
            elif lines[row][col] == 'E':
                end = (row, col)
                field[row].append(int(ord('z') - ord('a')))
            else:
                field[row].append(int(ord(lines[row][col]) - ord('a')))
    field = np.array(field)
    print(field)
    print(f"Start: {start}, End: {end}")

    goal = breadth_first_search(field, start, end)

    path = [goal['pos'], ]

    v = goal['parent']

    while True:
        if v['pos'] is start:
            break
        else:
            path.append(v['pos'])
            v = v['parent']

    printPath(field, path)
    print(f"Answer: {len(path)}")

def part2(dryRun = False):
    print(f"PART 2, dryRun {dryRun}")
    if dryRun:
        lines = dry_lines
    else:
        lines = i_lines

    field = []
    end = []
    elevation_a = []

    # parse to matrix

    for row in range(len(lines)):
        field.append([])
        for col in range(len(lines[0])-1):
            if lines[row][col] == 'S':
                field[row].append(0)
            elif lines[row][col] == 'E':
                end = (row, col)
                field[row].append(int(ord('z') - ord('a')))
            else:
                field[row].append(int(ord(lines[row][col]) - ord('a')))
                if lines[row][col] == 'a':
                    elevation_a.append((row,col))

    field = np.array(field)
    print(field)

    shortestPath = 10000000

    for start in elevation_a:
        print(f"Start: {start}, End: {end}")

        goal = breadth_first_search(field, start, end)

        if goal == []:
            continue

        path = [goal['pos']]

        v = goal['parent']

        while True:
            if v['pos'] is start:
                break
            else:
                path.append(v['pos'])
                v = v['parent']

        shortestPath = min(shortestPath, len(path))

    print(f"Answer: {shortestPath}")

    # Optimize by checking which 'a's are in a hole and save them in the visited list


if __name__=="__main__":
    part1(dryRun = False)
    part2(dryRun = False)
