#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Advent of Code 2022
import re
import pdb
import numpy as np
import copy

# Testinput -> BLA BLA erwartung
dry_monkeys = [
    {
        'id': 0,
        'items':[79, 98],
        'fun': lambda a : int((a*19) / 3),
        'fun2': lambda a : (a*19),
        'test': lambda a : 2 if (a % 23 == 0) else 3,
        'inspections': 0,
    },
    {
        'id': 1,
        'items':[54, 65, 75, 74],
        'fun': lambda a : int((a+6)/3),
        'fun2': lambda a : (a+6),
        'test': lambda a : 2 if (a % 19 == 0) else 0,
        'inspections': 0,
    },
    {
        'id': 2,
        'items':[79, 60, 97],
        'fun': lambda a : int((a*a) / 3),
        'fun2': lambda a : (a*a),
        'test': lambda a : 1 if (a % 13 == 0) else 3,
        'inspections': 0,
    },
    {
        'id': 3,
        'items':[74],
        'fun': lambda a : int((a+3)/3),
        'fun2': lambda a : (a+3),
        'test': lambda a : 0 if (a % 17 == 0) else 1,
        'inspections': 0,
    },
]


real_monkeys = [
    {
        'id': 0,
        'items':[56, 56, 92, 65, 71, 61, 79],
        'fun': lambda a : int((a*7) /3),
        'fun2': lambda a : (a*7),
        'test': lambda a : 3 if (a % 3 == 0) else 7,
        'inspections': 0,
    },
    {
        'id': 1,
        'items': [61, 85],
        'fun': lambda a : int((a+5) /3),
        'fun2': lambda a : (a+5),
        'test': lambda a : 6 if (a % 11 == 0) else 4,
        'inspections': 0,
    },
    {
        'id': 2,
        'items': [54, 96, 82, 78, 69],
        'fun': lambda a : int((a*a)/3),
        'fun2': lambda a : (a*a),
        'test': lambda a : 0 if (a % 7 == 0) else 7,
        'inspections': 0,
    },
    {
        'id': 3,
        'items': [57, 59, 65, 95],
        'fun': lambda a : int((a+4)/3),
        'fun2': lambda a : (a+4),
        'test': lambda a : 5 if (a % 2 == 0) else 1,
        'inspections': 0,
    },
    {
        'id': 4,
        'items': [62, 67, 80],
        'fun': lambda a : int((a*17)/3),
        'fun2': lambda a : (a*17),
        'test': lambda a : 2 if (a % 19 == 0) else 6,
        'inspections': 0,
    },
    {
        'id': 5,
        'items': [91],
        'fun': lambda a : int((a+7)/3),
        'fun2': lambda a : (a+7),
        'test': lambda a : 1 if (a % 5 == 0) else 4,
        'inspections': 0,
    },
    {
        'id': 6,
        'items': [79, 83, 64, 52, 77, 56, 63, 92],
        'fun': lambda a : int((a+6)/3),
        'fun2': lambda a : (a+6),
        'test': lambda a : 2 if (a % 17 == 0) else 0,
        'inspections': 0,
    },
    {
        'id': 7,
        'items': [50, 97, 76, 96, 80, 56],
        'fun': lambda a : int((a+3)/3),
        'fun2': lambda a : (a+3),
        'test': lambda a : 3 if (a % 13 == 0) else 5,
        'inspections': 0,
    },
]

def part1(dryRun = False):
    print(f"PART 1, dryRun {dryRun}")
    if dryRun:
        monkeys = copy.deepcopy(dry_monkeys)
    else:
        monkeys = copy.deepcopy(real_monkeys)

    for i in range(20):
        for monkey in monkeys:
            for item in monkey['items']:
                monkey['inspections'] += 1
                newWorry = monkey['fun'](item)
                nmonkey = monkey['test'](newWorry)
                monkeys[nmonkey]['items'].append(newWorry)
            monkey['items'] = []

    m = [{'id': monkey['id'], 'items': monkey['items'], 'inspections': monkey['inspections'] } for monkey in monkeys]
    m = sorted(m, key=lambda a: a['inspections'])

    print(m)
    print(f"Answer: {m[-1]['inspections'] * m[-2]['inspections']}")

def part2(dryRun = False):
    print(f"PART 2, dryRun {dryRun}")
    if dryRun:
        monkeys = copy.deepcopy(dry_monkeys)
        maxWorry = 23*19*13*17
    else:
        monkeys = copy.deepcopy(real_monkeys)
        maxWorry = 3*11*7*2*19*5*17*13

    for i in range(10000):
        for monkey in monkeys:
            for item in monkey['items']:
                monkey['inspections'] += 1
                newWorry = monkey['fun2'](item) % maxWorry
                if newWorry % maxWorry != 0:
                    newWorry = newWorry % maxWorry
                nmonkey = monkey['test'](newWorry)
                monkeys[nmonkey]['items'].append(newWorry)
            monkey['items'] = []

    m = [{'id': monkey['id'], 'items': monkey['items'], 'inspections': monkey['inspections'] } for monkey in monkeys]
    m = sorted(m, key=lambda a: a['inspections'])

    print(m)
    print(f"Answer: {m[-1]['inspections'] * m[-2]['inspections']}")

if __name__=="__main__":
    part1(dryRun = False)
    part2(dryRun = False)
