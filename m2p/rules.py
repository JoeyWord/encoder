# !/usr/bin/python
# coding=utf-8

import re
import jieba.posseg as psg
import random

can_lib = {u"段子":u"这都不知道，好尴尬啊",u"笑话":u"小样，你以为脱掉马甲我就不认识你了",u"绕口令":u"吃葡萄不吐葡萄皮，不吃葡萄倒吐葡萄皮"}
host_info = {u"性别":u"女",u"星座":u"双子座",u"兴趣":u"看书"}
chat_info = {u"名字":u"小喵",u"年龄":u"1"}

def specify_rule(inp):
    if not type(inp)== unicode:
        inp = inp.decode("utf-8")

    rule1 = ur"你(猜|知道).*(什么|啥|？|\?|呢|吗)"
    rule2 = ur"你(会|可以|能).*(什么|啥|？|\?|呢|吗)"
    rule3 = ur"你的主人[^\u4e00-\u9f4a]*$"
    rule4 = ur"你的主人((叫|有|是).*)|(.*哪儿的)|(.*哪里人).*?"
    rule5 = ur"我(的*名字)*叫.*?"

    rule6 = ur"你叫(啥|什么)|(多大)|(几岁)|(的?(年[纪龄])|名字)"


    pattern1 = re.compile(rule1)
    pattern2 = re.compile(rule2)
    pattern3 = re.compile(rule3)
    pattern4 = re.compile(rule4)
    pattern5 = re.compile(rule5)
    pattern6 = re.compile(rule6)


    if re.search(pattern1,inp):
        return "ques"
    elif re.search(pattern2,inp):
        return "can"
    elif re.search(pattern3,inp):
        return "host_entry"
    elif re.search(pattern4,inp):
        return "host_info"
    elif re.search(pattern5,inp):
        return "user_info"
    elif re.search(pattern6,inp):
        return "chatbot_info"

    return
def match_rule(inp):
    if not inp:
        return
    if not type(inp)== unicode:
        inp = inp.decode("utf-8")
    items = psg.cut(inp,HMM=True)
    extract_proc = []
    verb_flag = False
    for word,pos in items:
        if pos == "v":
            verb_flag = True
            tmp_verb = word
        if verb_flag and pos in ("r","nr","nz","nt","nrt","n"):
            extract_proc.append((tmp_verb,word))
            verb_flag = False
    return extract_proc

def answer_rule(inp_cur,inp_pre):
    sufix = u"，嘿嘿";prefix = u"小主，您"
    unknow = u"请原谅我还没来得及知晓。。。"
    answer = u""
    match_pre = match_rule(inp_pre)
    if specify_rule(inp_cur) == "ques":
        if match_pre:
            answer += prefix;match_len = len(match_pre)
            for idx,(verb,obj) in enumerate(match_pre):
                idx = idx + 1
                if idx == match_len:
                    info = verb + obj + sufix
                    answer += info
                else:
                    info = verb + obj + u"，"
                    answer += info
        else:
            answer = unknow
    elif specify_rule(inp_cur) == "can":
        prefix = u"小主，我会"
        unknow = u"哎呀，这个太难了，我还不会，我会好好学的，敬请期待哦，嘻嘻！！"
        topic = list(can_lib.keys())
        try:
            sele_topic = topic[random.randint(len(topic))]
        except:
            sele_topic = topic[-1]
        if sele_topic == u"诗":
            answer = prefix + u"念诗:" + "\r\n" + can_lib[sele_topic]
        elif sele_topic in [u"段子",u"笑话"]:
            answer = prefix + u"讲" + sele_topic + ":\r\n" + can_lib[sele_topic]
        elif sele_topic in u"绕口令":
            answer = prefix + sele_topic + ":\r\n" + can_lib[sele_topic]
        else:
            answer = unknow
    elif specify_rule(inp_cur) == "host_entry":
        answer = u"可以啊，不过我只能告诉你我知道以及我能说的，哈哈"
    elif specify_rule(inp_cur) == "host_info":
        connect_sign = "--";prefix = u"我主人的";sufix = [u",嘻嘻",u",嘿嘿",u",哇咔咔"]
        for word in host_info:
            if word in inp_cur:
                answer = prefix + word + connect_sign + host_info[word] + sufix[random.randint(len(sufix))]
                break
    elif specify_rule(inp_cur) == "chat_info":
        #answer = u"我"
        items = psg.cut(inp_cur,HMM=True)
        count = 0
        items_dict = {count+= 1 for _ in items}
        for idx,(word,flag) in enumerate(items):

            if flag != 'x' or len(word) > 1:
                if flag == 'v':
                    verb_flag = True
                    
                if verb_flag:
                    if word in [u"年纪",u"年龄"]:
                        answer = chat_info[u"年龄"] 
                        return answer + ",很年轻吧，嘻嘻"
                    elif word in [u"名字",u"大名"]:
                        answer = chat_info[u"名字"]
                        return answer + u",名字好听吧，哈哈"
                pos += 1
                if flag == 'r':
                    pos_sub = pos
                    sub_flag = True
                if sub_flag and (flag == 'm'):
                    pos_m = pos
                    sub_flag = False
                    m_flag = True
                    if pos_m > pos_sub and (idx + 1) == count:
                        return chat_info[u"年龄"] + u",没猜到吧！"
                if m_flag and (pos_m > pos_sub) and flag == 'a':
                    pos_a = pos
                    m_flag = False
                    if pos_a > pos_m and (idx + 1) == count:
                        return chat_info[u"年龄"] + u",青春年少对吧"


    return answer




