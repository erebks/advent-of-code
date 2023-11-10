#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Advent of Code 2021 Day 2 part 2

import re
import pdb
import numpy as np
import copy

i = open("day2_in.txt", "r")
lines = i.readlines()
i.close()

# Testinput -> BLA BLA erwartung
#lines = [
#    "2x3x4\n",
#    "1x1x10\n",
#]

packets = []

for l in lines:
    l = re.sub("\n","",l)
    a, b, c = np.sort(np.array([int(i) for i in re.split("x",l)]))
    ribbon = 2*a + 2*b + a*b*c
    packets.append(ribbon)

print(packets)

print(sum(packets))
