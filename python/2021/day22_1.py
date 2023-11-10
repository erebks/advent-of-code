#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Advent of Code 2021 Day 22 part 1
import re
import pdb
import numpy as np
import copy

i = open("day22_in.txt", "r")
lines = i.readlines()
i.close()

# Testinput 1
lines = [
    "on x=10..12,y=10..12,z=10..12\n", # 27 cubes
    "on x=11..13,y=11..13,z=11..13\n", # 27 + 19 cubes
    "off x=9..11,y=9..11,z=9..11\n",   # -8
    "on x=10..10,y=10..10,z=10..10\n", # +1 = 39
]

"""
# Testinput 2 -> 590784 cubes on
lines = [
    "on x=-20..26,y=-36..17,z=-47..7\n",
    "on x=-20..33,y=-21..23,z=-26..28\n",
    "on x=-22..28,y=-29..23,z=-38..16\n",
    "on x=-46..7,y=-6..46,z=-50..-1\n",
    "on x=-49..1,y=-3..46,z=-24..28\n",
    "on x=2..47,y=-22..22,z=-23..27\n",
    "on x=-27..23,y=-28..26,z=-21..29\n",
    "on x=-39..5,y=-6..47,z=-3..44\n",
    "on x=-30..21,y=-8..43,z=-13..34\n",
    "on x=-22..26,y=-27..20,z=-29..19\n",
    "off x=-48..-32,y=26..41,z=-47..-37\n",
    "on x=-12..35,y=6..50,z=-50..-2\n",
    "off x=-48..-32,y=-32..-16,z=-15..-5\n",
    "on x=-18..26,y=-33..15,z=-7..46\n",
    "off x=-40..-22,y=-38..-28,z=23..41\n",
    "on x=-16..35,y=-41..10,z=-47..6\n",
    "off x=-32..-23,y=11..30,z=-14..3\n",
    "on x=-49..-5,y=-3..45,z=-29..18\n",
    "off x=18..30,y=-20..-8,z=-3..13\n",
    "on x=-41..9,y=-7..43,z=-33..15\n",
    "on x=-54112..-39298,y=-85059..-49293,z=-27449..7877\n", # not within +-50 range
    "on x=967..23432,y=45373..81175,z=27513..53682\n", # not within +-50 range
]
"""

steps = []

for l in lines:
    l = re.sub("\n","",l)

    step = {
        "onoff": None,
        "x": None,
        "y": None,
        "z": None
    }

    step['onoff'], remain = re.split(" ", l)

    remain = re.sub("(x|y|z)=", "", remain)

    x, y, z = re.split(",", remain)
    x = re.split("\.+", x)
    y = re.split("\.+", y)
    z = re.split("\.+", z)

    x = list(map(int,x))
    y = list(map(int,y))
    z = list(map(int,z))

    step['x'] = x
    step['y'] = y
    step['z'] = z

    steps.append(step)

class Cuboid:
    def __init__(self, xRange, yRange, zRange):
        self.xRange = xRange
        self.yRange = yRange
        self.zRange = zRange

        # Get lengths
        xlen = self.xRange[1] - self.xRange[0]
        ylen = self.yRange[1] - self.yRange[0]
        zlen = self.zRange[1] - self.zRange[0]

        self.size = xlen*ylen*zlen
        if self.size == 0:
            raise ValueError("Size: 0")

    def __str__(self):
        return "xRange: {0}, yRange: {1}, zRange: {2}, size: {3}".format(self.xRange, self.yRange, self.zRange, self.size)

    def __repr__(self):
        return self.__str__()

    def pointWithin(self, point):
        if ( (point[0] in range(self.xRange[0], self.xRange[1]+1)) and
             (point[1] in range(self.yRange[0], self.yRange[1]+1)) and
             (point[2] in range(self.zRange[0], self.zRange[1]+1))):
            return True
        return False

    def getCorners(self):
        corners = [
            (self.xRange[0], self.yRange[0], self.zRange[0]),
            (self.xRange[0], self.yRange[0], self.zRange[1]),
            (self.xRange[0], self.yRange[1], self.zRange[0]),
            (self.xRange[0], self.yRange[1], self.zRange[1]),
            (self.xRange[1], self.yRange[0], self.zRange[0]),
            (self.xRange[1], self.yRange[0], self.zRange[1]),
            (self.xRange[1], self.yRange[1], self.zRange[0]),
            (self.xRange[1], self.yRange[1], self.zRange[1])]
        return corners

# Test class
c = Cuboid((0,1), (0,1), (0,1))

assert c.pointWithin((0,0,0)) == True
assert c.pointWithin((0,0,1)) == True
assert c.pointWithin((0,1,0)) == True
assert c.pointWithin((0,1,1)) == True
assert c.pointWithin((1,0,0)) == True
assert c.pointWithin((1,0,1)) == True
assert c.pointWithin((1,1,0)) == True
assert c.pointWithin((1,1,1)) == True

assert c.pointWithin((0,0,2)) == False
assert c.pointWithin((-1,0,0)) == False

assert c.getCorners() == [(0,0,0),
                          (0,0,1),
                          (0,1,0),
                          (0,1,1),
                          (1,0,0),
                          (1,0,1),
                          (1,1,0),
                          (1,1,1)]

assert c.size == 1

c = Cuboid((0,10), (0,10), (0,10))

assert c.pointWithin((0,0,0)) == True
assert c.pointWithin((0,0,1)) == True
assert c.pointWithin((0,1,0)) == True
assert c.pointWithin((0,1,1)) == True
assert c.pointWithin((1,0,0)) == True
assert c.pointWithin((1,0,1)) == True
assert c.pointWithin((1,1,0)) == True
assert c.pointWithin((1,1,1)) == True
assert c.pointWithin((10,10,10)) == True
assert c.pointWithin((0,0,2)) == True

assert c.pointWithin((-1,0,0)) == False
assert c.pointWithin((-1,11,0)) == False

assert c.size == 1000

class Field:
    def __init__(self):
        self.cuboids = [] # List of instances

    def _cuboid_overlaps(self, c1, c2):
        for corner in c2.getCorners():
            if c1.pointWithin(corner):
                return True
        return False

    def _reduce_cuboids(self, c1, c2):
        numOfCornersWithin = 0
        if c1.size > c2.size:
            cSmall = c2
            cBig = c1
        else c1.size <= c2.size:
            cSmall = c1
            cBig = c2

        for corner in cSmall.getCorners():
            if Big.pointWithin(corner):
                numOfCornersWithin += 1

        if not numOfCornersWithin in [0,1,2,4,8]:
            raise ValueError("numOfCornersWithin: {0}".format(numOfCornersWithin))

        print("numOfCornersWithin: {0}".format(numOfCornersWithin))
        # If 8 corners <=> only bigger
        if numOfCornersWithin == 8:
            return [cBig]
        # If 4 corners <=> can combine
        elif numOfCornersWithin == 4:
            # Get new cuboid with bigger size
            cNew = Cuboid(
                (min(cSmall.xRange[0], cBig.xRange[0]), max(cSmall.xRange[1], cBig.xRange[1])),
                (min(cSmall.yRange[0], cBig.yRange[0]), max(cSmall.yRange[1], cBig.yRange[1])),
                (min(cSmall.zRange[0], cBig.zRange[0]), max(cSmall.zRange[1], cBig.zRange[1])),
            )
            return [cNew]
        elif (numOfCornersWithin == 1 or numOfCornersWithin == 2):
            # Could bei either at edges => Do nothing
            # Or
            # Check if all corners are within
            return [c1, c2]
        else:
            print("Unhandled!")
            return []

    def addCuboid(self, cuboid):
        if len(self.cuboids) == 0:
            self.cuboids.append(copy.deepcopy(cuboid))

        else:
            for c in self.cuboids:
                if self._cuboid_overlaps(c, cuboid):
                    self.cuboids.remove(c)
                    for reducedCuboid in self._reduce_cuboids(c, cuboid):
                        self.cuboids.append(copy.deepcopy(reducedCuboid))
                    break
            else:
                self.cuboids.append(copy.deepcopy(cuboid))

        return

    def getSizes(self):
        sizes = 0
        for c in self.cuboids:
            sizes += c.size
        return sizes

f = Field()
c1 = Cuboid((0,1), (0,1), (0,1))

f.addCuboid(c1)

assert len(f.cuboids) == 1
assert f.cuboids[0].size == 1
assert f.getSizes() == 1


f = Field()
c1 = Cuboid((0,1), (0,1), (0,1))
c2 = Cuboid((0,1), (0,1), (0,1))

f.addCuboid(c1)
f.addCuboid(c2)

assert len(f.cuboids) == 1
assert f.cuboids[0].size == 1
assert f.getSizes() == 1


f = Field()
c1 = Cuboid((0,1), (0,1), (0,1))
c2 = Cuboid((2,3), (2,3), (2,3))

f.addCuboid(c1)
f.addCuboid(c2)

assert len(f.cuboids) == 2
assert f.cuboids[0].size == 1
assert f.cuboids[1].size == 1
assert f.getSizes() == 2


f = Field()
c1 = Cuboid((0,1), (0,1), (0,1))
c2 = Cuboid((1,2), (0,1), (0,1))

f.addCuboid(c1)
f.addCuboid(c2)

assert len(f.cuboids) == 1
assert f.cuboids[0].size == 2
assert f.getSizes() == 2


# 1 corner overlaps
f = Field()
c1 = Cuboid((0,1), (0,1), (0,1))
c2 = Cuboid((1,2), (1,2), (1,2))

f.addCuboid(c1)
f.addCuboid(c2)

assert len(f.cuboids) == 2
assert f.cuboids[0].size == 1
assert f.cuboids[1].size == 1
assert f.getSizes() == 2


# 2 corners overlap
f = Field()
c1 = Cuboid((0,1), (0,1), (0,1))
c2 = Cuboid((0,1), (1,2), (1,2))

f.addCuboid(c1)
f.addCuboid(c2)

assert len(f.cuboids) == 2
assert f.cuboids[0].size == 1
assert f.cuboids[1].size == 1
assert f.getSizes() == 2


# Overlaps a little
f = Field()
c1 = Cuboid((0,2), (0,2), (0,1))
c2 = Cuboid((1,3), (1,3), (0,1))

f.addCuboid(c1)
f.addCuboid(c2)

assert len(f.cuboids) == 4
assert f.getSizes() == 7


# Completely within
f = Field()
c1 = Cuboid((0,2), (0,2), (0,1))
c2 = Cuboid((1,2), (1,2), (0,1))

f.addCuboid(c1)
f.addCuboid(c2)

assert len(f.cuboids) == 1
assert f.getSizes() == 4

print("WONT WORK!")
