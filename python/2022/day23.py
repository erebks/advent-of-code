#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Advent of Code 2022
import re
import pdb
import numpy as np
import copy

i = open("day23_in.txt", "r")
i_lines = i.readlines()
i.close()

# Testinput -> BLA BLA erwartung
dry_lines = [
    '....#..\n',
    '..###.#\n',
    '#...#.#\n',
    '.#...##\n',
    '#.###..\n',
    '##.#.##\n',
    '.#..#..\n',
]

dry_lines = [
    '.....\n',
    '..##.\n',
    '..#..\n',
    '.....\n',
    '..##.\n',
    '.....\n',
]

# np:
# +--> x
# | .....
# | ..N..
# v .W#E.
# y ..S..
#   .....
#
# NPA[y,x]

class Elf():
    def __init__(self, pos):
        # pos is array [y,x]
        self.pos = pos
        self.target = None

    def nextStep(self, elfs, iteration):
        p = self.pos

        N = (p[0]-1, p[1])
        NE = (p[0]-1, p[1]+1)
        E = (p[0], p[1]+1)
        SE = (p[0]+1, p[1]+1)
        S = (p[0]+1, p[1])
        SW = (p[0]+1, p[1]-1)
        W = (p[0], p[1]-1)
        NW = (p[0]-1, p[1]-1)

        field = printField(elfs)
        print(f"{field[NW[0]][NW[1]]}{field[N[0]][N[1]]}{field[NE[0]][NE[1]]}")
        print(f"{field[W[0]][W[1]]}{field[p[0]][p[1]]}{field[E[0]][E[1]]}")
        print(f"{field[SW[0]][SW[1]]}{field[S[0]][S[1]]}{field[SE[0]][SE[1]]}")


        # First half:
        # If there is no Elf in the 8 tiles -> STOP!
        # If there is no Elf in the N, NE, or NW adjacent positions, the Elf proposes moving north one step. on iter == 0
        # If there is no Elf in the S, SE, or SW adjacent positions, the Elf proposes moving south one step. on iter == 1
        # If there is no Elf in the W, NW, or SW adjacent positions, the Elf proposes moving west one step. on iter == 2
        # If there is no Elf in the E, NE, or SE adjacent positions, the Elf proposes moving east one step. on iter == 3


        self.target = None
        return self.target

    def step(self, dublicateTargets):
        if self.taget not in dublicateTargets:
            print(f"[Elf @{self.pos}, newPos: {self.target}]")
            self.pos = self.target

        return self.pos

    def getPos(self):
        # Position as useable by np
        return (self.pos[0], self.pos[1])

    def __str__(self):
        return f"[Elf @{self.pos}]"

    def __repr__(self):
        return f"[Elf @{self.pos}]"

def printField(elfs):

    xMax = 0
    yMax = 0
    for e in elfs:
        xMax = max(xMax, e.pos[1])
        yMax = max(yMax, e.pos[0])

    a = ['.']*(xMax+1)
    f = []

    [f.append(copy.deepcopy(a)) for i in range(yMax+1)]

    for e in elfs:
        p = e.getPos()
        f[p[0]][p[1]] = '#'

    for r in f:
        print(''.join(r))

    return f

def part1(dryRun = False):
    print(f"PART 1, dryRun {dryRun}")
    if dryRun:
        lines = dry_lines
    else:
        lines = i_lines

    elfs = []

    for y in range(len(lines)):
        for x in range(len(lines[0])):
            # print(f"@{x,y}")
            if lines[y][x] == '#':
                elf = Elf([y,x])
                elfs.append(elf)

    print(elfs)

    printField(elfs)

    while True:
        targets = []
        dublicateTargets = []

        for e in elfs:
            t = e.nextStep(elfs, 0)
            if t in targets:
                dublicateTargets.append(t)
            else:
                targets.append(t)

        if targets == []:
            print("No more targets")
            break

        for e in elfs:
            e.steps(dublicateTargets)

def part2(dryRun = False):
    print(f"PART 2, dryRun {dryRun}")
    if dryRun:
        lines = dry_lines
    else:
        lines = i_lines

if __name__=="__main__":
    part1(dryRun = True)
    part2(dryRun = True)


"""
First half:
If there is no Elf in the 8 tiles -> STOP!
If there is no Elf in the N, NE, or NW adjacent positions, the Elf proposes moving north one step. on iter == 0
If there is no Elf in the S, SE, or SW adjacent positions, the Elf proposes moving south one step. on iter == 1
If there is no Elf in the W, NW, or SW adjacent positions, the Elf proposes moving west one step. on iter == 2
If there is no Elf in the E, NE, or SE adjacent positions, the Elf proposes moving east one step. on iter == 3

Resize map of one elf would step to 0< or >len()-1 rezize, pay attention to offset X and offset Y
Update all newPos with the offset
Save all new pos in a list, get dublicates -> save in dublicates list

Second half:
If two elfes would go to the same tile -> both stop (for ever elf -> check if new pos is in dublicates list)
Otherwise move


"""
