#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Advent of Code 2021 Day 14 part 1

import re
import pdb
import numpy as np

i = open("day14_in.txt", "r")
lines = i.readlines()
i.close()

"""
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
"""

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
    recipe = {'in': [], 'out': None}
    recipe_in, recipe['out'] = re.split(" -> ", s)
    for element in recipe_in:
        recipe['in'].append(element)
    recipies.append(recipe)

print(recipies)

def polymerize(polymer, recipies):
    polymere_new = []
    for i in range(len(polymer)-1):
        # Get element pair
        pair = [polymer[i], polymer[i+1]]
        newElement = None
        # Search for element pair in recipies
        for recipe in recipies:
            recipe_pair = recipe['in']
            if recipe_pair == pair:
                print("Recipe found %s -> %s"%(recipe['in'], recipe['out']))
                newElement = recipe['out']
                break
        if newElement == None:
            raise ValueError("newElement nout found")

        polymere_new.append(polymer[i])
        polymere_new.append(newElement)

    polymere_new.append(polymer[-1])
    return polymere_new

for i in range(10):
    polymer = polymerize(polymer, recipies)
    print(polymer)

print("Length: %d"%len(polymer))

# Convert to numpy array for easy counting
polymer = np.array(polymer)

polymer_int = np.zeros(len(polymer), int)

# Convert all capital letters to numers
for i in range(65,91):
    polymer_int[polymer==chr(i)] = int(i)

a = np.bincount(polymer_int)

maxValue = 0
minValue = a[a.argmax()] # Initialize with biggest value

for value in np.bincount(polymer_int):
    if value == 0:
        continue
    maxValue = max(maxValue, value)
    minValue = min(minValue, value)

print("Min: %d, Max: %d, Diff: %d"%(minValue, maxValue, maxValue-minValue))
