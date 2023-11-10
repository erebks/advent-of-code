#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Intcomputer for AoC 2019

import logging

logging.basicConfig(format='%(levelname)s:%(message)s')
l = logging.getLogger(__name__)
l.setLevel(logging.INFO)

# Instructions
# Number | Assembler          | Description
# -------|--------------------|----------------------------------
#      1 | ADD [a], [b], [c]  | a+b=c
#      2 | MUL [a], [b], [c]  | a*b=c
#      3 | READ [a]           | -> a
#      4 | PRNT [a]           | <- a
#      5 | JMPT [a], [b]      | JUMP to b if a != 0
#      6 | JMPF [a], [b]      | JUMP to b if a == 0
#      7 | LESS [a], [b], [c] | c = 1 if a < b else 0
#      8 | EQU [a], [b], [c]  | c = 1 if a == b else 0
#     99 | HALT               | Halts the CPU

class Result:
    def __init__(self, result, resultAddr, newPC):
        self.res = {'result': result, 'resultAddr': resultAddr, 'newPC': newPC}

    def get(self):
        return self.res

def instADD(mem, pc, ops, op_modes, read=None, prnt=None):
    try:
        if op_modes[0] == 0:
            a = mem[ops[0]]
        elif op_modes[0] == 1:
            a = ops[0]
        else:
            raise OpModeInvalid("OpMode 0 invalid: "+str(op_modes))

        if op_modes[1] == 0:
            b = mem[ops[1]]
        elif op_modes[1] == 1:
            b = ops[1]
        else:
            raise OpModeInvalid("OpMode 1 invalid: "+str(op_modes))

        res = a + b
    except IndexError:
        raise OutOfMem("Could not execute. OP: "+str(ops))

    result = Result(res, ops[2], pc+4)
    return result.get()

def instMUL(mem, pc, ops, op_modes, read=None, prnt=None):
    try:
        if op_modes[0] == 0:
            a = mem[ops[0]]
        elif op_modes[0] == 1:
            a = ops[0]
        else:
            raise OpModeInvalid("OpMode 0 invalid: "+str(op_modes))

        if op_modes[1] == 0:
            b = mem[ops[1]]
        elif op_modes[1] == 1:
            b = ops[1]
        else:
            raise OpModeInvalid("OpMode 1 invalid: "+str(op_modes))

        res = a * b
    except IndexError:
        raise OutOfMem("Could not execute. OP: "+str(ops))

    result = Result(res, ops[2], pc+4)
    return result.get()

def instREAD(mem, pc, ops, op_modes, read, prnt):
    return Result(read(), ops[0], pc+2).get()

def instPRNT(mem, pc, ops, op_modes, read, prnt):
    if op_modes[0] == 0:
        a = mem[ops[0]]
    elif op_modes[0] == 1:
        a = ops[0]
    else:
        raise OpModeInvalid("OpMode 0 invalid: "+str(op_modes))
    prnt(a)
    return Result(None, None, pc+2).get()


def instJMPT(mem, pc, ops, op_modes, read=None, prnt=None):
    try:
        if op_modes[0] == 0:
            a = mem[ops[0]]
        elif op_modes[0] == 1:
            a = ops[0]
        else:
            raise OpModeInvalid("OpMode 0 invalid: "+str(op_modes))

        if op_modes[1] == 0:
            b = mem[ops[1]]
        elif op_modes[1] == 1:
            b = ops[1]
        else:
            raise OpModeInvalid("OpMode 1 invalid: "+str(op_modes))

        if a != 0:
            jmpAddr = b
        else:
            jmpAddr = pc+3
    except IndexError:
        raise OutOfMem("Could not execute. OP: "+str(ops))

    result = Result(None, None, jmpAddr)
    return result.get()


def instJMPF(mem, pc, ops, op_modes, read=None, prnt=None):
    try:
        if op_modes[0] == 0:
            a = mem[ops[0]]
        elif op_modes[0] == 1:
            a = ops[0]
        else:
            raise OpModeInvalid("OpMode 0 invalid: "+str(op_modes))

        if op_modes[1] == 0:
            b = mem[ops[1]]
        elif op_modes[1] == 1:
            b = ops[1]
        else:
            raise OpModeInvalid("OpMode 1 invalid: "+str(op_modes))

        if a == 0:
            jmpAddr = b
        else:
            jmpAddr = pc+3
    except IndexError:
        raise OutOfMem("Could not execute. OP: "+str(ops))

    result = Result(None, None, jmpAddr)
    return result.get()

def instLESS(mem, pc, ops, op_modes, read=None, prnt=None):
    try:
        if op_modes[0] == 0:
            a = mem[ops[0]]
        elif op_modes[0] == 1:
            a = ops[0]
        else:
            raise OpModeInvalid("OpMode 0 invalid: "+str(op_modes))

        if op_modes[1] == 0:
            b = mem[ops[1]]
        elif op_modes[1] == 1:
            b = ops[1]
        else:
            raise OpModeInvalid("OpMode 1 invalid: "+str(op_modes))

        if ( a < b ):
            res = 1
        else:
            res = 0
    except IndexError:
        raise OutOfMem("Could not execute. OP: "+str(ops))

    result = Result(res, ops[2], pc+4)
    return result.get()

def instEQU(mem, pc, ops, op_modes, read=None, prnt=None):
    try:
        if op_modes[0] == 0:
            a = mem[ops[0]]
        elif op_modes[0] == 1:
            a = ops[0]
        else:
            raise OpModeInvalid("OpMode 0 invalid: "+str(op_modes))

        if op_modes[1] == 0:
            b = mem[ops[1]]
        elif op_modes[1] == 1:
            b = ops[1]
        else:
            raise OpModeInvalid("OpMode 1 invalid: "+str(op_modes))

        if ( a == b ):
            res = 1
        else:
            res = 0
    except IndexError:
        raise OutOfMem("Could not execute. OP: "+str(ops))

    result = Result(res, ops[2], pc+4)
    return result.get()

def instHALT(mem, pc, ops, op_modes, read=None, prnt=None):
    return {'result': None, 'newPC': None, 'resultAddr': None}


INSTSET = [
    {'op':'ADD',  'code':1,  'numOfOperands': 3, 'exec': instADD  },
    {'op':'MUL',  'code':2,  'numOfOperands': 3, 'exec': instMUL  },
    {'op':'READ', 'code':3,  'numOfOperands': 1, 'exec': instREAD },
    {'op':'PRNT', 'code':4,  'numOfOperands': 1, 'exec': instPRNT },
    {'op':'JMPT', 'code':5,  'numOfOperands': 2, 'exec': instJMPT },
    {'op':'JMPF', 'code':6,  'numOfOperands': 2, 'exec': instJMPF },
    {'op':'LESS', 'code':7,  'numOfOperands': 3, 'exec': instLESS },
    {'op':'EQU',  'code':8,  'numOfOperands': 3, 'exec': instEQU },
    {'op':'HALT', 'code':99, 'numOfOperands': 0, 'exec': instHALT },
]

class Intcomputer:
    def __init__(self, instset):
        # Init an intcomputer with instructionset
        self.ram = []          # RAM
        self.pc = 0            # Program counter
        self.instset = instset # Instset
        l.debug("New CPU with instset: "+str(instset))

    def __str__(self):
        return str("PC: "+str(self.pc))

    def __repr__(self):
        return str("PC: "+str(self.pc))

    def loadMem(self, mem):
        # Loads given memory
        l.debug("Loading Memory: "+str(mem))
        self.ram = mem
        self.pc = 0

    def fetchInst(self, pc):
        # Fetch next instruction at PC
        try:
            fetched_inst = str("%05d" %self.ram[pc])
            op_modes = [int(fetched_inst[2]), int(fetched_inst[1]), int(fetched_inst[0])]
            fetched_inst = int(fetched_inst[3]+fetched_inst[4])
            inst = list(filter(lambda inst: inst['code'] == fetched_inst, self.instset))
        except IndexError:
            raise OutOfMem("PC: "+str(pc)+", exceeds RAM")

        try:
            inst = inst[0]
        except IndexError:
            raise InstInvalid("INST: "+str(self.ram[pc])+", not found")

        l.debug("Fetched instruction: %d -> %s, op_modes: %s", self.ram[pc], inst, op_modes)
        return inst, op_modes

    def fetchOp(self, inst):
        op = []
        try:
            # Fetch operands as defined in instset
            for i in range(inst['numOfOperands']):
                op.append(self.ram[self.pc+(i+1)])

        except IndexError:
            raise OutOfMem("PC: "+str(self.pc)+" + "+str(i+1)+", exceeds RAM")
        except TypeError:
            pass
        l.debug("Fetched operands: %s", op)
        return op

    def execute(self, inst, ops, op_modes):
        # Execute instruction defined by instruction-list
        return inst['exec'](self.ram, self.pc, ops, op_modes, self.read, self.prnt)

    def writeBack(self, result):
        # Write to RAM
        try:
            self.ram[result['resultAddr']] = result['result']
            l.debug("Wrote %d to Addr %d", result['result'], result['resultAddr'])
        except IndexError:
            raise OutOfMem("Could not write %d to Addr %d", result['result'], result['resultAddr'])
        except TypeError:
            pass

        # Write PC
        self.pc = result['newPC']
        l.debug("New PC: %s", self.pc)
        return

    def read(self):
        return int(input("STOP -> USER: "))

    def prnt(self, text):
        print("Computer says: "+str(text))

    def step(self):
        # Executes one instruction
        inst, op_modes = self.fetchInst(self.pc)
        ops = self.fetchOp(inst)
        result = self.execute(inst, ops, op_modes)
        self.writeBack(result)

        if (self.pc is None):
            l.info("CPU HALTED")
        else:
            l.info("CPU: %d", self.pc)

        return self.pc

class OutOfMem(Exception):
    pass

class InstInvalid(Exception):
    pass

class NothingToWrite(Exception):
    pass
