#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   multiprocess.py
@Time    :   2019/07/23 22:31:23
@Author  :   Jin Weihua 
@Version :   1.0
@Contact :   jwhV587@gmail.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA
@Desc    :   None
'''

# here put the import lib

import multiprocessing
import os
import time
import threading

class MyThread(threading.Thread):
    """
    udf thread result for thread run and return value
    """
    def __init__(self,func,args,name):
        super(MyThread,self).__init__(target=func,args=args,name=name)
        self.res = None
        self.name = name
        self.func = func
        self.args = args
    def run():
        _res = self.func(*self.args)
        self.res=_res

from multiprocessing.pool import Pool
class MyPool(Pool):


def process_work(n):
    start = time.time()
    #s = sum(n)
    time.sleep(1)
    end = time.time()
    current_thread = threading.currentThread()

    print ("序列的父进程,以及当前进程的id为: %s,%s,%s" %(os.getpid(),current_thread.getName(),(end-start)))
    return sum(n)
def multi_process(worker,pNum,numData):
    p = multiprocessing.Pool(pNum)
    scale = divmod(len(numData),pNum)[0]
    #print scale
    if divmod(len(numData),pNum)[1] != 0:
        scale += 1
    start_id = 0
    for ind in range(pNum):
        end_id = start_id + scale
        if start_id > len(numData)-1:
            p.apply_async(worker,args=(numData[(end_id-2*scale):]))
            break
        p.apply_async(worker,args=(numData[start_id:end_id],))
        start_id = end_id
    p.close()
    p.join()
def multi_thread(worker,pNum,numData,threadName):
    threads = []
    scale,reserve = divmod(len(numData),pNum)
    # print reserve
    if reserve > 0:
        scale += 1
    for ind in range(pNum):
        name = threadName + str(ind)
        try:
            thread = threading.Thread(target=worker,args=(numData[ind*scale:(ind+1)*scale],),name=name)
            thread.setDaemon(True)  # 设置为守护线程，即当主线程结束，该线程也会终止
            thread.start()  # 开启线程
            threads.append(thread)
        except Exception as e:
            print(e)
            break
    for thread in threads:
        # thread.setDaemon(True)
        # thread.start()
        thread.join()

if __name__ == '__main__':
    numData = range(20)
    time0 = time.time()
    #multi_process(5,numData)
    multi_thread(process_work,5,numData,"test_thread")
    time1 = time.time()
    print("all threads run over cost time={}".format(time1-time0))
    num_thread = 5
    scale,yu = divmod(len(numData/num_thread))
    if yu > 0:
        scale += 1
    threads = []
    results = []
    for idx in num_thread:
        name = "myThread_" + str(idx)
        try:
            thread = MyThread(process_work,numData[idx*scale:(idx+1)*scale])
        except:
            break
        else:
            thread.setDaemon(True)
            thread.start()
            threads.append(thread)
    for thread in threads:
        thread.join()
        with threading.Lock():
            results.append(thread.res)
    print("results:",results)
    #print("all process run over cost time={}".format(time1 - time0))
    #os.system("pstree -p " + str(os.getpid()))