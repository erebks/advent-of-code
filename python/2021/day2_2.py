#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Advent of Code 2021 Day 2 part 2

i = open("day2_in.txt", "r")
lines = i.readlines()
i.close()
o = []

"""
# Test input -> Should yield (15,60)
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
        self.x = 0                # Left/Right -> Untouched
        self.y = 0                # Horizontal Position (Forward)
        self.z = 0                # Vertical Position, needs to be negative!
        self.aim = {"x":0, "z":0} # Aim of the submarine

    def __str__(self):
        return "["+str(self.x)+","+str(self.y)+","+str(self.z)+"]"

    def __repr__(self):
        return "["+str(self.x)+","+str(self.y)+","+str(self.z)+"]"

    def adjAimX(self, value):
        self.aim["x"] += value
        print("Adjusting x-Aim: "+str(value)+" Pos: ["+str(self.x)+","+str(self.y)+","+str(self.z)+"] Aim: ["+str(self.aim["x"])+","+str(self.aim["z"])+"]")

    def adjAimZ(self, value):
        self.aim["z"] += value
        print("Adjusting z-Aim: "+str(value)+" Pos: ["+str(self.x)+","+str(self.y)+","+str(self.z)+"] Aim: ["+str(self.aim["x"])+","+str(self.aim["z"])+"]")

    def moveY(self, value):
        self.y += value
        self.z += self.aim["z"]*value
        print("Moving: ["+str(value)+","+str(self.aim["z"]*value)+"] Pos: ["+str(self.x)+","+str(self.y)+","+str(self.z)+"] Aim: ["+str(self.aim["x"])+","+str(self.aim["z"])+"]")

yellow = Submarine()

for l in lines:
    a, dummy, remain = l.partition(" ")
    if (a == "forward"):
        yellow.moveY(int(remain))
    elif (a == "down"):
        yellow.adjAimZ(-int(remain))
    elif (a == "up"):
        yellow.adjAimZ(int(remain))

print(yellow)
print("Answer: "+str(yellow.y * yellow.z))
