#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Advent of Code 2021 Day 17 part 2

import re
import numpy as np
import copy
import pdb
import math

"""
# Testinput
lines = [
    "target area: x=20..30, y=-10..-5\n",
]

# all v that hit for testinput
correct_v_str = [
    "23,-10  25,-9   27,-5   29,-6   22,-6   21,-7   9,0     27,-7   24,-5",
    "25,-7   26,-6   25,-5   6,8     11,-2   20,-5   29,-10  6,3     28,-7",
    "8,0     30,-6   29,-8   20,-10  6,7     6,4     6,1     14,-4   21,-6",
    "26,-10  7,-1    7,7     8,-1    21,-9   6,2     20,-7   30,-10  14,-3",
    "20,-8   13,-2   7,3     28,-8   29,-9   15,-3   22,-5   26,-8   25,-8",
    "25,-6   15,-4   9,-2    15,-2   12,-2   28,-9   12,-3   24,-6   23,-7",
    "25,-10  7,8     11,-3   26,-7   7,1     23,-9   6,0     22,-10  27,-6",
    "8,1     22,-8   13,-4   7,6     28,-6   11,-4   12,-4   26,-9   7,4",
    "24,-10  23,-8   30,-8   7,0     9,-1    10,-1   26,-5   22,-9   6,5",
    "7,5     23,-6   28,-10  10,-2   11,-1   20,-9   14,-2   29,-7   13,-3",
    "23,-5   24,-8   27,-9   30,-7   28,-5   21,-10  7,9     6,6     21,-5",
    "27,-10  7,2     30,-9   21,-8   22,-7   24,-9   20,-6   6,9     29,-5",
    "8,-2    27,-8   30,-5   24,-7",
]

correct_v_int = []
for l in correct_v_str:
    parsed_line = re.split("\s+", l)
    for entry in parsed_line:
        correct_v_int.append(tuple(map(int, re.split(",", entry))))
"""

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

def findtThatHitsTrechWithGivenYvel(yVel, trench):
    t = []

    trenchUpper = trench[1][1]
    trenchLower = trench[1][0]

    discriminant = (yVel+0.5)**2 - 2*trenchUpper
    if discriminant < 0:
        return []

    tUpper = max([yVel + 0.5 + math.sqrt(discriminant), yVel + 0.5 - math.sqrt(discriminant)])

    discriminant = (yVel+0.5)**2 - 2*trenchLower
    if discriminant < 0:
        return []

    tLower = max([yVel + 0.5 + math.sqrt(discriminant), yVel + 0.5 - math.sqrt(discriminant)])

    for time in range(math.floor(tUpper)-1, math.ceil(tLower)+1):
        rasterizedPos = yVel * time - 0.5*time**2 + 0.5*time
        if rasterizedPos <= trenchUpper and rasterizedPos >= trenchLower:
            t.append(time)
    return t

def probeHitsTrench(initV, trench):
    # Check top x line and check if probe hits
    # If yes check floor and roof function and see if in there
#    print("{0}".format(initV))
    for x in range(trench[0][0], trench[0][1]+1):
        for y in range(trench[1][0], trench[1][1]+1):
            t = calcTimeAtPos( (x, y), initV) # Use upper trenchborder
#            print("\tt: {0}".format(t))
            if None != t:
#                print("Hit @{0} -> {1}".format((x, trench[1][1]), t))
                t_floor = math.floor(t)
                t_ceil = math.ceil(t)
                floorPos = calcPosAtTime(t_floor, initV)
                ceilPos = calcPosAtTime(t_ceil, initV)
#                print("\t\tt_floor: {0}, t_ceil: {1}, floorPos: {2}, ceilPos: {3}".format(t_floor, t_ceil, floorPos, ceilPos))

                if (floorPos[0] >= trench[0][0] and
                    floorPos[0] <= trench[0][1] and
                    floorPos[1] >= trench[1][0] and
                    floorPos[1] <= trench[1][1]):
#                    print("\t\tfloorHit")
                    return True
                elif (ceilPos[0] >= trench[0][0] and
                      ceilPos[0] <= trench[0][1] and
                      ceilPos[1] >= trench[1][0] and
                      ceilPos[1] <= trench[1][1]):
#                    print("\t\tceilHit")
                    return True

            else:
                continue
#            print("No hit  @{0}".format((x, trench[1][1])))

    return False

def probeHitsTrenchWithGivent(initV, trench, t):
    for time in t:
        pos = calcPosAtTime(time, initV)
        if (pos[0] >= trench[0][0] and
            pos[0] <= trench[0][1] and
            pos[1] >= trench[1][0] and
            pos[1] <= trench[1][1]):
            return True
    return False

def testProbeHitsTrench(correct_v_int, trench):
    for v in correct_v_int:
        assert True == probeHitsTrench(v, trench)

maxXvel = findMaxXVelThatHitsTrench(trench)
minXvel = findMinXVelThatHitsTrench(trench)

print("maxXvel is: {0}".format(findMaxXVelThatHitsTrench(trench)))
print("minXvel is: {0}".format(findMinXVelThatHitsTrench(trench)))

yVels = []
# Step through y and
for yVel in range(-100, 100):
    t = findtThatHitsTrechWithGivenYvel(yVel, trench)
    if t != []:
        yVels.append({"yVel": yVel, "time": t})

print(yVels)

allVel = []

# Now step trough x and find hits
for xVel in range(0,1000):
    for yVel in yVels:
        if(probeHitsTrenchWithGivent((xVel, yVel["yVel"]), trench, yVel["time"])):
            allVel.append((xVel, yVel["yVel"]))

print(allVel)
print("Answer: {0}".format(len(allVel)))
