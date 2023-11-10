#!/usr/bin/env python3
# -*- coding: utf-8 -*-

i = open("day3_in.txt", "r")
lines = i.readlines()
i.close()

# Test input
"""
lines = [
    "..##.......",
    "#...#...#..",
    ".#....#..#.",
    "..#.#...#.#",
    ".#...##..#.",
    "..#.##.....",
    ".#.#.#....#",
    ".#........#",
    "#.##...#...",
    "#...##....#",
    ".#..#...#.#"
    ]
"""

piste = []

for line in lines:
    l = line.partition("\n")[0]
    piste.append(list(l))

# right 3, down 1
# Should yield 7
trees = 0
pos = {'x':0, 'y':0}
delta_x = 3
delta_y = 1

def slideHitsTree(p, delta_x, delta_y, pos):
    pos['x'] = pos['x'] + delta_x
    pos['y'] = pos['y'] + delta_y
    if (p[pos['y']][pos['x'] % len(p[pos['y']])] == '#'):
        highlight = p[pos['y']]
        highlight[pos['x'] % len(p[pos['y']])] = 'X'
        print("".join(highlight)+" -> Tree hit at ("+str(pos['x'])+","+str(pos['y'])+")")
        return True, pos
    else:
        highlight = p[pos['y']]
        highlight[pos['x'] % len(p[pos['y']])] = 'O'
        print("".join(highlight)+" -> No tree at ("+str(pos['x'])+","+str(pos['y'])+")")
        return False, pos

for i in range(len(piste)-1):
    ret = slideHitsTree(piste, delta_x, delta_y, pos)
    if ret[0]:
        trees = trees + 1
    pos = ret[1]

print(trees)
