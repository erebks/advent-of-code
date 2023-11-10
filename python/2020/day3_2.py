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

def slideHitsTree(p, delta_x, delta_y, pos):
    pos['x'] = pos['x'] + delta_x
    pos['y'] = pos['y'] + delta_y
    if pos['y'] > len(p):
        print("EOPiste")
        return False, pos
    if (p[pos['y']][pos['x'] % len(p[pos['y']])] == '#'):
        highlight = p[pos['y']].copy()
        highlight[pos['x'] % len(p[pos['y']])] = 'X'
        print("".join(highlight)+" -> Tree hit at ("+str(pos['x'])+","+str(pos['y'])+")")
        return True, pos
    else:
        highlight = p[pos['y']].copy()
        highlight[pos['x'] % len(p[pos['y']])] = 'O'
        print("".join(highlight)+" -> No tree at ("+str(pos['x'])+","+str(pos['y'])+")")
        return False, pos

a = 1
t = 0
pos = {'x':0, 'y':0}

for i in range(len(piste)-1):
    ret = slideHitsTree(piste, 1, 1, pos)
    if ret[0]:
        t = t + 1
    pos = ret[1]
print("Right 1, down 1 -> "+str(t))
a *= t
t = 0
pos = {'x':0, 'y':0}

for i in range(len(piste)-1):
    ret = slideHitsTree(piste, 3, 1, pos)
    if ret[0]:
        t = t + 1
    pos = ret[1]
print("Right 3, down 1 -> "+str(t))
a *= t
t = 0
pos = {'x':0, 'y':0}

for i in range(len(piste)-1):
    ret = slideHitsTree(piste, 5, 1, pos)
    if ret[0]:
        t = t + 1
    pos = ret[1]
print("Right 5, down 1 -> "+str(t))
a *= t
t = 0
pos = {'x':0, 'y':0}

for i in range(len(piste)-1):
    ret = slideHitsTree(piste, 7, 1, pos)
    if ret[0]:
        t = t + 1
    pos = ret[1]
print("Right 7, down 1 -> "+str(t))
a *= t
t = 0
pos = {'x':0, 'y':0}

for i in range(int(len(piste)/2)):
    ret = slideHitsTree(piste, 1, 2, pos)
    if ret[0]:
        t = t + 1
    pos = ret[1]
print("Right 1, down 2 -> "+str(t))
a *= t

print(a)
