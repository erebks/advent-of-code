#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Advent of Code 2015 Day 5 part 1

import re
import pdb
import numpy as np
import copy

i = open("day5_in.txt", "r")
lines = i.readlines()
i.close()

# Testinput -> BLA BLA erwartung
#lines = [
#    "ugknbfddgicrmopn\n", # -> nice
#    "aaa\n",              # -> nice
#    "jchzalrnumimnmhp\n", # -> naughty
#    "haegwjzuvuyypxyu\n", # -> naughty
#    "dvszwmarrgswjxmb\n", # -> naughty
#]

nice_cnt = 0

for l in lines:
    l = re.sub("\n","",l)

    # Rule 3 -> check if 'ab', 'cd', 'pq', or 'xy' are in the string
    if (re.search("(ab)|(cd)|(pq)|(xy)", l) != None):
        print("{0} contains 'ab', 'cd', 'pq', or 'xy'".format(l))
        continue

    # Rule 1 -> at least 3 vowels (aeiou)
    if (len(re.findall("(a|e|i|o|u)", l)) < 3):
        print("{0} does not contain at least 3 vowels".format(l))
        continue

    # Rule 2 -> at least one letter appearing twice
    if (re.search(r"([a-z])\1", l) == None):
        print("{0} does not contain at least one letter twice in a row".format(l))
        continue

    print("{0} is nice".format(l))
    nice_cnt += 1

print("Nice counter: {0}".format(nice_cnt))
