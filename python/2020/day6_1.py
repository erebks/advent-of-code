#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

i = open("day6_in.txt", "r")
lines = i.readlines()
i.close()

# Test input
lines = [
    "abc\n",
    "\n",
    "a\n",
    "b\n",
    "c\n",
    "\n",
    "ab\n",
    "ac\n",
    "\n",
    "a\n",
    "a\n",
    "a\n",
    "a\n",
    "\n",
    "b\n",
]

class Group:
    def __init__(self, numMembers, answers_code):
        self.numMembers = numMembers
        self.answers_code = answers_code
        self.answers = self._getAnswers(answers_code)

    def __str__(self):
        return None
    def __repr__(self):
        return None

    def _getAnswers(self, code):
        return None

l = []
questionaire = {'s':"", 'numMembers':0}

for i in range(len(lines)):
    if lines[i] == "\n":
        l.append(questionaire)
        questionaire = {'s':"", 'numMembers':0}
    else:
        s1 = lines[i]
        s1 = s1.partition("\n")[0]
        questionaire['numMembers'] += 1
        questionaire['s'] += s1

l.append(questionaire)

print(l)
