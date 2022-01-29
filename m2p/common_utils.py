# !/usr/bin/python
# coding=utf-8

import logging
import re

def clean(text):
    if not type(text) == unicode:
        text = text.decode("utf-8")
    text = full_to_half(text)
    text = re.sub(u"^[^\u4E00-\u9FA5]+","",text)
    text = re.sub(u"\{[^\u4E00-\u9FA5]*\}","",text)
    text = re.sub(u"\[[^\u4E00-\u9FA5]*\]","",text)
    text = re.sub(u"\([^\u4E00-\u9FA5]{1,2}","",text)
    text = re.sub(u"[^\u4E00-\u9FA5]{1,2}\)","",text)
    text = re.sub(u"[^\u4E00-\u9FA5]+$","",text)
    pattern_rep = re.compile(ur"([^\u4E00-\u9FA5])(\1+)")
    text = re.sub(pattern_rep,ur'\1',text)
    return text

def full_to_half(s):
    """
    Convert full-width character to half-width one
    """
    n = []
    for char in s:
        num = ord(char)
        #0x3000表示中文的全角空格符,是unicode的16进制表示(0x开头,8进制一般以0开头),对应的十进制是12288,32是英文半角空格的ascii(0-255),也是十进制的unicode值,通过chr还原成字符
        if num == 0x3000:
            num = 32
        #0xFF01,0xFF5E分别是中文字符信息'！','～'
        elif 0xFF01 <= num <= 0xFF5E:
            num -= 0xfee0
        char = unichr(num)  #python3 直接使用chr
        n.append(char)
    return ''.join(n)

def half_to_full(s):
    """
    convert half-width charater to ful
    :param s:
    :return:
    """
    n = []
    for char in s:
        num = ord(char)
        if num == 32:
            num = 0x3000
        elif 0x21 < num < 0x7E:
            num += 0xfee0
        char = unichr(num)
        n.append(char)
    return ''.join(n)


def get_logger(log_file):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.DEBUG)
    sh = logging.StreamHandler()
    sh.setLevel(logging.INFO)
    formater = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    sh.setFormatter(formater)
    fh.setFormatter(formater)
    logger.addHandler(sh)
    logger.addHandler(fh)
    return logger

from numpy import array
# className don't be the same with fileName at best
class MySimhashComp:
    def __init__(self, tokens, kaggle, habbits):
        self.tokens = tokens
        self.kaggle = kaggle
        self.habbits = habbits
        self.simhash = self.simhash()

    def __str__(self):
        return str(self.hash)

    def simhash(self):
        """
            @description: compute the simhash value with the result of tokenize
            @params:
            @params:
            @params:
            @return: string: simhash value
        """
        hash_arr = []
        for feature, weight in self.tokens:
            # print "权重信息",weight
            weight = int(self.kaggle * weight)
            hash = self.strhash(feature)
            if len(hash) < 64:
                print "no hash value"
                continue
            try:
                new_hash = [None for x in range(len(hash))]
                for i in range(len(hash)):
                    if hash[i] == "1":
                        new_hash[i] = weight
                    else:
                        new_hash[i] = -weight
            except Exception as e:
                print e.message
            hash_arr.append(new_hash)
        # print hash_arr
        sum_hash = list(array(hash_arr).sum(axis=0))
        # print "特征合并后的hash结果："
        # print sum_hash
        if not sum_hash:
            return "00"
        simhashValue = ""
        for x in sum_hash:
            if x > 0:
                simhashValue += '1'
            else:
                simhashValue += '0'
        # print "simhash值：%s" %simhashValue
        return simhashValue

    def strhash(self, source):

        if not type(source) == unicode:
            source = source.decode('utf-8')

        if source == "":
            return "00"
        else:
            x = ord(source[0]) << 7
            mask = 1000003
            m = 2 ** self.habbits - 1
            for c in source:
                # print "unicode字节c的16进制形式:%s" % c.encode('utf-8')
                x = ((x * mask) ^ ord(c)) & m
            x ^= len(source)
            if x == -1:
                x = -2
            x = bin(x).replace("0b", "").zfill(self.habbits)[-self.habbits:]
            # print "原生输入和当前转化后的结果：(%s,%s)" % (source.encode("utf-8"), x)
            return str(x)

    def haimingDis(self, other):
        """
            @description: compute the haiming distance between two simhash value
            @params:    two simhash value between this and that
            @params:
            @params:
            @return:    int:haimingdistance
        """
        """
        this = self.simhash
        that = other.simhash
        distance = 0
        for i in range(len(this)):
            if this[i] != that[i]:
                distance += 1
            else:
                distance += 0
        return distance
        """
        this = "0b" + self.simhash
        that = "0b" + other.simhash
        # print "对比两片文档simhash的结果："
        # print this
        # print that
        n = int(this,2) ^ int(that,2) #转化为10进制进行异或计算
        # print "二进制取异或后的结果：%s" %n
        distance = 0
        while n:
            n &= (n-1)
            distance += 1
        return distance

    def distance2Score(self,distance,num):
        """
            @description: compute the score according to the distance and
                        reference the yuzhi define the is similarity , yuzhi: distance=3,score=61/64*100
            @params:  distance from the haimingDistance
            @params:
            @params:
            @return: yuzhi,score, similarity
        """
        yuzhi = round((float(self.habbits - num)/self.habbits)*100,2)
        isSim = ""
        if distance>64:
            score = round(float(0),2)
        else:
            score = round((float(self.habbits - distance)/self.habbits)*100,2)
        if score >= yuzhi:
            isSim = "YES"
        else:
            isSim = "NO"
        return yuzhi,score,isSim

import string
import jieba.posseg as psg
def extract_proc(input_sentence):
    
    zhuyu_flag = False;
    symbols = string.punctuation;
    tmp_proc = []
    count = 0;
    symbols_pos = 0;
    weiyu_flag = False
    tokens = psg.cut(input_sentence, HMM=True)
    for word, flag in tokens:
        count += 1
        if flag in ('n', 'nr', 'r', 'nz', 'nt', 'ns'):
            zhuyu_flag = True
            zhuyu_pos = count
            tmp_zhuyu = word
        if word in symbols:
            symbols_pos = count
        if zhuyu_flag and (symbols_pos < zhuyu_pos):
            if flag in ("v", "vn"):
                weiyu_pos = count
                tmp_weiyu = word
                weiyu_flag = True
                tmp_proc = [tmp_zhuyu, tmp_weiyu]
                zhuyu_flag = False
        if word in symbols:
            symbols_pos = count
        if weiyu_flag and (symbols_pos < weiyu_pos):
            if flag in ("n", 'nr', 'r', 'nz', 'nt', 'ns'):
                tmp_proc.append(word)
                break
    return tmp_proc

#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   common_utils.py
@Time    :   2019/06/22 08:38:31
@Author  :   Jin Weihua 
@Version :   1.0
@Contact :   jwhV587@gmail.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA
@Desc    :   None
'''

# here put the import lib


# new add function 
def _moving_average(nums:list, windows=2):
    average_ls = []
    if windows >= 2:
        if len(nums) < windows:
            raise ValueError("data nums too short ")
        i = 0
        while i < (len(nums)-1):
            average_ls.append((nums[i]+nums[i+1])/2)
            i += 1
    elif windows == 1:
        average_ls = nums.copy()
    else:
        raise ValueError("windows can't be less than 1")
    return average_ls

def _exp_moving_average(nums,beta=0.3):
    if beta > 1 or beta <0:
        raise ValueError("beta value is not suitable")
    if not nums:
        raise ValueError("null list")
    theta = 0.0
    thetas = []
    i = 0
    while i < len(nums):
        theta = beta*theta + (1-beta)*nums[i]
        thetas.append(theta)
        i += 1 
    return thetas

    