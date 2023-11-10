#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Advent of Code 2021 Day 8 part 1

import re
import numpy as np
import copy

i = open("day8_in.txt", "r")
lines = i.readlines()
i.close()

# Test input -> Should yield 26 instances

"""
lines = [
    "be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe\n",
    "edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc\n",
    "fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg\n",
    "fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb\n",
    "aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea\n",
    "fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb\n",
    "dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe\n",
    "bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef\n",
    "egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb\n",
    "gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce\n",
]
"""

notes = []

for l in lines:
    l = re.sub("\n","",l)
    inp, outp = re.split("\s\|\s",l)
    inp = re.split("\s", inp)
    outp = re.split("\s", outp)
    notes.append([inp, outp])

cnt = 0

for note in notes:
    for digit in note[1]:
        if len(digit) == 2: # 1 needs 2 segments
            cnt += 1
        elif len(digit) == 4: # 4 needs 4 segments
            cnt += 1
        elif len(digit) == 3: # 7 needs 3 segments
            cnt += 1
        elif len(digit) == 7: # 8 needs 7 segments
            cnt += 1

print("Answer: "+str(cnt))
