#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   df_demo.py
@Time    :   2019/06/28 23:29:25
@Author  :   Jin Weihua 
@Version :   1.0
@Contact :   jwhV587@gmail.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA
@Desc    :   None
'''

# here put the import lib
import pandas as pd
from numpy import arange,random
from copy import copy,deepcopy

_data = arange(0,9)
_data = _data.reshape(3,3)
_col = ["a","b","c"]
_df = pd.DataFrame(_data,columns=_col)
print("now df\n",_df)
_df_cpy = copy(_df)
print("_df id=",id(_df))
print("_df_cpy id=",id(_df_cpy))
random.shuffle(_df.values)
print("current df\n",_df)



from numpy import isnan
def fill_na(row):
    if isnan(row["d"]):
        row["d"] = 0
    else:
        row["d"]=1
    return row

from pandas import to_numeric


_df.apply(fill_na,axis=1)

# lgb
import lightgbm as lgb

params = {
    'task': 'train',
    'boosting_type': 'gbdt',  # 设置提升类型
    'objective': 'regression', # 目标函数
    'metric': {'l2', 'auc'},  # 评估函数
    'num_leaves': 31,   # 叶子节点数
    'learning_rate': 0.05,  # 学习速率
    'feature_fraction': 0.9, # 建树的特征选择比例
    'bagging_fraction': 0.8, # 建树的样本采样比例
    'bagging_freq': 5,  # k 意味着每 k 次迭代执行bagging
    'verbose': 1 # <0 显示致命的, =0 显示错误 (警告), >0 显示信息
}

x_train,x_test,y_train,y_test=train_test_split(iris.data,iris.target,test_size=0.4,random_state=0)

#init
bst_init=lgb.Booster(model_file="iris_model.txt")
y_hat=bst_init.predict(x_test,num_iteration=99)
print(y_hat.shape)
from numpy import argmax
pred = [argmax(_p) for _p in y_hat]
print("test samples length={}".format(len(pred)))
accuracy=sum([1 if _p==_r else 0 for _p,_r in zip(pred,y_test)])/len(pred)
print("accuracy= %.2f%%" %(accuracy*100))

x_input,x_dev,y_input,y_dev=train_test_split(x_train,y_train,test_size=0.1,random_state=0)