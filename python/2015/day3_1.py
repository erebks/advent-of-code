#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Advent of Code 2015 Day 3 part 1

import re
import pdb
import numpy as np
import copy

i = open("day3_in.txt", "r")

l = i.readlines()

#l = ">\n"
#l = "^>v<\n"
#l = "^v^v^v^v^v\n"

i.close()

l = re.sub("\n","",l[0])

loc = [0,0]

places_visited = [
    copy.copy(loc),
]

for e in l:
    if (e == '^'):
        loc[0] += 1
    elif (e == '>'):
        loc[1] += 1
    elif (e == 'v'):
        loc[0] -= 1
    elif (e == '<'):
        loc[1] -= 1
    else:
        print("problem")

    print(loc)

    if not loc in places_visited:
        places_visited.append(copy.copy(loc))

print(len(places_visited))
