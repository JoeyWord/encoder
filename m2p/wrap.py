# coding=utf-8

from wrapt import decorator
from time import time

#common decorator demo
def test_decorator1(func):
    def wrapper(n):
        t0 = time()
        ans = func(n)
        t1 = time()
        print ("time cost:{} and ans:{}".format((t1-t0),ans))
        return ans
    return wrapper
@test_decorator1
def func1(m):
    for i in range(m):
        if i**2 == 625:
            return i
    return m

@decorator
def test_decorator2(func,instance,args,kwargs):
    t0 = time()
    ans = func(*args)
    t1 = time()
    print ("test2 cost time: %.2f and ans= %d" %(t1-t0,ans))
    return ans

@test_decorator2
def factorial(m):
    if m == 1:
        return 1
    elif m <= 0:
        raise ValueError("factorial comp input params illegal")
    else:
        a = m*factorial(m-1)
        return a

def test_decorator3(esp,retry=2):
    @decorator
    def wrapper(func,isinstance,n,kwargs):
        t0=time()
        print("position argument:{} and {}".format(n,kwargs))
        if esp>0:
            if retry:
                ans = func(n,kwargs)
            else:
                ans = -1
        else:
            print ("esp is negative to pass params")
            ans = "no match"
        t1 = time()
        print ("test2 cost time: %.2f and ans= %s" %(t1-t0,ans))
        return ans
    return wrapper

@test_decorator3(0.5,retry=0)
def sum_func(m,limit_n):
    sum_val = 0
    print ("m value={} and type m={}".format(m,type(m)))
    if m>1:
        for i in range(1,m+1):
            sum_val += i
            if i > limit_n:
                sum_val = 0
                break
    else:
        m_t = int(1/m)
        for i in range(1,m_t+1):
            sum_val += 1/i
            if i > limit_n:
                sum_val = 1
    return sum_val

from lxml import objectify
from lxml.objectify import ObjectifiedElement
from functools import wraps

ns = """

    """

# def test_decorator4(XPATH,OBJ_TYPE="list"):
#     @Wraps
#     def wraper(func):
#         def inner(objectifiedElement:ObjectifiedElement,namespace):
            
#             xnodes = ObjectifiedElement.xpath(XPATH,namespaces=namespace)
#             if xnodes:
#                 if OBJ_TYPE == "list":
#                     rets = []
#                     for node in xnodes:
#                         rets.append(func(node))
#                     return rets
#                 else:
#                     ret = func(xnodes[0])
#                     return ret
#             else:
#                 if OBJ_TYPE == "list":
#                     return []
#                 else:
#                     return None
#         return inner
#     return wraper


def test_decorator4(XPATH,OBJ_TYPE="list"):
    @decorator
    def inner(func,instance,objectifiedElement,kwargs):
        
        xnodes = objectifiedElement[0].xpath(XPATH,namespaces=objectifiedElement[1])
        if xnodes:
            if OBJ_TYPE == "list":
                rets = []
                for node in xnodes:
                    rets.append(func(*objectifiedElement))
                return rets
            else:
                ret = func(*objectifiedElement)
                return ret
        else:
            if OBJ_TYPE == "list":
                return []
            else:
                return None

    return inner


if __name__ == "__main__":
    res=func1(10000)
    print ("res = {}\nfunc1 name:{} and decorator name:{}\n\n".format(res,func1.__name__,test_decorator1.__name__))
    factorial_res = factorial(5)
    print ("factorial res = {}\nfunc name:{} and decorator2 name:{}".format(factorial_res,factorial.__name__,test_decorator2.__name__))
    sum_res = sum_func(1001,100)
    print ("sum_val res = {}\nfunc name:{} and decorator3 name:{}".format(sum_res,sum_func.__name__,test_decorator3.__name__))
    

