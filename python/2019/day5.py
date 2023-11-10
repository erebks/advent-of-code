#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Advent of Code 2019 day 5

import re
import intcomp
import copy

computer = intcomp.Intcomputer(intcomp.INSTSET)

i = open("day5_in.txt", "r")
lines = i.readlines()
i.close()

code = re.sub("\n","", lines[0]) # Get rid of newline
code_initial = list(map(int, re.split(",", code)))
code = copy.deepcopy(code_initial)

computer.loadMem(code)

# Provide 1 for part 1
while computer.step() is not None:
    continue

code = copy.deepcopy(code_initial)
computer.loadMem(code)

# Provide 5 for part 2
while computer.step() is not None:
    continue
