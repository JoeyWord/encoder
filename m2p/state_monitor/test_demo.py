#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   test_demo.py
@Time    :   2019/06/23 11:04:25
@Author  :   Jin Weihua 
@Version :   1.0
@Contact :   jwhV587@gmail.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA
@Desc    :   test file for state pattern
'''

# here put the import lib
from student import Student
from state_me import ExcellentState,CommonState,TerribleState

def test():
    student = Student()

    
    common_state = CommonState("common")
    student.set_score(60)
    student.behavior(common_state)

    terrible_state = TerribleState("terrible")
    student.remove_more_labor(20)
    student.behavior(terrible_state)

    excellent_state = ExcellentState("excellent")
    student.add_more_labor(30)
    student.behavior(excellent_state)

if __name__ == "__main__":
    test()
