#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Advent of Code 2015 Day 4 part 1 and 2

import re
import pdb
import numpy as np
import copy
import hashlib

key = "abcdef"  # -> 609043
key = "pqrstuv" # -> 1048970
key = "iwrupvqb"

i = 0

while True:
    i += 1
    seq = key+str(i)
    md5 = hashlib.md5(seq.encode()).hexdigest()

    if (md5[0:5] == '00000' and md5[5] != '0'):
        print("lowest integer is {0} with md5 {1}".format(i, md5))
        break

while True:
    i += 1
    seq = key+str(i)
    md5 = hashlib.md5(seq.encode()).hexdigest()

    if (md5[0:6] == '000000' and md5[6] != '0'):
        print("lowest integer is {0} with md5 {1}".format(i, md5))
        break
