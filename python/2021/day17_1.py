#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Advent of Code 2021 Day 17 part 1

import re
import numpy as np
import copy
import pdb
import math

# Testinput
lines = [
    "target area: x=20..30, y=-10..-5\n",
]


# Real input
lines = [
    "target area: x=244..303, y=-91..-54\n",
]


l = re.sub("target area: ","",re.sub("\n","",lines[0]))
x, y = re.split(",\s", l)

x = re.sub("(x|y)=","",x)
x = re.split("\.\.", x)
x = list(map(int,x))

y = re.sub("(x|y)=","",y)
y = re.split("\.\.", y)
y = list(map(int,y))

trench = [x,y]

print("Trench: {0}".format(trench))

# ^ y
# |
# -> x
#
# .....
# ...TT
# ...TT

# Pos after t = 0 -> (0 ,0)
# Pos after t = 1 -> (7 ,2)
# Pos after t = 2 -> (13,3)
# Pos after t = 3 -> (18,3)

def calcPosAtTime(t, initV):
    posY = initV[1]*t - 0.5 * t**2 + 0.5*t

    if (t < initV[0]):
        posX = initV[0]*t - 0.5 * t**2 + 0.5*t
    else:
        t = initV[0]
        posX = initV[0]*t - 0.5 * t**2 + 0.5*t
    return (posX, posY)

def calcTimeAtPos(pos, initV):
    # Invert formulas and find t
    posX = pos[0]
    posY = pos[1]

    # X sqrt
    a = ((initV[0]+0.5)**2-2*posX)
    if (a < 0):
        return None
    else:
        t_x = [-((-initV[0]+0.5)+math.sqrt(a)), -((-initV[0]+0.5)-math.sqrt(a))]

    t_x_real = []
    # Check if velX already at 0
    for t in t_x:
        if (initV[0]-t > 1):
            t_x_real.append(t)

    # Y sqrt
    a = ((initV[1]+0.5)**2-2*posY)
    if (a < 0):
        return None
    else:
        t_y = [-((-initV[1]+0.5)+math.sqrt(a)), -((-initV[1]+0.5)-math.sqrt(a))]

    if (t_x_real == []):
        for t in t_y:
            if t >= -1:
                return t+1
    else:
        for t in t_x_real:
            if t >= -1:
                if t == t_y[0]:
                    return t+1
                elif t == t_y[1]:
                    return t+1

    return None

def findMaxXVelThatHitsTrench(trench):
    # Get right trench border
    trenchRight = trench[0][1]

    a = 0.25+2*trenchRight
    if a < 0:
        return None

    velX = [-0.5 + math.sqrt(a), -0.5 - math.sqrt(a)]

    for v in velX:
        if v >= 0:
            return v

    return None

def findMinXVelThatHitsTrench(trench):
    # Get right trench border
    trenchLeft = trench[0][0]

    a = 0.25+2*trenchLeft
    if a < 0:
        return None

    velX = [-0.5 + math.sqrt(a), -0.5 - math.sqrt(a)]

    for v in velX:
        if v >= 0:
            return v

    return None

def findHighestYPos(vel):
    # Also the 1st deritive would work here...
    # Increase t until y gets smaller again
    t = 0
    pos = calcPosAtTime(t, vel)
    while True:
        t += 1
        posN = calcPosAtTime(t, vel)
        if (posN[1] < pos[1]):
            return pos[1]
        pos = posN


def probeHitsTrench(initV, trench):
    # Check top x line and check if probe hits
    # If yes check floor and roof function and see if in there

    for x in range(trench[0][0], trench[0][1]+1):
        t = calcTimeAtPos( (x, trench[1][0]), initV) # Use upper trenchborder
        if None != t:
#            print("Hit @{0} -> {1}".format((x, trench[1][1]), t))
            t_floor = math.floor(t)
            t_ceil = math.ceil(t)
            floorPos = calcPosAtTime(t_floor, initV)
            ceilPos = calcPosAtTime(t_ceil, initV)

            if (floorPos[0] >= trench[0][0] and
                floorPos[0] <= trench[0][1] and
                floorPos[1] >= trench[1][0] and
                floorPos[1] <= trench[1][1]):
                return True
            elif (ceilPos[0] >= trench[0][0] and
                ceilPos[0] <= trench[0][1] and
                ceilPos[1] >= trench[1][0] and
                ceilPos[1] <= trench[1][1]):
                return True
        else:
            continue
#            print("No hit  @{0}".format((x, trench[1][1])))

    return False

def printTrajectory(pos, trench):
    # Take highest X value (pos or trench)
    maxX = max(abs(trench[0][0]), abs(trench[0][1]))
    maxY = max(abs(trench[1][0]), abs(trench[1][1]))

    for p in pos:
        maxX = max(maxX, abs(p[0]))
        maxY = max(maxY, abs(p[1]))

    field = np.zeros([maxY+1, maxX+1], 'U1')
    field.fill('.')

    # draw trench
    for y in range(trench[1][0], trench[1][1]+1):
        for x in range(trench[0][0], trench[0][1]+1):
            field[y,x] = 'T'

    # draw pos
    for p in pos:
        field[p[1],p[0]] = '#'

    s = ""
    for line in field:
        for p in line:
            s += p
        s += '\n'

    return s

maxXvel = findMaxXVelThatHitsTrench(trench)
minXvel = findMinXVelThatHitsTrench(trench)

print("maxXvel is: {0}".format(findMaxXVelThatHitsTrench(trench)))
print("minXvel is: {0}".format(findMinXVelThatHitsTrench(trench)))

print("HighstYPos of (6,9): {0}".format(findHighestYPos((6,9))))

highestYPos = {"v": None, "pos": 0}

# Use minXVel and increase y until 100 (for starters...)

for xvel in range(math.floor(minXvel), math.ceil(maxXvel)):
    for yvel in range(0, 100):
        v = (xvel, yvel)
        if probeHitsTrench(v, trench):
            print("({0},{1}) -> HIT".format(xvel, yvel))
            highestYPos["v"] = v
            highestYPos["pos"] = max(highestYPos["pos"], findHighestYPos(v))
        else:
            print("({0},{1}) -> no hit".format(xvel, yvel))

print("Answer: {0}".format(highestYPos))

for t in range(0,20):
    print("{1} @{0}".format(calcPosAtTime(t, highestYPos["v"]), highestYPos["v"]))
