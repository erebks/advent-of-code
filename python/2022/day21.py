#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Advent of Code 2022
import re
import pdb
import numpy as np
import copy

i = open("day21_in.txt", "r")
i_lines = i.readlines()
i.close()

# Testinput -> BLA BLA erwartung
dry_lines = [
    'root: pppw + sjmn\n',
    'dbpl: 5\n',
    'cczh: sllz + lgvd\n',
    'zczc: 2\n',
    'ptdq: humn - dvpt\n',
    'dvpt: 3\n',
    'lfqf: 4\n',
    'humn: 5\n',
    'ljgn: 2\n',
    'sjmn: drzm * dbpl\n',
    'sllz: 4\n',
    'pppw: cczh / lfqf\n',
    'lgvd: ljgn * ptdq\n',
    'drzm: hmdt - zczc\n',
    'hmdt: 32\n',
]

def monkeyCircus(monkeys, ignoreMonkeys=[]):
    lopen = ['root']
    lclosed = []
    lwaiting = []

    while len(lopen) > 0 or len(lwaiting) > 0:
        if len(lopen) > 0:
            m_name = lopen.pop(0)
            m = monkeys[m_name]

        elif len(lwaiting) > 0:
            m_name = lwaiting.pop(0)
            m = monkeys[m_name]

        if m in ignoreMonkeys:
            lclosed.append(m)
            continue

        if m['depends'] == []:
            lclosed.append(m)
        else:
            if monkeys[m['depends'][0]['monkey']]['yells'] is not None:
                m['depends'][0]['yells'] = monkeys[m['depends'][0]['monkey']]['yells']
            else:
                if (m['depends'][0]['monkey'] not in lopen or m['depends'][0]['monkey'] not in lwaiting):
                    lopen.append(m['depends'][0]['monkey'])

            if monkeys[m['depends'][1]['monkey']]['yells'] is not None:
                m['depends'][1]['yells'] = monkeys[m['depends'][1]['monkey']]['yells']
            else:
                if (m['depends'][1]['monkey'] not in lopen or m['depends'][1]['monkey'] not in lwaiting):
                    lopen.append(m['depends'][1]['monkey'])

            if (m['depends'][0]['yells'] != None and m['depends'][1]['yells'] != None):
                exec(f"m['yells'] = int({m['depends'][0]['yells']} {m['job']} {m['depends'][1]['yells']})")
                lclosed.append(m_name)
            else:
                lwaiting.append(m_name)

    return monkeys

def part1(dryRun = False):
    print(f"PART 1, dryRun {dryRun}")
    if dryRun:
        lines = dry_lines
    else:
        lines = i_lines

    monkeys = {}
    for l in lines:
        monkey, yells = re.split(': ', l[:-1])

        try:
            job = None
            depends = []
            yells = int(yells)
        except ValueError:
            depends = [{'monkey': None, 'yells': None},{'monkey': None, 'yells': None}]
            depends[0]['monkey'], job, depends[1]['monkey'] = re.split(' ', yells)
            yells = None

        monkeys[monkey] = {'depends': depends, 'job': job, 'yells': yells}

    monkeys = monkeyCircus(monkeys)

    print(f"Answer: {monkeys['root']['yells']}")


def part2(dryRun = False):
    print(f"PART 2, dryRun {dryRun}")
    if dryRun:
        lines = dry_lines
    else:
        lines = i_lines

    monkeys = {}
    for l in lines:
        monkey, yells = re.split(': ', l[:-1])

        try:
            job = None
            depends = []
            yells = int(yells)
        except ValueError:
            depends = [{'monkey': None, 'yells': None},{'monkey': None, 'yells': None}]
            depends[0]['monkey'], job, depends[1]['monkey'] = re.split(' ', yells)
            yells = None

        monkeys[monkey] = {'depends': depends, 'job': job, 'yells': yells}

    monkeys['root']['job'] = '=='
    oMonkeys = copy.deepcopy(monkeys)

    s = [100000000000000, 0]
    while True:
        monkeys = copy.deepcopy(oMonkeys)
        monkeys['humn']['yells'] = int((s[1]+s[0])/2)
        monkeys = monkeyCircus(monkeys)
        above = monkeys['root']['depends'][0]['yells'] > monkeys['root']['depends'][1]['yells']
        if (monkeys['root']['yells'] == True):
            print(f"Answer: {monkeys['humn']['yells']}")
            break

        if above:
            s[1] = int((s[1]+s[0])/2)
            s[0] = s[0]
        else:
            s[1] = s[1]
            s[0] = int((s[1]+s[0])/2)

if __name__=="__main__":
    part1(dryRun = False)
    part2(dryRun = False)
