#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Advent of Code 2015 Day 3 part 2

import re
import pdb
import numpy as np
import copy

i = open("day3_in.txt", "r")

l = i.readlines()

#l = "^v\n" # 3
#l = "^>v<\n" # 3
#l = "^v^v^v^v^v\n" #11

i.close()

l = re.sub("\n","",l[0])

s_loc = [0,0]
rs_loc = [0,0]

places_visited = [
    copy.copy(s_loc),
]

places_visited = [
    copy.copy(rs_loc),
]

for e in l[::2]:
    if (e == '^'):
        s_loc[0] += 1
    elif (e == '>'):
        s_loc[1] += 1
    elif (e == 'v'):
        s_loc[0] -= 1
    elif (e == '<'):
        s_loc[1] -= 1
    else:
        print("problem")

    print(s_loc)

    if not s_loc in places_visited:
        places_visited.append(copy.copy(s_loc))

for e in l[1::2]:
    if (e == '^'):
        rs_loc[0] += 1
    elif (e == '>'):
        rs_loc[1] += 1
    elif (e == 'v'):
        rs_loc[0] -= 1
    elif (e == '<'):
        rs_loc[1] -= 1
    else:
        print("problem")

    print(rs_loc)

    if not rs_loc in places_visited:
        places_visited.append(copy.copy(rs_loc))


print(len(places_visited))
