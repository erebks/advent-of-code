#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Intcomputer unittests

import unittest
import intcomp
import re

class IntcomputerTest(unittest.TestCase):

    def setUp(self):
        self.comp = intcomp.Intcomputer(intcomp.instset)

    def test_fetchInst_fetchesADD(self):
        # Arrange
        self.comp.ram = [1]
        # Act
        inst, op_modes = self.comp.fetchInst(0)
        # Assert
        self.assertEqual(intcomp.INSTSET[0], inst)
        self.assertEqual([0,0,0], op_modes)

    def test_fetchInst_fetchesMULT(self):
        # Arrange
        self.comp.ram = [2]
        # Act
        inst, op_modes = self.comp.fetchInst(0)
        # Assert
        self.assertEqual(intcomp.INSTSET[1], inst)
        self.assertEqual([0,0,0], op_modes)

    def test_fetchInst_fetchesHALT(self):
        # Arrange
        self.comp.ram = [99]
        # Act
        inst, op_modes = self.comp.fetchInst(0)
        # Assert
        self.assertEqual(intcomp.INSTSET[-1], inst)
        self.assertEqual([0,0,0], op_modes)

    def test_fetchInst_fetchesOpModes(self):
        # Arrange
        self.comp.ram = [1002]
        # Act
        inst, op_modes = self.comp.fetchInst(0)
        # Assert
        self.assertEqual(intcomp.INSTSET[1], inst)
        self.assertEqual([0,1,0], op_modes)

    def test_fetchInst_raisesExceptionIfInstructionInvalid(self):
        # Arrange
        self.comp.ram = [999]
        # Act and Assert
        with self.assertRaises(intcomp.InstInvalid):
            self.comp.fetchInst(0)

    def test_fetchInst_raisesExceptionIfOutOfMem(self):
        # Arrange
        self.comp.ram = [1]
        # Act and Assert
        with self.assertRaises(intcomp.OutOfMem):
            self.comp.fetchInst(1)

    def test_fetchOp_fetches0Op(self):
        # Arrange
        self.comp.ram = [1,1,2,3]
        # Act
        op = self.comp.fetchOp({'op':'TEST', 'code':1, 'numOfOperands': 0})
        # Assert
        self.assertEqual([], op)

    def test_fetchOp_fetches1Op(self):
        # Arrange
        self.comp.ram = [1,1,2,3]
        # Act
        op = self.comp.fetchOp({'op':'TEST', 'code':1, 'numOfOperands': 1})
        # Assert
        self.assertEqual([1], op)

    def test_fetchOp_fetches3Op(self):
        # Arrange
        self.comp.ram = [1,1,2,3]
        # Act
        op = self.comp.fetchOp({'op':'TEST', 'code':1, 'numOfOperands': 3})
        # Assert
        self.assertEqual([1,2,3], op)

    def test_fetchOp_raisesOutOfMem(self):
        # Arrange
        self.comp.ram = [1]
        # Act and Assert
        with self.assertRaises(intcomp.OutOfMem):
            op = self.comp.fetchOp({'op':'TEST', 'code':1, 'numOfOperands': 1})

    def test_execute_executesInstruction(self):
        # Arrange
        self.comp.ram = [1,0,3,5]
        # Act
        ret = self.comp.execute(intcomp.INSTSET[0], [1,2,3])
        # Assert
        self.assertEqual(3+5, ret['result'])
        self.assertEqual(1, ret['resultAddr'])
        self.assertEqual(4, ret['newPC'])

    def test_writeBack_writesValueBack(self):
        # Arrange
        self.comp.ram = [0,0,0,0]
        result = intcomp.Result(result=1, resultAddr=2, newPC=3).get()
        # Act
        ret = self.comp.writeBack(result)
        # Assert
        self.assertEqual(1, self.comp.ram[2])
        self.assertEqual(3, self.comp.pc)

    def test_writeBack_raisesOutOfMem(self):
        # Arrange
        self.comp.ram = [1]
        result = intcomp.Result(1, 2, 3).get()
        # Act and Assert
        with self.assertRaises(intcomp.OutOfMem):
            op = self.comp.writeBack(result)

    def test_step_haltsOn99(self):
        # Arrange
        self.comp.ram = [99]
        # Act
        ret = self.comp.step()
        # Assert
        self.assertEqual(None, ret)

    def test_step_executesADDInstruction(self):
        # Arrange
        self.comp.ram = [1,1,2,4]
        # Act
        ret = self.comp.step()
        # Assert
        self.assertEqual(4, ret)
        self.assertEqual([1,1,2,2], self.comp.ram)

    def test_read_readsFromUser(self):
        # Arrange
        # Act
        ret = self.comp.read()
        # Assert
        self.assertEqual(1, ret)

    def test_prnt_printsToUser(self):
        # Arrange
        # Act
        ret = self.comp.prnt(69)
        # Assert

class InstTest(unittest.TestCase):
    def test_instADD_addsValues(self):
        # Arrange
        mem = [3,5,0]
        # Act
        ret = intcomp.instADD(mem, 0, [0,1,2], [0,0,0])
        # Assert
        self.assertEqual(3+5, ret['result'])
        self.assertEqual(2, ret['resultAddr'])
        self.assertEqual(4, ret['newPC'])

    def test_instADD_addsValuesWithImmMode(self):
        # Arrange
        mem = [0,0,0]
        # Act
        ret = intcomp.instADD(mem, 0, [3,5,2], [1,1,0])
        # Assert
        self.assertEqual(3+5, ret['result'])
        self.assertEqual(2, ret['resultAddr'])
        self.assertEqual(4, ret['newPC'])

    def test_instADD_addsValuesWithMixedMode(self):
        # Arrange
        mem = [0,5,0]
        # Act
        ret = intcomp.instADD(mem, 0, [3,1,2], [1,0,0])
        # Assert
        self.assertEqual(3+5, ret['result'])
        self.assertEqual(2, ret['resultAddr'])
        self.assertEqual(4, ret['newPC'])

    def test_instADD_raisesOutOfMem(self):
        # Arrange
        mem = [1]
        # Act and Assert
        with self.assertRaises(intcomp.OutOfMem):
            ret = intcomp.instADD(mem, 0, [0,1,2], [0,0,0])


    def test_instMUL_multipliesValues(self):
        # Arrange
        mem = [3,5,0]
        # Act
        ret = intcomp.instMUL(mem, 0, [0,1,2], [0,0,0])
        # Assert
        self.assertEqual(3*5, ret['result'])
        self.assertEqual(2, ret['resultAddr'])
        self.assertEqual(4, ret['newPC'])

    def test_instMUL_multipliesValuesWithImmMode(self):
        # Arrange
        mem = [0,0,0]
        # Act
        ret = intcomp.instMUL(mem, 0, [3,5,2], [1,1,0])
        # Assert
        self.assertEqual(3*5, ret['result'])
        self.assertEqual(2, ret['resultAddr'])
        self.assertEqual(4, ret['newPC'])

    def test_instMUL_multipliesValuesWithMixedMode(self):
        # Arrange
        mem = [0,5,0]
        # Act
        ret = intcomp.instMUL(mem, 0, [3,1,2], [1,0,0])
        # Assert
        self.assertEqual(3*5, ret['result'])
        self.assertEqual(2, ret['resultAddr'])
        self.assertEqual(4, ret['newPC'])

    def test_instMUL_raisesOutOfMem(self):
        # Arrange
        mem = [1]
        # Act and Assert
        with self.assertRaises(intcomp.OutOfMem):
            ret = intcomp.instMUL(mem, 0, [0,1,2], [0,0,0])

    def test_instHALT_haltsCPU(self):
        # Arrange
        mem = [3,5,0]
        # Act
        ret = intcomp.instHALT(mem, 0, [0,1,2], [0,0,0])
        # Assert
        self.assertEqual(None, ret['result'])
        self.assertEqual(None, ret['resultAddr'])
        self.assertEqual(None, ret['newPC'])

    def test_instREAD_readsFromUser(self):
        # Arrange
        mem = [0]
        def reader():
            return 1
        # Act
        ret = intcomp.instREAD(mem, 0, [0], [0,0,0], read=reader, prnt=None)
        # Assert
        self.assertEqual(1, ret['result'])
        self.assertEqual(0, ret['resultAddr'])
        self.assertEqual(2, ret['newPC'])

    def test_instPRNT_printsToUser(self):
        # Arrange
        mem = [69]
        def printer(s):
            print("CPU: "+str(s))
        # Act
        ret = intcomp.instPRNT(mem, 0, [0], [0,0,0], read=None, prnt=printer)
        # Assert -> USER
        self.assertEqual(2, ret['newPC'])


    def test_instJMPT_jumpesIfTrue(self):
        # Arrange
        mem = [1,5,0]
        # Act
        ret = intcomp.instJMPT(mem, 0, [0,1,2], [0,0,0])
        # Assert
        self.assertEqual(None, ret['result'])
        self.assertEqual(None, ret['resultAddr'])
        self.assertEqual(5, ret['newPC'])

    def test_instJMPT_jumpesNotIfFalse(self):
        # Arrange
        mem = [0,5,0]
        # Act
        ret = intcomp.instJMPT(mem, 0, [0,1,0], [0,0,0])
        # Assert
        self.assertEqual(None, ret['result'])
        self.assertEqual(None, ret['resultAddr'])
        self.assertEqual(3, ret['newPC'])

    def test_instJMPT_jumpesIfTrueWithImmMode(self):
        # Arrange
        mem = [0,0,0]
        # Act
        ret = intcomp.instJMPT(mem, 0, [1,5,2], [1,1,0])
        # Assert
        self.assertEqual(None, ret['result'])
        self.assertEqual(None, ret['resultAddr'])
        self.assertEqual(5, ret['newPC'])

    def test_instJMPT_jumpesIfTrueWithMixedMode(self):
        # Arrange
        mem = [0,5,0]
        # Act
        ret = intcomp.instJMPT(mem, 0, [1,1,2], [1,0,0])
        # Assert
        self.assertEqual(None, ret['result'])
        self.assertEqual(None, ret['resultAddr'])
        self.assertEqual(5, ret['newPC'])

    def test_instJMPT_raisesOutOfMem(self):
        # Arrange
        mem = [1]
        # Act and Assert
        with self.assertRaises(intcomp.OutOfMem):
            ret = intcomp.instJMPT(mem, 0, [0,1,2], [0,0,0])


    def test_instJMPF_jumpesIfFalse(self):
        # Arrange
        mem = [0,5,0]
        # Act
        ret = intcomp.instJMPF(mem, 0, [0,1,2], [0,0,0])
        # Assert
        self.assertEqual(None, ret['result'])
        self.assertEqual(None, ret['resultAddr'])
        self.assertEqual(5, ret['newPC'])

    def test_instJMPF_jumpesNotIfTrue(self):
        # Arrange
        mem = [1,5,0]
        # Act
        ret = intcomp.instJMPF(mem, 0, [0,1,0], [0,0,0])
        # Assert
        self.assertEqual(None, ret['result'])
        self.assertEqual(None, ret['resultAddr'])
        self.assertEqual(3, ret['newPC'])

    def test_instJMPF_jumpesIfFalseWithImmMode(self):
        # Arrange
        mem = [0,0,0]
        # Act
        ret = intcomp.instJMPF(mem, 0, [0,5,2], [1,1,0])
        # Assert
        self.assertEqual(None, ret['result'])
        self.assertEqual(None, ret['resultAddr'])
        self.assertEqual(5, ret['newPC'])

    def test_instJMPF_jumpesIfFalseWithMixedMode(self):
        # Arrange
        mem = [0,5,0]
        # Act
        ret = intcomp.instJMPF(mem, 0, [0,1,2], [1,0,0])
        # Assert
        self.assertEqual(None, ret['result'])
        self.assertEqual(None, ret['resultAddr'])
        self.assertEqual(5, ret['newPC'])

    def test_instJMPF_raisesOutOfMem(self):
        # Arrange
        mem = [1]
        # Act and Assert
        with self.assertRaises(intcomp.OutOfMem):
            ret = intcomp.instJMPF(mem, 0, [0,1,2], [0,0,0])


    def test_instLESS_writes1IfLess(self):
        # Arrange
        mem = [3,5,0]
        # Act
        ret = intcomp.instLESS(mem, 0, [0,1,2], [0,0,0])
        # Assert
        self.assertEqual(1, ret['result'])
        self.assertEqual(2, ret['resultAddr'])
        self.assertEqual(4, ret['newPC'])

    def test_instLESS_writes0IfNotLess(self):
        # Arrange
        mem = [5,3,0]
        # Act
        ret = intcomp.instLESS(mem, 0, [0,1,2], [0,0,0])
        # Assert
        self.assertEqual(0, ret['result'])
        self.assertEqual(2, ret['resultAddr'])
        self.assertEqual(4, ret['newPC'])

    def test_instLESS_writes1IfLessWithImmMode(self):
        # Arrange
        mem = [0,0,0]
        # Act
        ret = intcomp.instLESS(mem, 0, [3,5,2], [1,1,0])
        # Assert
        self.assertEqual(1, ret['result'])
        self.assertEqual(2, ret['resultAddr'])
        self.assertEqual(4, ret['newPC'])

    def test_instLESS_writes1IfLessWithMixedMode(self):
        # Arrange
        mem = [0,5,0]
        # Act
        ret = intcomp.instLESS(mem, 0, [3,1,2], [1,0,0])
        # Assert
        self.assertEqual(1, ret['result'])
        self.assertEqual(2, ret['resultAddr'])
        self.assertEqual(4, ret['newPC'])

    def test_instLESS_raisesOutOfMem(self):
        # Arrange
        mem = [1]
        # Act and Assert
        with self.assertRaises(intcomp.OutOfMem):
            ret = intcomp.instLESS(mem, 0, [0,1,2], [0,0,0])


    def test_instEQU_writes1IfEqual(self):
        # Arrange
        mem = [3,3,0]
        # Act
        ret = intcomp.instEQU(mem, 0, [0,1,2], [0,0,0])
        # Assert
        self.assertEqual(1, ret['result'])
        self.assertEqual(2, ret['resultAddr'])
        self.assertEqual(4, ret['newPC'])

    def test_instEQU_writes0IfNotLess(self):
        # Arrange
        mem = [5,3,0]
        # Act
        ret = intcomp.instEQU(mem, 0, [0,1,2], [0,0,0])
        # Assert
        self.assertEqual(0, ret['result'])
        self.assertEqual(2, ret['resultAddr'])
        self.assertEqual(4, ret['newPC'])

    def test_instEQU_writes1IfLessWithImmMode(self):
        # Arrange
        mem = [0,0,0]
        # Act
        ret = intcomp.instEQU(mem, 0, [3,3,2], [1,1,0])
        # Assert
        self.assertEqual(1, ret['result'])
        self.assertEqual(2, ret['resultAddr'])
        self.assertEqual(4, ret['newPC'])

    def test_instEQU_writes1IfLessWithMixedMode(self):
        # Arrange
        mem = [0,3,0]
        # Act
        ret = intcomp.instEQU(mem, 0, [3,1,2], [1,0,0])
        # Assert
        self.assertEqual(1, ret['result'])
        self.assertEqual(2, ret['resultAddr'])
        self.assertEqual(4, ret['newPC'])

    def test_instEQU_raisesOutOfMem(self):
        # Arrange
        mem = [1]
        # Act and Assert
        with self.assertRaises(intcomp.OutOfMem):
            ret = intcomp.instEQU(mem, 0, [0,1,2], [0,0,0])



class IntcomputerTest(unittest.TestCase):
    def setUp(self):
        self.comp = intcomp.Intcomputer(intcomp.INSTSET)

    def test_day2_testvector_1(self):
        # Arrange
        self.comp.ram = list(map(int,re.split(",", "1,9,10,3,2,3,11,0,99,30,40,50")))
        # Act
        cnt = 0
        while self.comp.step() is not None:
            cnt += 1
            continue
        # Assert
        self.assertEqual(2, cnt)
        self.assertEqual(list(map(int,re.split(",", "3500,9,10,70,2,3,11,0,99,30,40,50"))), self.comp.ram)

    def test_day2_testvector_2(self):
        # Arrange
        self.comp.ram = list(map(int,re.split(",", "1,0,0,0,99")))
        # Act
        cnt = 0
        while self.comp.step() is not None:
            cnt += 1
            continue
        # Assert
        self.assertEqual(list(map(int,re.split(",", "2,0,0,0,99"))), self.comp.ram)

    def test_day2_testvector_3(self):
        # Arrange
        self.comp.ram = list(map(int,re.split(",", "2,3,0,3,99")))
        # Act
        cnt = 0
        while self.comp.step() is not None:
            cnt += 1
            continue
        # Assert
        self.assertEqual(list(map(int,re.split(",", "2,3,0,6,99"))), self.comp.ram)

    def test_day2_testvector_3(self):
        # Arrange
        self.comp.ram = list(map(int,re.split(",", "2,4,4,5,99,0")))
        # Act
        cnt = 0
        while self.comp.step() is not None:
            cnt += 1
            continue
        # Assert
        self.assertEqual(list(map(int,re.split(",", "2,4,4,5,99,9801"))), self.comp.ram)

    def test_day2_testvector_4(self):
        # Arrange
        self.comp.ram = list(map(int,re.split(",", "1,1,1,4,99,5,6,0,99")))
        # Act
        cnt = 0
        while self.comp.step() is not None:
            cnt += 1
            continue
        # Assert
        self.assertEqual(list(map(int,re.split(",", "30,1,1,4,2,5,6,0,99"))), self.comp.ram)

    def test_day5_testvector_1(self):
        # Arrange
        self.comp.ram = list(map(int,re.split(",", "3,0,4,0,99")))
        # Act
        cnt = 0
        while self.comp.step() is not None:
            cnt += 1
            continue
        # Assert

    def test_day5_testvector_2(self):
        # Arrange
        self.comp.ram = list(map(int,re.split(",", "1002,4,3,4,33")))
        # Act
        cnt = 0
        while self.comp.step() is not None:
            cnt += 1
            continue
        # Assert
        self.assertEqual(list(map(int,re.split(",", "1002,4,3,4,99"))), self.comp.ram)

    def test_day5_testvector_3(self):
        # Arrange
        self.comp.ram = list(map(int,re.split(",", "1101,100,-1,4,0")))
        # Act
        cnt = 0
        while self.comp.step() is not None:
            cnt += 1
            continue
        # Assert
        self.assertEqual(list(map(int,re.split(",", "1101,100,-1,4,99"))), self.comp.ram)

if __name__ == '__main__':
    unittest.main()
