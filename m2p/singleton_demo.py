#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   singleton_demo.py
@Time    :   2019/06/26 21:00:57
@Author  :   Jin Weihua 
@Version :   1.0
@Contact :   jwhV587@gmail.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA
@Desc    :   None
'''

# here put the import lib
class Dog():
    init_flag = False
    def __new__(cls,name):
        if not hasattr(cls,'_name'):
            orgin = super(Dog,cls)
            cls._name = orgin.__new__(cls)  #不可以添加参数，因为继承的父类object的__new__
        return cls._name
    
    def __init__(self,name):
        if not Dog.init_flag:
            self.name = name
            Dog.init_flag = True
    

#decorate for class
class Decorator():
    
    def __init__(self,_cls):
        self.objCnt = 0
        self._cls = _cls
    
    def __call__(self,*args,**kwargs):
        self.objCnt += 1
        obj = self._cls(*args,**kwargs)
        print("instance: %s the %dth ins and name: %s" 
                %(self._cls.__name__,self.objCnt,obj.name))

@Decorator
class Test():
    def __init__(self,name):
        self.name = name
    
    def getName(self):
        return self.name

class A():
    def __init__(self,name):
        self.name=name
    
    def _protect(self):
        print("it's protected func")
    
    def __setItem(self,item):
        if item:
            self.name=item
        print("add item result:",self.name)
    
    def __add(self,item):
        print("add info:",item)
    
    def add(self,item):
        print("can be extend or not")

class B(A):
    def __init__(self,name,score):
        super(B,self)
        self.score=score
    
    def _protect(self,obj):
        print("current score is: ",self.score)
        return obj
    
    def __setItem(self,key):
        if key not in self.__dict__:
            self.__dict__[key]=key
        print("set method for B class")

def _pro(name):
    print("pro name is:",name)

def __pri(name):
    print("pri name is:",name)

def normal(name):
    print("normal name is:",name)


class F():
    def __init__(self,file):
        self.file = file
        self.f = None
    
    # def __enter__(self):
    #     print("=====enter===")
    #     return self.file
    
    def __exit__(self,ext,exv,extr):
        print("exit the file")
        print("ext:",ext)
        print("exv:",exv)
        print("extr:",extr)
    
    def do(self):
        res = self.f/2
        print("do res:",res)


if __name__ == "__main__":
    dog_a = Dog("a")
    print("id info: %s and name: %s and instance a name: %s" %(id(dog_a),dog_a.name))
    dog_b = Dog("b")
    print("id info: %s and name: %s and instance b name: %s" %(id(dog_b),dog_b.name))
    #输出均为--id info: 2854035287288 and name: a
    test_d = Test("test_d")
    print("instance 1 perform name={}".format(test_d.name))
    test_e = Test("test_e")
    print("instance 2 perform name={}".format(test_e.name))

    