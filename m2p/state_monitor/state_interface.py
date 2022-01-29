#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   state_interface.py
@Time    :   2019/06/22 14:51:53
@Author  :   Jin Weihua 
@Version :   1.0
@Contact :   jwhV587@gmail.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA
@Desc    :   None
'''

# here put the import lib
from abc import ABCMeta,abstractmethod

class State(ABCMeta):

    def __init__(self,name):
        self.name = name
    
    def get_name(self):
        return self.name
    
    def is_match(self,stateInfo):
        return False
    
    @abstractmethod
    def behaviou(self):
        pass

