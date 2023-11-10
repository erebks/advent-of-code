#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Advent of Code 2021 Day 5 faster version

import re
import numpy as np
import math

i = open("day5_in.txt", "r")
lines = i.readlines()
i.close()

# Test input -> Should yield 5
# .......1..
# ..1....1..
# ..1....1..
# .......1..
# .112111211
# ..........
# ..........
# ..........
# ..........
# 222111....

"""
lines = [
    "0,9 -> 5,9\n",
    "8,0 -> 0,8\n",
    "9,4 -> 3,4\n",
    "2,2 -> 2,1\n",
    "7,0 -> 7,4\n",
    "6,4 -> 2,0\n",
    "0,9 -> 2,9\n",
    "3,4 -> 1,4\n",
    "0,0 -> 8,8\n",
    "5,5 -> 8,2\n",
]
"""

# class of a smoker line
class SmokerLine:
    def __init__(self, start, end):
        self.start = start  # Array of [x,y]
        self.end = end      # Array of [x,y]
        self.xRange = [min(start[0],end[0]), max(start[0],end[0])]
        self.yRange = [min(start[1],end[1]), max(start[1],end[1])]

        delta = [self.start[0] - self.end[0], self.start[1] - self.end[1]]

        self.direction = None

        if delta == [0,0]:
            # Does not move! -> Impossible
            self.direction = None
        elif (delta[0] == 0):
            # Does not move in x-dir
            if (delta[1] > 0):
                # South
                self.direction = 'S'
            else:
                # North
                self.direction = 'N'
        elif (delta[1] == 0):
            # Does not move in y-dir
            if (delta[0] > 0):
                # West
                self.direction = 'W'
            else:
                # East
                self.direction = 'E'
        else:
            if (delta[0] > 0 and delta[1] > 0):
                # South West
                self.direction = "SW"
            elif (delta[0] > 0 and delta[1] < 0):
                # North West
                self.direction = "NW"
            elif (delta[0] < 0 and delta[1] < 0):
                # North East
                self.direction = "NE"
            elif (delta[0] < 0 and delta[1] > 0):
                # South East
                self.direction = "SE"

    def __str__(self):
        return "["+str(self.start)+"->"+str(self.end)+", xRange: "+str(self.xRange)+", yRange: "+str(self.yRange)+", direction: "+str(self.direction)+"]"
    def __repr__(self):
        return "["+str(self.start)+"->"+str(self.end)+", xRange: "+str(self.xRange)+", yRange: "+str(self.yRange)+", direction: "+str(self.direction)+"]"

    def drawField(self, size):
        # Draw a full map of the smokerline with given size
        field = np.zeros(size, dtype=int)

        # Now draw the line
        pos = self.start
        # Start at start
        field[pos[1], pos[0]] = 1
        for i in range(max((self.xRange[1]-self.xRange[0]), (self.yRange[1]-self.yRange[0]))):
            if self.direction == "N":
                # Only in y-dir
                pos[1] += 1
            elif self.direction == "NE":
                pos[0] += 1
                pos[1] += 1
            elif self.direction == "E":
                pos[0] += 1
            elif self.direction == "SE":
                pos[0] += 1
                pos[1] -= 1
            elif self.direction == "S":
                # Only in y-dir
                pos[1] -= 1
            elif self.direction == "SW":
                pos[0] -= 1
                pos[1] -= 1
            elif self.direction == "W":
                pos[0] -= 1
            elif self.direction == "NW":
                pos[0] -= 1
                pos[1] += 1

            field[pos[1], pos[0]] = 1

        return field

smokers = []
maxX = 0
maxY = 0

for l in lines:
    start, end = re.split("\s+->\s+", re.sub("\n","",l))
    start = list(map(int,re.split("\D", start)))
    end = list(map(int,re.split("\D", end)))

    maxX = max(maxX, start[0], end[0])
    maxY = max(maxY, start[1], end[1])
    smoker = SmokerLine(start,end)
    smokers.append(smoker)

print(smokers)
print(len(smokers))
print(maxX)
print(maxY)

field = np.zeros((maxX+1,maxY+1), dtype=int)

for smoker in smokers:
    smoker_field = smoker.drawField((maxX+1,maxY+1))
    field += smoker_field

print(field)

ans = len(np.where(field >= 2)[0])
print("Answer: "+str(ans))
