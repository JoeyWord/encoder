#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   student.py
@Time    :   2019/06/23 10:23:09
@Author  :   Jin Weihua 
@Version :   1.0
@Contact :   jwhV587@gmail.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA
@Desc    :   class to describe attribute of student inherit from performance
'''

# here put the import lib
from my_performance import Performance
from state_interface import State
from state_me import ExcellentState,CommonState,TerribleState

class Student(Performance):

    def __init__(self):
        super().__init__()
        self.add_state(ExcellentState('excellent'))
        self.add_state(CommonState("common"))
        self.add_state(TerribleState("terrible"))
        self._set_state_info(60)

    def get_score(self):
        return self._get_state_info()
    
    def set_score(self,score):
        self._set_state_info(score)
    
    def add_more_labor(self,labor):
        self._set_state_info(self.__state_info + labor)
    
    def remove_more_labor(self,labor):
        self._set_state_info(self.__state_info - labor)
    
    def behavior(self,state):
        self.__cur_state = state
        if isinstance(state,State):
            state.behavior(self)

