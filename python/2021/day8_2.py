#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Advent of Code 2021 Day 8 part 2

import re
import numpy as np
import copy
import pdb

i = open("day8_in.txt", "r")
lines = i.readlines()
i.close()

"""
# Testinput -> output [8,5,2,3,7,9,6,4,0,1] | [5,3,5,3]
lines = [
    "acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf\n"
]
"""

"""
# Testinput -> output -> Sum of all: 61229
lines = [
    "be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe\n", # [8,3,9,4]
    "edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc\n",     # [9,7,8,1]
    "fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg\n",          # [1,1,9,7]
    "fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb\n",    # [9,3,6,1]
    "aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea\n",    # [4,8,7,3]
    "fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb\n",   # [8,4,1,8]
    "dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe\n",   # [4,5,4,8]
    "bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef\n",     # [1,6,2,5]
    "egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb\n",        # [8,7,1,7]
    "gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce\n",       # [4,3,1,5]
]
"""

def mapper(s):
    # Gets a string with chars a-f and converts to a 7 dim. vector
    o = np.zeros(7, bool)
    for seg in s:
        if seg == 'a':
            o[0] = True
        elif seg == 'b':
            o[1] = True
        elif seg == 'c':
            o[2] = True
        elif seg == 'd':
            o[3] = True
        elif seg == 'e':
            o[4] = True
        elif seg == 'f':
            o[5] = True
        elif seg == 'g':
            o[6] = True
        else:
            raise ValueError("Can't decode char '%c'", seg)
    return o

def segmentParser(seg):
    if np.array_equal(seg,[True, True, True, False, True, True, True]):
        return 0
    if np.array_equal(seg,[False, False, True, False, False, True, False]):
        return 1
    if np.array_equal(seg,[True, False, True, True, True, False, True]):
        return 2
    if np.array_equal(seg,[True, False, True, True, False, True, True]):
        return 3
    if np.array_equal(seg,[False, True, True, True, False, True, False]):
        return 4
    if np.array_equal(seg,[True, True, False, True, False, True, True]):
        return 5
    if np.array_equal(seg,[True, True, False, True, True, True, True]):
        return 6
    if np.array_equal(seg,[True, False, True, False, False, True, False]):
        return 7
    if np.array_equal(seg,[True, True, True, True, True, True, True]):
        return 8
    if np.array_equal(seg,[True, True, True, True, False, True, True]):
        return 9


displays = []

for l in lines:
    l = re.sub("\n","",l)
    inp, outp = re.split("\s\|\s",l)
    inp = re.split("\s", inp)
    outp = re.split("\s", outp)

    mapped_inputs = []
    mapped_outputs = []

    for entry in inp:
        mapped_inputs.append(mapper(entry))
    for entry in outp:
        mapped_outputs.append(mapper(entry))

    displays.append({"patterns": mapped_inputs, "display": mapped_outputs})

display_results = []

for display in displays:
    # Determine 1,4,7 and 8
    patterns = {'#2':[],'#3':[],'#4':[],'#5':[],'#6':[],'#7':[]}
    segments = {}
    # Organize according to numOfElements
    for pattern in display["patterns"]:
        if np.sum(pattern) == 2:   # digit 1
            patterns['#2'].append(pattern)
            segments['1'] = pattern
        elif np.sum(pattern) == 3: # digit 7
            patterns['#3'].append(pattern)
            segments['7'] = pattern
        elif np.sum(pattern) == 4: # digit 4
            patterns['#4'].append(pattern)
            segments['4'] = pattern
        elif np.sum(pattern) == 5: # digit 2,3,5
            patterns['#5'].append(pattern)
        elif np.sum(pattern) == 6: # digit 0,6,9
            patterns['#6'].append(pattern)
        elif np.sum(pattern) == 7: # digit 8
            patterns['#7'].append(pattern)
            segments['8'] = pattern
        else:
            raise ValueError("NumOfSegments too high")

    # Get all digits that can be known at this point
    # Search for digit 6 -> digit 1 & digit 6 = 1 element
    for pattern in patterns['#6']:
        if (np.sum(pattern & segments['4']) == 3):
            # Found digit 0 or 6
            if (np.sum(pattern & segments['1']) == 1):
                # Found digit 6
                segments['6'] = pattern
            else:
                segments['0'] = pattern
        elif (np.sum(pattern & segments['1']) == 2):
            # Found digit 9
            segments['9'] = pattern
        else:
            raise ValueError("Can't find pattern 6 or 9")

    for pattern in patterns['#5']:
        if (np.sum(pattern ^ segments['4']) == 5):
            # Found digit 2
            segments['2'] = pattern
        elif (np.sum(pattern ^ segments['7']) == 2):
            # Found digit 3
            segments['3'] = pattern
        else:
            # Found digit 5
            segments['5'] = pattern

    # matrix for mapping
    # first col -> mapping for A and so on
    print(segments)
    mat = np.zeros((7,7), bool)
    mat[:,2] = segments['1'] & ~segments['6']        #C
    mat[:,3] = ~segments['0'] & segments['8']        #D
    mat[:,4] = ~(segments['9'] & segments['8'])      #E
    mat[:,5] = segments['1'] & segments['6']         #F

    mat[:,0] = segments['7'] & ~mat[:,2] & ~mat[:,5] #A
    mat[:,1] = ~(segments['2'] | mat[:,5])           #B
    mat[:,6] = ~(mat[:,0] |
                 mat[:,1] |
                 mat[:,2] |
                 mat[:,3] |
                 mat[:,4] |
                 mat[:,5])                           #G

    # Inverse matrix!
    mat = np.array(np.linalg.inv(mat), bool)
    print(mat)

    disp = [np.matmul(mat,np.array(display['display'][0])),
            np.matmul(mat,np.array(display['display'][1])),
            np.matmul(mat,np.array(display['display'][2])),
            np.matmul(mat,np.array(display['display'][3]))]
    disp_int = list(map(segmentParser, disp))
    display_results.append(int("".join(map(str, disp_int))))
    print("DISP: "+str(disp_int)+" -> "+str(display_results[-1]))

print("Answer: "+str(sum(display_results)))
