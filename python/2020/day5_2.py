#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

i = open("day5_in.txt", "r")
lines = i.readlines()
i.close()

# Test input
"""
lines = [
    "BFFFBBFRRR\n",
    "FFFBBBFRRR\n",
    "BBFFBBFRLL\n"
    ]
"""

class seat:
    def __init__(self, rowCode, colCode):
        self.rowCode = rowCode
        self.colCode = colCode
        self.row = self._calcRow(rowCode)
        self.col = self._calcCol(colCode)
        self.seatId = self._calcId(self.row, self.col)

    def __str__(self):
        return "[rowCode: "+str(self.rowCode)+", colCode: "+str(self.colCode)+", row: "+str(self.row)+", col: "+str(self.col)+", id: "+str(self.seatId)+"]"
    def __repr__(self):
        return "[rowCode: "+str(self.rowCode)+", colCode: "+str(self.colCode)+", row: "+str(self.row)+", col: "+str(self.col)+", id: "+str(self.seatId)+"]"

    def _calcRow(self, code):
        lowLim = 0
        upLim = 2**7-1
        for i in range(len(code)):
            if (code[i] == 'B'):
                lowLim += 2**i
            elif (code[i] == 'F'):
                upLim -= 2**i
        return lowLim

    def _calcCol(self, code):
        lowLim = 0
        upLim = 2**3-1
        for i in range(len(code)):
            if (code[i] == 'R'):
                lowLim += 2**i
            elif (code[i] == 'L'):
                upLim -= 2**i
        return lowLim

    def _calcId(self, row, col):
        return row * 8 + col

seats = []
ids = []

for line in lines:
    c, check, dummy = line.partition("\n")
    if check == "":
        raise Exception("Can't partition!")
    rowCode = list(c[:7])
    colCode = list(c[7:])
    rowCode.reverse()
    colCode.reverse()
    seat_entry = seat(rowCode, colCode)
    seats.append(seat_entry)
    ids.append(seat_entry.seatId)

#print(seats)

o = np.sort(ids)

#print(o)

for i in range(1000):
    x = np.where(o == i)
    if not x[0].size > 0:
        print(i)
