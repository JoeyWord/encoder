#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   singleton.py
@Time    :   2019/06/24 23:46:48
@Author  :   Jin Weihua 
@Version :   1.0
@Contact :   jwhV587@gmail.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA
@Desc    :   test instance for singleton
'''

# here put the import lib
from threading import Thread
import threading
import time

class Singleton():

    def __new__(cls,name,**kwargs):
        if not hasattr(cls,'_instance'):
            _orig = super(Singleton,cls)
            cls._instance = _orig.__new__(cls,name,**kwargs)
        return cls._instance
    
class ThreadTest(Singleton):
    
    def __init__(self,name):
        self._lock = threading.RLock()
        self.name = "thread_" + name
    
    def send_message(self,msg):
        self._lock.acquire()
        time.sleep(3)
        print("now message: %s --> name:" %(msg,self.name))
        self._lock.release()

def run(msg,thread_t,name):
    thread_name = "thread_" + str(name)
    print("now thread is: %s and msg: %s and instance id: %s" %(thread_name,msg,id(thread_t)))
    thread_t.send_message(msg)


if __name__ == "__main__":

    threads = []
    msgs = ["go","come","bye"]
    for idx,msg in enumerate(msgs):
        work = ThreadTest(msg)
        
        thread = Thread(target=run,args=(msg,work,idx+1))
        threads.append(thread)
    for _t in threads:
        _t.start()
        # _t.setDaemon(True)
    _t.join()


