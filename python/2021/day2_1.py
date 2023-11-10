#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Advent of Code 2021 Day 2 part 1

i = open("day2_in.txt", "r")
lines = i.readlines()
i.close()
o = []

"""
# Test input -> Should yield (15,10)
lines = [
    "forward 5\n",
    "down 5\n",
    "forward 8\n",
    "up 3\n",
    "down 8\n",
    "forward 2\n",
    ]
"""

class Submarine:
    def __init__(self):
        self.x = 0 # Left/Right
        self.y = 0 # Forward
        self.z = 0 # Up/Down, Depth, needs to be negative!

    def __str__(self):
        return "["+str(self.x)+","+str(self.y)+","+str(self.z)+"]"

    def __repr__(self):
        return "["+str(self.x)+","+str(self.y)+","+str(self.z)+"]"

    def moveX(self, value):
        self.x += value
        print("MovingX: "+str(value)+" @["+str(self.x)+","+str(self.y)+","+str(self.z)+"]")

    def moveY(self, value):
        self.y += value
        print("MovingY: "+str(value)+" @["+str(self.x)+","+str(self.y)+","+str(self.z)+"]")

    def moveZ(self, value):
        self.z += value
        print("MovingZ: "+str(value)+" @["+str(self.x)+","+str(self.y)+","+str(self.z)+"]")

yellow = Submarine()

for l in lines:
    a, dummy, remain = l.partition(" ")
    if (a == "forward"):
        yellow.moveY(int(remain))
    elif (a == "down"):
        yellow.moveZ(-int(remain))
    elif (a == "up"):
        yellow.moveZ(int(remain))

print(yellow)
print("Answer: "+str(yellow.y * yellow.z))
