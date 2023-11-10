#!/usr/bin/env python3
# -*- coding: utf-8 -*-

i = open("day4_in.txt", "r")
lines = i.readlines()
i.close()

# Test input
"""
lines = [
    "ecl:gry pid:860033327 eyr:2020 hcl:#fffffd\n",
    "byr:1937 iyr:2017 cid:147 hgt:183cm\n",
    "\n",
    "iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884\n",
    "hcl:#cfa07d byr:1929\n",
    "\n",
    "hcl:#ae17e1 iyr:2013\n",
    "eyr:2024\n",
    "ecl:brn pid:760753108 byr:1931\n",
    "hgt:179cm\n",
    "\n",
    "hcl:#cfa07d eyr:2025 pid:166559648\n",
    "iyr:2011 ecl:brn hgt:59in\n",
    ]
"""

class passportEntry:
    def __init__(self, byr=None, iyr=None, eyr=None, hgt=None, hcl=None, ecl=None, pid=None, cid=None):
        self.byr = byr
        self.iyr = iyr
        self.eyr = eyr
        self.hgt = hgt
        self.hcl = hcl
        self.ecl = ecl
        self.pid = pid
        self.cid = cid
        self.valid = self._checkValidity()

    def __str__(self):
        return "[byr: "+str(self.byr)+" iyr: "+str(self.iyr)+" eyr: "+str(self.eyr)+" hgt: "+str(self.hgt)+" hcl: "+str(self.hcl)+" ecl: "+str(self.ecl)+" pid: "+str(self.pid)+" cid: "+str(self.cid)+" valid: "+str(self.valid)+"]"
    def __repr__(self):
        return "[byr: "+str(self.byr)+" iyr: "+str(self.iyr)+" eyr: "+str(self.eyr)+" hgt: "+str(self.hgt)+" hcl: "+str(self.hcl)+" ecl: "+str(self.ecl)+" pid: "+str(self.pid)+" cid: "+str(self.cid)+" valid: "+str(self.valid)+"]"

    def _checkValidity(self):
        if ((self.byr != None) and
           (self.iyr != None)  and
           (self.eyr != None)  and
           (self.hgt != None)  and
           (self.hcl != None)  and
           (self.ecl != None)  and
           (self.pid != None)):
#           (self.cid != None)):
            return True
        else:
            return False

l = []
s = ''

for i in range(len(lines)):
    if lines[i] == "\n":
        l.append(s)
        s = ''
    else:
        s1 = lines[i]
        s1 = s1.partition("\n")[0]
        s = s + s1 + " "
l.append(s)

#print(l)

db = []

for entry in l:
    byr = None
    iyr = None
    eyr = None
    hgt = None
    hcl = None
    ecl = None
    pid = None
    cid = None
    while True:
        s, dummy, entry = entry.partition(" ")
        if s == "":
            db_entry = passportEntry(byr, iyr, eyr, hgt, hcl, ecl, pid, cid)
            db.append(db_entry)
            break
        key, dummy, value = s.partition(":")
        if (key == "byr"):
            byr = value
        elif (key == "iyr"):
            iyr = value
        elif (key == "eyr"):
            eyr = value
        elif (key == "hgt"):
            hgt = value
        elif (key == "hcl"):
            hcl = value
        elif (key == "ecl"):
            ecl = value
        elif (key == "pid"):
            pid = value
        elif (key == "cid"):
            cid = value
        else:
            raise KeyError("Unknown Key")

print(db)
a = 0
for entry in db:
    if entry.valid:
        a +=1

print(a)
