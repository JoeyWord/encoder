#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   my_class.py
@Time    :   2019/08/08 00:10:24
@Author  :   Jin Weihua 
@Version :   1.0
@Contact :   jwhV587@gmail.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA
@Desc    :   None
'''

# here put the import lib
class A:
    name = "a_cls"
    def __init__(self,name):
        self.a = name
        self.common = "yes"

    def fo(self,name):
        self.a = name
    
    def _pro_a(self):
        return self.a
    
    @classmethod
    def change_cls(cls):
        if cls.name.startswith("a"):
            return True
        return False

    @staticmethod
    def sta():
        
        return "a method"


class B:
    def __init__(self,name):
        self.b = name
        self.common = "no"
    
    def fo(self,name):
        self.b = name
    
    def _pro_b(self):
        return "pro_b"
    
    def __pri_b(self):
        return "pri_b"
    
    @staticmethod
    def sta_b():
        
        return "b method"

class C(B,A):
    def __init__(self,name):
        self.c = "c"
        # super().__init__(name)
    def fo(self,name):

        self.a = name

    

if __name__ == "__main__":
    c = C("b")
    print("c common attr value: {}".format(c.common))
    # c.fo("modify")
    # print("current attr:{}|{}".format(c.a,c.b))
    
    # res = c.sta()
    # print("common def value:{}".format(res))
    c_pro = c._pro_b()
    print("c pro:",c_pro)
