2#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Advent of Code 2022
import re
import pdb
import numpy as np
import copy

i = open("day9_in.txt", "r")
i_lines = i.readlines()
i.close()

# Testinput -> Tail covers 13 pos
dry_lines = [
    'R 4\n',
    'U 4\n',
    'L 3\n',
    'D 1\n',
    'R 4\n',
    'D 1\n',
    'L 5\n',
    'R 2\n',
]

dry_lines_2 = [
    'R 5\n',
    'U 8\n',
    'L 8\n',
    'D 3\n',
    'R 17\n',
    'D 10\n',
    'L 25\n',
    'U 20\n',
]

class Knot():
    def __init__(self):
        self.posX = 0
        self.posY = 0

        self.posVisited = []

    def isNearPred(self, posPred):
        dX = posPred[0] - self.posX
        dY = posPred[1] - self.posY

        if (dX in [-1, 0, 1] and
            dY in [-1, 0, 1]):
            # print(f"Head @{posPred[0]},{posPred[1]} | Tail @{self.posX},{self.posY} -> Head is near")
            return True

        # print(f"Head @{posPred[0]},{posPred[1]} | Tail @{self.posX},{self.posY} -> Tail needs to move!")
        return False

    def move(self, posPred):
        if self.isNearPred(posPred):
            # print(f"\tNot moved")
            return

        dX = posPred[0] - self.posX
        dY = posPred[1] - self.posY

        if ((dX >= 2 or dX <= -2) or
            (dX >= 1 or dX <= -1) and (dY >= 2 or dY <= -2)):
            if dX > 0:
                self.posX += 1
                # print(f"\tdX: {dX}, dY: {dY} -> posx+1")
            else:
                self.posX -= 1
                # print(f"\tdX: {dX}, dY: {dY} -> posx-1")

        if ((dY >= 2 or dY <= -2) or
            (dY >= 1 or dY <= -1) and (dX >= 2 or dX <= -2)):
            if dY > 0:
                self.posY += 1
                # print(f"\tdX: {dX}, dY: {dY} -> posy+1")
            else:
                self.posY -= 1
                # print(f"\tdX: {dX}, dY: {dY} -> posy-1")

        # print(f"\tHead @{posPred[0]},{posPred[1]} | Tail @{self.posX},{self.posY}")

    def step(self, posPred):
        self.move(posPred)
        self.posVisited.append((self.posX, self.posY))
        return (self.posX, self.posY)

def part1(dryRun = False):
    print(f"PART 1, dryRun {dryRun}")
    if dryRun:
        lines = dry_lines
    else:
        lines = i_lines

    steps = []
    for l in lines:
        for s in range(int(l[2:-1])):
            steps.append(l[0])

    tail = Knot()
    head = [0,0]
    for step in steps:
        if step == 'U':
            head[0] += 1
        elif step == 'D':
            head[0] -= 1
        elif step == 'R':
            head[1] += 1
        elif step == 'L':
            head[1] -= 1

        tail.step(head)

    print(f"Places visited: {len(set(tail.posVisited))}")

def part2(dryRun = False):
    print(f"PART 2, dryRun {dryRun}")
    if dryRun:
        lines = dry_lines_2
    else:
        lines = i_lines

    steps = []
    for l in lines:
        for s in range(int(l[2:-1])):
            steps.append(l[0])

    knots = [Knot(), Knot(), Knot(), Knot(), Knot(), Knot(), Knot(), Knot(), Knot()]

    head = [0,0]
    for step in steps:
        if step == 'U':
            head[0] += 1
        elif step == 'D':
            head[0] -= 1
        elif step == 'R':
            head[1] += 1
        elif step == 'L':
            head[1] -= 1

        pred = head
        for knot in knots:
            knot.step(pred)
            pred = [knot.posX, knot.posY]

    print(f"Places visited: {len(set(knots[-1].posVisited))}")

if __name__=="__main__":
    part1(dryRun = False)
    part2(dryRun = False)
