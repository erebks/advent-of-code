#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Advent of Code 2022
import re
import pdb
import numpy as np
import copy

i = open("day14_in.txt", "r")
i_lines = i.readlines()
i.close()

# Testinput -> BLA BLA erwartung
dry_lines = [
    '498,4 -> 498,6 -> 496,6\n',
    '503,4 -> 502,4 -> 502,9 -> 494,9\n',
]

class Rockline():
    def __init__(self, idn, edges):
        self.idn = idn
        self.edges = edges

        self.points = []

        for iedge in range(len(edges)-1):
            [self.points.append(x) for x in self._draw(edges[iedge], edges[iedge+1])]

    def _draw(self, start_edge, end_edge):

        dx = end_edge[0] - start_edge[0]
        dy = end_edge[1] - start_edge[1]

        line = []

        if dx != 0 and dy != 0:
            print("PROBLEM!")

        elif dx != 0:
            if dx > 0:
                for i in range(dx+1):
                    line.append((start_edge[0]+i, start_edge[1]))
            else:
                for i in range(abs(dx)+1):
                    line.append((end_edge[0]+i, end_edge[1]))

        elif dy != 0:
            if dy > 0:
                for i in range(dy+1):
                    line.append((start_edge[0], start_edge[1]+i))
            else:
                for i in range(abs(dy)+1):
                    line.append((end_edge[0], end_edge[1]+i))

        return line

    def isAtPos(self, pos):
        if pos in self.points:
            return True

        return False

    def getPoints(self):
        return self.points

def dropSand(field, maxY, offset=0):
    pos = [500+offset,0]

    while True:
        # Move down until obstacle => increase y
        if pos[1] + 1 >= maxY:
            return [False, pos]

        if field[pos[1] + 1, pos[0]] == 0:
            pos[1] += 1
        else:
            if field[pos[1] + 1, pos[0]-1] == 0:
                pos[1] += 1
                pos[0] -= 1
            elif field[pos[1] + 1, pos[0]+1] == 0:
                pos[1] += 1
                pos[0] += 1
            else:
                return [True, pos]

def printField(field, spanX, spanY):
    minX, maxX = spanX
    minY, maxY = spanY

    for row in range(minY, maxY):
        s = []
        for col in range(minX, maxX):
            if field[row, col] == 1:
                s.append('#')
            elif field[row, col] == 2:
                s.append('+')
            elif field[row, col] == 3:
                s.append('o')
            else:
                s.append('-')
        print(''.join(s))

def printField_2(field):
    for row in range(len(field)):
        s = []
        for col in range(len(field[0])):
            if field[row, col] == 1:
                s.append('#')
            elif field[row, col] == 2:
                s.append('+')
            elif field[row, col] == 3:
                s.append('o')
            else:
                s.append('-')
        print(''.join(s))


def part1(dryRun = False):
    print(f"PART 1, dryRun {dryRun}")
    if dryRun:
        lines = dry_lines
    else:
        lines = i_lines

    rocklines = []
    idn = 0

    for l in lines:
        edges = [[int(x), int(y)] for x,y in [re.split(',', a) for a in re.split(' -> ', l[:-1])]]
        rockline = Rockline(idn,edges)
        idn += 1
        rocklines.append(rockline)

    rocks = []
    maxX = 0
    maxY = 0
    minX = 600
    minY = 0
    # gather all points
    for rockline in rocklines:
        for point in rockline.getPoints():
            rocks.append(point)
            minX = min(minX, point[0])
            minY = min(minY, point[1])
            maxX = max(maxX, point[0]+1)
            maxY = max(maxY, point[1]+1)

    spanX = [minX, maxX]
    spanY = [minY, maxY]

    print(rocks)
    field = np.zeros([maxY, maxX], int)

    for point in rocks:
        field[point[1],point[0]] = 1

    field[0, 500] = 2

    drops = 0
    while True:
        landed, pos = dropSand(field, maxY)
        if landed:
            field[pos[1], pos[0]] = 3
            drops += 1
        else:
            break

    printField(field, spanX, spanY)
    print(f"Anwer: {drops}")

    # NUMPY 2D ARRAY
    # TL;DR -> use A[y,x]

    # AR[0,1] => first row; 2nd element
    # => x = 0; y = 1 "A[x,y]"
    # y ->
    # .#..
    # ....
    # ....
    # ....
    # But AOC wants
    # x ->
    # .#..
    # ....
    # ....
    # ....

def part2(dryRun = False):
    print(f"PART 2, dryRun {dryRun}")
    if dryRun:
        lines = dry_lines
    else:
        lines = i_lines

    rocklines = []
    idn = 0

    for l in lines:
        edges = [[int(x), int(y)] for x,y in [re.split(',', a) for a in re.split(' -> ', l[:-1])]]
        rockline = Rockline(idn,edges)
        idn += 1
        rocklines.append(rockline)

    rocks = []
    maxX = 0
    maxY = 0
    minX = 600
    minY = 0
    # gather all points
    for rockline in rocklines:
        for point in rockline.getPoints():
            rocks.append(point)
            minX = min(minX, point[0])
            minY = min(minY, point[1])
            maxX = max(maxX, point[0]+1)
            maxY = max(maxY, point[1]+1)

    # All these max and min come from part 1

    floorY = maxY + 1

    # Use it to center the sand entry point (Essentially a pyramid grows)
    offset = (floorY - 1) + 2 - 500 # => "x=500"
    xSize = (floorY - 1)*2 + 2 + 2 +1

    field = np.zeros([floorY+1, xSize], int)

    for point in rocks:
        field[point[1],point[0]+offset] = 1

    field[0, 500+offset] = 2

    # floor -1 => highest ebene

    # Need to have at least (500 - floor) * 2 + 2 in x

    # Add a floor spanning from left to right
    for i in range(xSize):
        field[floorY, i] = 1

    drops = 0
    while True:

        landed, pos = dropSand(field, floorY+1, offset)
        if landed:
            field[pos[1], pos[0]] = 3
            drops += 1
            if pos == [500+offset, 0]:
                break
        else:
            break

    printField_2(field)

    print(f"Anwer: {drops}")

if __name__=="__main__":
    part1(dryRun = False)
    part2(dryRun = False)
