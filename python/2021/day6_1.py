#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Advent of Code 2021 Day 6 part 1 and 2

import re
import numpy as np
import copy

i = open("day6_in.txt", "r")
lines = i.readlines()
i.close()

# Test input -> Should yield 5934 after 80 days

"""
lines = [
    "3,4,3,1,2\n",
]
"""

fish = np.zeros(9,int)

for l in lines:
    initial = re.split("\D", re.sub("\n","",l))
    initial = list(map(int,initial))
    initial = np.array(initial)
    print("Input vector: "+str(initial))
    for i in range(9):
        fish[i] = np.count_nonzero(initial == i)
    print("Fish: "+str(fish))

for i1 in range(256):
    # 80 rounds for part 1
    # 256 rounds for part 2
    fish_temp = copy.deepcopy(fish)
    fish[0:8] = fish_temp[1:9]
    fish[6] += fish_temp[0]
    fish[8] = fish_temp[0]
    print("Round: "+str(i1+1)+", Fish: "+str(fish))

print("Answer: "+str(sum(fish)))
