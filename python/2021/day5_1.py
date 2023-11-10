#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Advent of Code 2021 Day 5 part 1
# Very slow! (~5 min)

import re
import numpy as np

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
        self.delta = [self.start[0] - self.end[0], self.start[1] - self.end[1]]

    def __str__(self):
        return "["+str(self.start)+"->"+str(self.end)+", xRange: "+str(self.xRange)+", yRange: "+str(self.yRange)+", delta: "+str(self.delta)+"]"
    def __repr__(self):
        return "["+str(self.start)+"->"+str(self.end)+", xRange: "+str(self.xRange)+", yRange: "+str(self.yRange)+", delta: "+str(self.delta)+"]"

    def atPoint(self, point):
        # Return True if smokerline is present at point; otherwise False
        print(str(self)+" atPoint: "+str(point))
        if (((point[0] >= self.xRange[0]) and (point[0] <= self.xRange[1])) and
           ((point[1] >= self.yRange[0]) and (point[1] <= self.yRange[1]))):
            print("\tdelta:"+str(self.delta))
            if (self.delta == [0,0]):
                # What todo?
                print("\tdelta == [0,0]")
                return False
            elif (self.delta[0] == 0 or self.delta[1] == 0):
                print("\tdelta[0 or 1] == 0")
                return True
            else:
                equ = ((point[0]-self.start[0])/(delta[0]) == (point[1]-self.start[1])/(delta[1]))
                print("\tEquation: "+str(equ))
                return equ
        else:
            print("\tOut of Range")
            return False

    def crossesXLine(self, x):
        # Check if Smokerline will be at given x-line
        # Do this by checking xRange
        cross = (x >= self.xRange[0]) and (x <= self.xRange[1])
        print(str(self)+" crossesX: "+str(x)+" -> "+str(cross))
        return cross

    def crossesYLine(self, y):
        # Check if Smokerline will be at given y-line
        cross = (y >= self.yRange[0]) and (y <= self.yRange[1])
        print(str(self)+" crossesY: "+str(y)+" -> "+str(cross))
        return cross

smokers = []
maxX = 0
maxY = 0

for l in lines:
    start, end = re.split("\s+->\s+", re.sub("\n","",l))
    start = list(map(int,re.split("\D", start)))
    end = list(map(int,re.split("\D", end)))

    maxX = max(maxX, start[0], end[0])
    maxY = max(maxY, start[1], end[1])
    # Check if horizontal or vertical -> Puzzle description
    if ((start[0] == end[0]) or (start[1] == end[1])):
        smoker = SmokerLine(start,end)
        smokers.append(smoker)
    else:
        print(str(start)+"->"+str(end)+" Not horizontal or vertical")

print(smokers)
print(len(smokers))
print(maxX)
print(maxY)

field = np.zeros((maxX+1,maxY+1), dtype=int)

for smoker in smokers:
    for y in range(len(field)):
        if (smoker.crossesYLine(y)):
            for x in range(len(field[0])):
                if (smoker.crossesXLine(x)):
                    if (smoker.atPoint([x,y])):
                        field[y,x] += 1

print(field)

ans = len(np.where(field >= 2)[0])
print("Answer: "+str(ans))
