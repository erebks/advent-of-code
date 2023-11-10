#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

i = open("day4_in.txt", "r")
lines = i.readlines()
i.close()

# Test input
"""
lines = [ # all invalid
    "eyr:1972 cid:100\n",
    "hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926\n",
    "\n",
    "iyr:2019\n",
    "hcl:#602927 eyr:1967 hgt:170cm\n",
    "ecl:grn pid:012533040 byr:1946\n",
    "\n",
    "hcl:dab227 iyr:2012\n",
    "ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277\n",
    "\n",
    "hgt:59cm ecl:zzz\n",
    "eyr:2038 hcl:74454a iyr:2023\n",
    "pid:3556412378 byr:2007\n"
]
"""
"""
lines = [ # all valid
    "pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980\n",
    "hcl:#623a2f\n",
    "\n",
    "eyr:2029 ecl:blu cid:129 byr:1989\n",
    "iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm\n",
    "\n",
    "hcl:#888785\n",
    "hgt:164cm byr:2001 iyr:2015 cid:88\n",
    "pid:545766238 ecl:hzl\n",
    "eyr:2022\n",
    "\n",
    "iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719\n"
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
        if ((self._checkByr() == True ) and
           (self._checkIyr() == True )  and
           (self._checkEyr() == True )  and
           (self._checkHgt() == True )  and
           (self._checkHcl() == True )  and
           (self._checkEcl() == True )  and
           (self._checkPid() == True)):
            return True
        else:
            return False

    def _checkByr(self):
        try:
            if (int(self.byr) < 1920 or int(self.byr) > 2002):
                print("byr invalid")
                return False
            return True
        except:
            print("byr invalid by exception: "+str(self.byr))
            return False

    def _checkIyr(self):
        try:
            if (int(self.iyr) < 2010 or int(self.iyr) > 2020):
                print("iyr invalid")
                return False
            return True
        except:
            print("iyr invalid by exception: "+str(self.iyr))
            return False

    def _checkEyr(self):
        try:
            if (int(self.eyr) < 2020 or int(self.eyr) > 2030):
                print("eyr invalid")
                return False
            return True
        except:
            print("eyr invalid by exception: "+str(self.eyr))
            return False

    def _checkHgt(self):
        try:
            a, c, dummy = self.hgt.partition("cm")
            if c == "":
                a, c, dummy = self.hgt.partition("in")
                if c == "":
                    print("hgt invalid")
                    return False
                else:
                    if (int(a) < 59 or int(a) > 76):
                        print("hgt invalid")
                        return False
            else:
                if (int(a) < 150 or int(a) > 193):
                    print("hgt invalid")
                    return False
            return True
        except:
            print("hgt invalid by exception: "+str(self.hgt))
            return False

    def _checkHcl(self):
        try:
            #RegEx
            if re.search("^#[0-9a-f]{6}$", self.hcl):
                return True
            print("hcl invalid")
            return False
        except:
            print("hcl invalid by exception")
            return False

    def _checkEcl(self):
        try:
            #RegEx
            if re.search("^(amb|blu|brn|gry|grn|hzl|oth)$", self.ecl):
                return True
            print("ecl invalid")
            return False
        except:
            print("ecl invalid by exception")
            return False

    def _checkPid(self):
        try:
            if (len(self.pid) != 9):
                print("pid invalid")
                return False
            return True
        except:
            print("pid invalid by exception")
            return False

    def _checkCid(self):
        return True


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
