#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Advent of Code 2019 day 2

import re
import intcomp
import copy

computer = intcomp.Intcomputer(intcomp.INSTSET)

i = open("day2_in.txt", "r")
lines = i.readlines()
i.close()

code = re.sub("\n","", lines[0]) # Get rid of newline
code_inital = list(map(int, re.split("\D", code)))

# TEST DESCRIPTION
code = copy.deepcopy(code_inital)
code[1] = 12
code[2] = 2

computer.loadMem(code)

while computer.step() is not None:
    continue

print("Answer part 1: "+str(code[0]))

# Now find which verb and noun produce 19690720

for noun in range(99):
    for verb in range(99):
        code = copy.deepcopy(code_inital)
        code[1] = noun
        code[2] = verb
        computer.loadMem(code)
        while computer.step() is not None:
            continue
        if code[0] == 19690720:
            print("Answer part 2: "+str(100*noun+verb))
            exit(0)
