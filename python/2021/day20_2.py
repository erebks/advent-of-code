#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Advent of Code 2021 Day 20 part 2
import re
import pdb
import numpy as np
import copy

i = open("day20_in.txt", "r")
lines = i.readlines()
i.close()

"""
# Testinput -> after 50 enhancements -> 3351 pixels
lines = [
    "..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#\n",
    "\n",
    "#..#.\n",
    "#....\n",
    "##..#\n",
    "..#..\n",
    "..###\n",
]
"""

enhancementKey = []

for entry in lines[0]:
    if entry == '\n':
        continue
    elif entry == '.':
        enhancementKey.append(0)
    elif entry == '#':
        enhancementKey.append(1)

enhancementKey = np.array(enhancementKey)

imgI = []
for l in lines[2:]:
    l = re.sub("\n","",l)
    row = []
    for entry in l:
        if entry == '#':
            row.append(1)
        else:
            row.append(0)
    imgI.append(row)

def extendImage(img, fillValue):
    if (fillValue == 0):
        i = np.insert(img, 0, np.zeros(len(img)), axis=1)
        i = np.insert(i, len(i[0]), np.zeros(len(i)), axis=1)
        i = np.insert(i, 0, np.zeros(len(i[0])), axis=0)
        i = np.insert(i, len(i), np.zeros(len(i[0])), axis=0)
    else:
        i = np.insert(img, 0, np.ones(len(img)), axis=1)
        i = np.insert(i, len(i[0]), np.ones(len(i)), axis=1)
        i = np.insert(i, 0, np.ones(len(i[0])), axis=0)
        i = np.insert(i, len(i), np.ones(len(i[0])), axis=0)

    return i

def reduceImage(img):
    i = np.delete(img, 0, axis=1)
    i = np.delete(i, len(i[0])-1, axis=1)
    i = np.delete(i, 0, axis=0) #axis = 0 -> row
    i = np.delete(i, len(i)-1, axis=0)
    return i

def prettyPrintImg(img):
    s = ""
    for row in img:
        for e in row:
            if e == 0:
                s += '.'
            else:
                s += '#'
        s += '\n'
    return s

print(enhancementKey)
print(prettyPrintImg(imgI))

imgI = extendImage(imgI, 0)
imgI = extendImage(imgI, 0)
imgI = extendImage(imgI, 0)
imgI = extendImage(imgI, 0)

def calcEnhancementKeyAtPixel(img, pos):
    if (pos[0] == 0):
        raise ValueError("pos[0] can't be 0")
    if (pos[0] == len(img)-2):
        raise ValueError("pos[0] is higher than img")
    if (pos[1] == 0):
        raise ValueError("pos[1] can't be 0")
    if (pos[1] == len(img[0])-2):
        raise ValueError("pos[1] is higher than img")
    clip = [
        img[pos[0]-1, pos[1]-1],
        img[pos[0]-1, pos[1]],
        img[pos[0]-1, pos[1]+1],
        img[pos[0], pos[1]-1],
        img[pos[0], pos[1]],
        img[pos[0], pos[1]+1],
        img[pos[0]+1, pos[1]-1],
        img[pos[0]+1, pos[1]],
        img[pos[0]+1, pos[1]+1],
        ]

    # convert binary to dec
    result = 0
    for digits in clip:
        result = (result << 1) | digits

    return result

def enhanceImg(img):
    imgO = np.zeros((len(img)-1, len(img[0])-1), int)
    for row in range(1, len(img)-2):
        for col in range(1, len(img[0])-2):
            key = calcEnhancementKeyAtPixel(img, (row, col))
            imgO[row,col] = enhancementKey[key]

    # Delete unused edge
    imgO = reduceImage(imgO)

    # Determine value at edge and extend 4 times
    fillValue = imgO[0,0]
    imgO = extendImage(imgO, fillValue)
    imgO = extendImage(imgO, fillValue)
    imgO = extendImage(imgO, fillValue)
    imgO = extendImage(imgO, fillValue)

    return imgO

img = copy.deepcopy(imgI)
for i in range(50):
    img = enhanceImg(img)
    print(prettyPrintImg(img))


# Count num of pixels
print("Answer: {0}".format(np.count_nonzero(img)))

# 5769 too high
# 5694 too high
