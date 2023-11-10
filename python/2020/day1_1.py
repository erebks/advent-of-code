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

for entry in a:
    x = np.where(a == 2020-entry)
    if (x[0].size > 0):
        print("For entry: "+str(entry)+" counter (idx): "+str(x[0])+" counter: "+str(a[x[0]]))
        break

print(a[x[0]]*entry)
