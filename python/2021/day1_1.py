#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Advent of Code 2021 Day 1 (part 1 and 2)

i = open("day1_in.txt", "r")
lines = i.readlines()
i.close()
o = []

"""
# Test input -> Should yield 7 increases
lines = [
    "199\n",
    "200\n",
    "208\n",
    "210\n",
    "200\n",
    "207\n",
    "240\n",
    "269\n",
    "260\n",
    "263\n",
    ]
"""

for l in lines:
    o.append(int(l))

sums = []

for i in range(len(o)):
    try:
        sums.append(o[i]+o[i+1]+o[i+2])
    except:
        break

inc = 0
dec = 0

for i in range(len(sums)-1):
    if (sums[i+1] > sums[i]):
        print("inc")
        inc += 1
    elif (sums[i+1] < sums[i]):
        print("dec")
        dec += 1
    else:
        print("STAY")

print(sums)
print(inc)
