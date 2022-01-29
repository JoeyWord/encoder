#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   state_me.py
@Time    :   2019/06/22 15:03:08
@Author  :   Jin Weihua 
@Version :   1.0
@Contact :   jwhV587@gmail.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA
@Desc    :   various state to instance by singleton pattern
'''

# here put the import lib
from wrapt import decorator
from state_interface import State

#define singleton pattern by decorator

def singleton(cls,*args,**kwargs):
    instance_dict = {}
    def _singleton(*args,**kwargs):
        if cls not in instance_dict:
            print("current cls type:{}".format(type(cls)))
            instance_dict[cls] = cls(*args,**kwargs)
        return instance_dict[cls]
    return _singleton

@singleton
class ExcellentState(State):

    def __init__(self,name):
        super(ExcellentState,self).__init__(name)
    
    def is_match(self,stateInfo):
        return stateInfo >= 80
    
    def behavior(self,performance):
        print("I am good at my performance: " + performance.__state_info)

@singleton
class CommonState(State):

    def __init__(self,name):
        super(ExcellentState,self).__init__(name)
    
    def is_match(self,stateInfo):
        return (stateInfo < 80) & (stateInfo >= 60)
    
    def behavior(self,performance):
        print("my performance perform a bit little bad: " + performance.__state_info)

@singleton
class TerribleState(State):

    def __init__(self,name):
        super(ExcellentState,self).__init__(name)
    
    def is_match(self,stateInfo):
        return stateInfo < 60
    
    def behavior(self,performance):
        print("my parent and tearcher angry: " + performance.__state_info)




