#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Advent of Code 2021 Day 14 part 2

import re
import pdb
import numpy as np
import copy

i = open("day14_in.txt", "r")
lines = i.readlines()
i.close()

# Testinput
lines = [
    "NNCB\n",
    "\n",
    "CH -> B\n",
    "HH -> N\n",
    "CB -> H\n",
    "NH -> C\n",
    "HB -> C\n",
    "HC -> B\n",
    "HN -> C\n",
    "NN -> C\n",
    "BH -> H\n",
    "NC -> B\n",
    "NB -> B\n",
    "BN -> B\n",
    "BB -> N\n",
    "BC -> B\n",
    "CC -> N\n",
    "CN -> C\n",
]

polymer = []

for element in lines[0]:
    if element == '\n':
        break
    else:
        polymer.append(element)

print("Polymere: %s"% polymer)

recipies = []

for l in lines[2:]:
    s = re.sub('\n',"",l)
    recipe = {'in': [], 'out': None, 'count': 0}
    recipe_in, recipe['out'] = re.split(" -> ", s)
    for element in recipe_in:
        recipe['in'].append(element)
    recipies.append(recipe)

for e in recipies:
    if e['in'] == ['N','N']:
        e['count'] += 1
    elif e['in'] == ['N', 'C']:
        e['count'] += 1
    elif e['in'] == ['C', 'B']:
        e['count'] += 1

print(recipies)

def polimerize(recipies):
    recipiesO = copy.deepcopy(recipies)

    for r in recipies:
        if r['count'] == 0:
            continue
        else:
            a, b = r['in']
            res = next((sub for sub in recipiesO if sub['in'] == [a, r['out']]), None)
            res['count'] += r['count']
            res = next((sub for sub in recipiesO if sub['in'] == [r['out'], b]), None)
            res['count'] += r['count']

            # Da hats iwas!
    return recipiesO

def getElements(recipies, first):
    elements = np.zeros(26, int)
    elements[ord(first)-65] = 1
    for r in recipies:
        elements[ord(r['in'][1])-65] += r['count']
    return elements

for i in range(10):
    recipies = polimerize(recipies)

print(recipies)
print(getElements(recipies, 'N'))

a = getElements(recipies, 'N')

maxValue = 0
minValue = a[a.argmax()] # Initialize with biggest value

for value in getElements(recipies, 'N'):
    if value == 0:
        continue
    maxValue = max(maxValue, value)
    minValue = min(minValue, value)

print("Min: %d, Max: %d, Diff: %d"%(minValue, maxValue, maxValue-minValue))
