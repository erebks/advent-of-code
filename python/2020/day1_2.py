#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pdb
import numpy as np

i = open("day1_in.txt", "r")
lines = i.readlines()
i.close()
o = []

for l in lines:
    o.append(int(l))

a = np.sort(o)

b = []

for entry in a:
    if 2020-entry-(a[0]+a[1]) < 0:
        break
    else:
        b.append(entry)

def getIdx(diff, forbidden_idx):
    for i in range(len(b)):
        if (i == forbidden_idx):
            return None
        else:
            diff_i = diff - b[i]
            x = np.where(b==diff_i)
            if (x[0].size>0):
                return i, x[0].item()

for i1 in range(len(b)):
    diff_o = 2020-b[i1]
    ret = getIdx(diff_o, i1)
    if (ret != None):
        print(ret)
        break

print(b[i1]*b[ret[0]]*b[ret[1]])
