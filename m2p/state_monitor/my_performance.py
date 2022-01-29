#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   my_performance.py
@Time    :   2019/06/22 15:13:41
@Author  :   Jin Weihua 
@Version :   1.0
@Contact :   jwhV587@gmail.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA
@Desc    :   None
'''

# here put the import lib

class Performance():

    def __init__(self):
        self.__cur_state = None
        self._states = set()
        self.__state_info = 60
    
    def get_state(self):
        return self.__cur_state
    
    def set_state(self,state):
        self.__cur_state = state
    
    def add_state(self,state):
        self._states.add(state)
    
    # def _get_state_info(self):
    #     return self.__state_info

    def _set_state_info(self,state_info):
        self.__state_info = state_info
        for state in self._states:
            if state.is_match(state_info):
                self.__change_state(state)
    
    def __change_state(self,state):
        if state is None:
            return False
        elif self.__cur_state is None:
            print("init state: ",state.get_name())
        else:
            print("state from %s to %s" %(self.__cur_state.get_name(),state.get_name()))
        self.__cur_state = state
        self.add_state(state)
        return True
    

    