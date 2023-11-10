#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import re

i = open("day2_in.txt", "r")
lines = i.readlines()
i.close()

class PwEntry:
    def __init__(self, firstOcc, secondOcc, ch, pw):
        self.firstOcc = firstOcc
        self.secondOcc = secondOcc
        self.ch = ch
        self.pw = pw
        self.valid = self._checkValidity()

    def __str__(self):
        return "[firstOcc: "+str(self.firstOcc)+" secondOcc: "+str(self.secondOcc)+" ch: "+self.ch+" pw: "+self.pw+" valid: "+str(self.valid)+"]"

    def __repr__(self):
        return "[firstOcc: "+str(self.firstOcc)+" secondOcc: "+str(self.secondOcc)+" ch: "+self.ch+" pw: "+self.pw+" valid: "+str(self.valid)+"]"

    def _checkValidity(self):
        return ((self.pw[self.firstOcc-1] == self.ch) ^ (self.pw[self.secondOcc-1] == self.ch))

def splitter(line):
    minVal, dummy, leftover = line.partition("-")
    maxVal, dummy, leftover = leftover.partition(" ")
    ch, dummy, pw = leftover.partition(": ")
    return int(minVal), int(maxVal), ch, pw

l = []

# Test data
#a = splitter("1-3 a: abcde")
#entry = PwEntry(a[0], a[1], a[2], a[3])
#l.append(entry)
#a = splitter("1-3 b: cdefg")
#entry = PwEntry(a[0], a[1], a[2], a[3])
#l.append(entry)
#a = splitter("2-9 c: ccccccccc")
#entry = PwEntry(a[0], a[1], a[2], a[3])
#l.append(entry)
#print(l)

c = 0

for line in lines:
    a = splitter(line)
    entry = PwEntry(a[0], a[1], a[2], a[3])
    l.append(entry)
    if l[-1].valid == True:
        c = c+1

print(c)
