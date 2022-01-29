# !/usr/bin/python
# coding=utf-8

from __future__ import print_function,division
import sys
import os
import time
import pickle
import codecs
import jieba
import numpy as np
from jieba.analyse import extract_tags
# from utils import save_pickle,load_pickle
from common_utils import clean

# from gensim.models.keyedvectors import KeyedVectors
# from src_file import SrcFiles



#jieba.load_userdict("")
#jieba.analyse.set_idf_path(os.path.join("file","idf_info.txt"))
if sys.getdefaultencoding() != "utf-8":
    reload(sys)
    sys.setdefaultencoding("utf-8")

cur_dir = os.getcwd()
random_ans = [u"不知道你在说什么",u"请重复下你的问题",u"就这样吧"]
topic = [u"最近NBA又发生重大交易了",u"传奇人物金庸老先生去世了，你喜欢看他的小说吗？"]


def read_douban(file,filter_ls,trg_fpath,trie={},with_weight=False):
    t0 = time.time()

    jieba.analyse.set_idf_path(os.path.join("file", "douban_idf"))
    ans_res = {}
    with codecs.open(file,'r',encoding="utf-8") as fr:
        for line in fr.readlines():
            line = line.strip().rstrip('\r\n')
            items = line.split("\t")
            if int(items[0]) == 1:
                end_flag = False
                for id,item in enumerate(items[1:-1]):
                    q_keywords = extract_tags(item.replace(" ",""),topK=3,allowPOS=("n","vn","nt","nz","nrt"),withWeight=True)
                    keyword_tuple = tuple([word for word,_ in q_keywords])
                    filter_flag = False
                    for filter_word in filter_ls:
                        if filter_word.strip("\r\n") in items[id + 2]:
                            # trie[word].append(line.replace('m',"").replace('\t',"").strip())
                            filter_flag = True
                            break
                    if not filter_flag:
                        if not ans_res.has_key(keyword_tuple):
                            ans_res[keyword_tuple] = []
                        ans_res[keyword_tuple].append(items[id+2].replace(" ",""))
                        for word,weight in q_keywords:
                            if not with_weight:
                                if not trie.has_key(word):
                                    trie[word] = []
                                trie[word].append(items[id+2].replace(" ",""))
                            else:
                                if not trie.has_key(word):
                                    trie[word] = {}
                                trie[word].update({items[id+2].replace(" ",""):weight})
    if not with_weight:
        save_pickle(trie, os.path.join(trg_fpath, "douban_trie.pkl"))
    else:
        save_pickle(trie, os.path.join(trg_fpath, "weight_douban_trie.pkl"))
    save_pickle(ans_res, os.path.join(trg_fpath, "match_douban_trie.pkl"))
    t1 = time.time()
    print("gen trie of douban cost time:%.2f(min)" %((t1-t0)/60))
    #return trie

def read_xiaohuangji(file,filter_ls,trg_fpath,trie={},with_weight=False):
    t0 = time.time()
    user_flag = False
    jieba.analyse.set_idf_path(os.path.join("file", "xhj_idf"))
    #user_keywords = []
    #xhj_no_filter = {}
    with codecs.open(file,'r',encoding="utf-8") as fr:
        for line in fr.readlines():
            line = line.strip().rstrip('\r\n').lower()
            #print("line type:", type(line))
            if line.startswith("e"):
                user_flag = True
                continue
            if line.startswith("m") and user_flag:
                user_keywords = extract_tags(line,topK=1,allowPOS=("n","vn","nt","nz","nrt"),withWeight=True)
                user_flag = False
                continue
            if not user_flag:
                filter_flag = False
                for filter_word in filter_ls:
                    if filter_word.strip("\r\n") in line:
                        # trie[word].append(line.replace('m',"").replace('\t',"").strip())
                        filter_flag = True
                        break
                if not filter_flag:
                    for word,weight in user_keywords:
                        if not with_weight:
                            if not trie.has_key(word):
                                trie[word] = []
                            response = line.replace('m', "").replace('\t', "").strip()
                            if u"小通" not in response:
                                trie[word].append(response)
                        else:
                            if not trie.has_key(word):
                                trie[word] = {}
                            key = line.replace('m', "").replace('\t', "").strip()
                            if u"小通" not in key:
                                trie[word].update({key:weight})

    if with_weight:
        save_pickle(trie, os.path.join(trg_fpath, "weight_xhj_trie.pkl"))
    else:
        save_pickle(trie, os.path.join(trg_fpath, "xhj_trie.pkl"))
    t1 = time.time()
    print("gen trie of xiaohuangji cost time:%.2f(min)" %((t1-t0)/60))
    #return trie

def read_qingyun(file,filter_ls,trg_fpath,trie={},with_weight=False):
    t0 = time.time()
    jieba.analyse.set_idf_path(os.path.join("file", "qingyun_idf"))
    with codecs.open(file,'r',encoding="utf-8") as fr:
        for line in fr.readlines():
            #print("line type:",type(line))
            line = line.strip().rstrip("\r\n")
            line = clean(line)
            items = line.split("|")
            if len(items) > 1:
                keywords_ask = extract_tags(items[0],topK=1,allowPOS=("n","vn","nt","nz","nrt"),withWeight=True)
                filter_flag = False
                for filter_word in filter_ls:
                    if filter_word.strip("\r\n") in items[1]:
                        filter_flag = True
                        break
                if not filter_flag:
                    for word,weight in keywords_ask:
                        if not with_weight:
                            if trie.has_key(word):
                                trie[word] = []
                            if u"菲菲" not in items[1]:
                                trie[word].append(items[1])
                        else:
                            if not trie.has_key(word):
                                trie[word] = {}
                            if u"菲菲" not in items[1]:
                                trie[word].update({items[1]:weight})

    if with_weight:
        save_pickle(trie,os.path.join(trg_fpath,"weight_qingyun_trie.pkl"))
    else:
        save_pickle(trie, os.path.join(trg_fpath, "qingyun_trie.pkl"))
    t1 = time.time()
    print("gen trie of qingyun cost time:%.2f(min)" %((t1-t0)/60))
    #return trie


def douban_classify_files(path,filter_ls,trg_path,trie={},with_weight=True):
    t0 = time.time()
    files = os.listdir(path)
    if not files:
        raise ValueError("file can't find please check the path")
    for file in files:
        if file.endswith("txt"):
            class_name = os.path.basename(file).split(".")[0]
            if not type(class_name) == unicode:
                class_name = class_name.decode("utf-8")
            if not trie.has_key(class_name):
                trie[class_name] = {}
                with codecs.open(os.path.join(path,file),'r',encoding="utf-8") as fr:
                    for line in fr.readlines():
                        line = line.rstrip("\r\n")
                        items = line.split("\t")
                        if int(items[0]) == 1:
                            for id,item in enumerate(items[1:-1]):
                                words = extract_tags(item,topK=3,allowPOS=("n","vn","nt","nz","nrt"),withWeight=True)
                                filter_flag = False
                                for filter_word in filter_ls:
                                    if filter_word.strip("\r\n") in items[id + 1]:
                                        # xhj_trie[word].append(line.replace('m',"").replace('\t',"").strip())
                                        filter_flag = True
                                        break
                                if not filter_flag:
                                    for word,weight in words:
                                        if not with_weight:
                                            if not trie[class_name].has_key(word):
                                                trie[class_name][word] = []
                                            trie[class_name][word].append(items[id + 1].replace(" ", ""))
                                        else:
                                            if not trie[class_name].has_key(word):
                                                trie[class_name][word] = {}
                                            trie[class_name][word].update({items[id + 1].replace(" ", ""): weight})
    t1 = time.time()
    print("gen trie of douban cost time:%.2f(min)" %((t1-t0)/60))
    save_pickle(trie,os.path.join(trg_path,"douban_classify.pkl"))
    return trie

def trie_gen(trg_fpath,funcs,filter_ls,with_weight=False):
    t0 = time.time()
    if not os.path.exists(trg_fpath):
        os.mkdir(trg_fpath)
    for func in funcs:
        if hasattr(func,"__name__"):
            #file_suffix = str(func.__name__).split("_")[-1]
            #idf_file = os.path.join(trg_fpath,(file_suffix + "_trie"))
            func(funcs[func],filter_ls,trg_fpath,trie={},with_weight=with_weight)
        else:
            raise ValueError("no suit func input")
    t1 = time.time()
    print("generate all idfs cost time:%.2f(s)" %(t1-t0))

from rules import match_rule,specify_rule,answer_rule
from common_utils import MySimhashComp as MySimhash

def deal_cache(cache,input_timestamp,input_sentence,input_keywords_items,search_scale=30):
    """

    :param cache: store the previou session between
    :param input_timestamp:
    :param input_sentence:
    :param input_keywords_items:
    :param search_scale:
    :return:
    """
    search_upper = input_timestamp - 30
    tmp_dis = 64;pre_match = ""
    if input_keywords_items:
        cur_simhash = MySimhash(input_keywords_items,20,64)
    else:
        raise ValueError("NO ENOUGH INFO FOR COMPUTE SIMHASH VALUE")
    #for time in np.arange(search_upper,input_timestamp):
    for stamp in cache:
        pre_info = cache.get(stamp)
        if pre_info:
            pre_keywords_items = extract_tags(pre_info.replace(" ",""),allowPOS=("n","vn","nt","nz","nrt"),topK=3,withWeight=True)
            if not pre_keywords_items:
                continue
            pre_simhash = MySimhash(pre_keywords_items,20,64)
            dis = cur_simhash.haimingDis(pre_simhash)
            if dis < tmp_dis:
                tmp_dis = dis
                pre_match = pre_info
    cache.update({str(input_timestamp):input_sentence})
    if pre_match:
        answer = answer_rule(input_sentence,pre_match)
        if answer:
            return answer,cache


def choose_answer_from_cache(cache,input_sentence,timestamp):
    input_sentence = clean(input_sentence)
    input_keyword_items = extract_tags(input_sentence.replace(" ",""),allowPOS=("n","vn","nt","nz","nrt"),topK=3,withWeight=True)
    res = deal_cache(cache,timestamp,input_sentence,input_keyword_items)
    if res:
        return res


def choose_output(trie,match_trie,input_sentence,random_ans,classes=None,with_weight=False):
    """

    :param trie:
    :param input_sentence:
    :param random_ans: answers for no choice to output
    :return:
    """


    input_sentence = clean(input_sentence)
    input_keyword_items = extract_tags(input_sentence.replace(" ",""),allowPOS=("n","vn","nt","nz","nrt"),topK=3,withWeight=True)


    #res_candi = {}
    if classes and (not trie.has_key(classes)):
        classes = u"其他"
        for word,weight in input_keyword_items:
            if word in trie[classes]:
                if not with_weight:
                    index_random = np.random.randint(0,len(trie[word]))
                    try:
                        answer = trie[classes][word][index_random]
                    except:
                        answer = trie[classes][word][-1]
                    answer = clean(answer)
                    if type(answer) == unicode:
                        answer = answer.encode("utf-8")
                    return answer
                else:
                    weights = trie[classes][word].values()
                    p_prob = np.array([weight/sum(weights) for weight in weights])
                    answer = np.random.choice(list(trie[classes][word].keys()),avel=p_prob)
                    answer = clean(answer)
                    if type(answer) == unicode:
                        answer = answer.encode("utf-8")
                    return answer
    words_tuple = tuple([word for word,_ in input_keyword_items])
    if match_trie.has_key(words_tuple):
        index_random = np.random.randint(0, len(match_trie[words_tuple]))
        try:
            answer = match_trie[words_tuple][index_random]
        except:
            answer = match_trie[words_tuple][-1]
        print("answer from match pattern...")
        answer = clean(answer)
        return answer

    input_keyword_items = extract_tags(input_sentence.replace(" ", ""), topK=3, withWeight=True)
    for word,weight in input_keyword_items:
        if trie.has_key(word):
            if not with_weight:
                index_random = np.random.randint(0,len(trie[word]))
                try:
                    answer = trie[word][index_random]
                except:
                    answer = trie[word][-1]
                answer = clean(answer)
                if type(answer) == unicode:
                    answer = answer.encode("utf-8")
                return answer
            else:
                weights = trie[word].values()
                p_prob = np.array([weight / sum(weights) for weight in weights])
                #print(u"trie[word] key 0:",trie[word].keys()[0])
                answer = np.random.choice(trie[word].keys(), p=p_prob.ravel())
                answer = clean(answer)
                if type(answer) == unicode:
                    answer = answer.encode("utf-8")
                return answer
    if isinstance(random_ans,list):
        weight_ini = 1 / len(random_ans)
        prob = np.array([weight_ini]*len(random_ans))
        res_choice = np.random.choice(random_ans,p=prob.ravel())
    elif isinstance(random_ans,dict):
        print("please choose a topic")
        topic = raw_input("topic:")
        if topic in random_ans:
            weight_ini = 1 / len(random_ans[topic])
            prob = np.array([weight_ini] * len(random_ans[topic]))
            res_choice = np.random.choice(random_ans[topic], p=prob.ravel())
    print("choose answer from answers lib")
    if type(res_choice) == unicode:
        res_choice = res_choice.encode("utf-8")
    return res_choice

def combine_trie(trie_path,with_weight=False,combine_weight=False):
    t0 = time.time()
    trie = {}
    for file in os.listdir(trie_path):
        items = file.split(".")
        if items[0].endswith("trie") and (not items[0].startswith("match")) and ("combine" not in items[0]):
            temp_trie = load_pickle(os.path.join(trie_path,file))
            for word in temp_trie:
                if not trie.has_key(word):
                    trie[word] = []
                if (not with_weight) and (not combine_weight):
                    trie[word].extend(temp_trie[word])
                elif (not with_weight) and combine_weight:
                    trie[word] = {}
                    for sentence in temp_trie[word]:
                        if file.split(".")[0].startswith("xhj"):
                            trie[word].update({sentence:0.3})
                        elif file.split(".")[0].startswith("qingyun"):
                            trie[word].update({sentence:0.3})
                        else:
                            trie[word].update({sentence:0.4})
                elif with_weight and (not combine_weight):
                    trie[word] = {}
                    for key in temp_trie[word]:
                        weight = temp_trie[word][key]
                        trie[word].update({key:weight/3})
                else:
                    trie[word] ={}
                    for key in temp_trie[word]:
                        weight = temp_trie[word][key]
                        if file.split(".")[0].startswith("xhj"):
                            trie[word].update({key:0.3*weight})
                        elif file.split(".")[0].startswith("qingyun"):
                            trie[word].update({key:0.3*weight})
                        else:
                            trie[word].update({key:0.4*weight})
    if not with_weight:
        save_pickle(trie,os.path.join(trie_path,"combine_trie.pkl"))
    else:
        save_pickle(trie,os.path.join(trie_path, "weight_combine_trie.pkl"))
    t1 = time.time()
    print("combine trie cost time:%.2f(min)" %((t1-t0)/60))
    #return trie

def main(trie_type,with_weight=False):
    t0 = time.time()
    match_trie = load_pickle(os.path.join("trie_file","match_douban_trie.pkl"))
    if trie_type in ["xhj","qingyun","douban"]:
        if not with_weight:
            trie = load_pickle(os.path.join("trie_file",trie_type + "_trie.pkl"))
        else:
            trie = load_pickle(os.path.join("trie_file", "weight_" + trie_type + "_trie.pkl"))
    else:
        if not with_weight:
            trie = load_pickle(os.path.join("trie_file","combine_trie.pkl"))
        else:
            trie = load_pickle(os.path.join("trie_file", "weight_combine_trie.pkl"))
    t1 = time.time()
    print("load  %s trie cost time: %.f(s)" %(trie_type,(t1-t0)))

    while True:
        try:
            input_sentence = raw_input("user:")
            t_q = time.time()
            cache.set_user(t_q,input_sentence)
            result = choose_output(trie,match_trie,input_sentence,random_ans,with_weight=True)
            t_a = time.time()
            print("chatbot: %s" %result)
        except (KeyboardInterrupt,SystemExit,EOFError,RuntimeError):
            break
import redis
from utils import RedisCache
client = redis.StrictRedis()
cache = RedisCache(client)

if __name__ == '__main__':
    file = u"D:\\jwh\\machine2person\\语料\\raw_chat_corpus\\douban-multiturn-100w\\train.txt"
    filter_ls = [word.strip("\r\n") for word in codecs.open(SrcFiles.ming_gan_words, 'r', encoding="utf-8")]
    # with codecs.open(file,'r',encoding="utf-8") as fr:
    #     for count,line in enumerate(fr.readlines()):
    #         if count >3:
    #             break
    #         print("%d hang info: %s" %(count,line))
    #         line = line.replace(" ","")
    #         print("%d hang new info: %s" %(count,line))
    #         diag_info = line.split("\t")
    #         print('%d hang tab diag: %s' %(count,diag_info))
    # time_s = time.time()
    # # res_trie = read_douban(file)
    # # save_pickle(res_trie,"file\\trie.pkl")
    # pickle_exist = os.path.join("file","trie.pkl")
    # if os.path.exists(pickle_exist):
    #     res_trie = load_pickle(pickle_exist)
    #
    # t0 = time.time()
    # funcs = {read_douban:SrcFiles.src_file_douban,read_qingyun:SrcFiles.src_file_qingyun,read_xiaohuangji:SrcFiles.src_file_xhj}
    # #trie_gen("trie_file",funcs,SrcFiles.ming_gan_words,with_weight=True)
    # print("begain compute douban trie with weight...")
    # if not os.path.exists("trie_file"):
    #     os.mkdir("trie_file")
    # read_douban(SrcFiles.src_file_douban,SrcFiles.ming_gan_words,"trie_file",trie={},with_weight=True)
    # #173.56(min)
    # # print("begain compute qingyun trie with weight...")
    # # read_qingyun(SrcFiles.src_file_qingyun,SrcFiles.ming_gan_words,"trie_file",trie={},with_weight=True)
    # # #1.57
    # # print("begain compute xhj trie with weight...")
    # # read_xiaohuangji(SrcFiles.src_file_xhj,SrcFiles.ming_gan_words,"trie_file",trie={},with_weight=True)
    # #5.66
    # print("begain compute the combine trie with weight...")
    # combine_trie("trie_file",with_weight=True,combine_weight=True)
    # print("begain check the input from combine...")
    # main("combine",with_weight=True)
    # xhj_file = u"D:\\jwh\\machine2person\\语料\\raw_chat_corpus\\xiaohuangji-40w\\xiaohuangji50w_nofenci.conv"
    # xhj_trie = read_xiaohuangji(xhj_file,filter_file)
    # t1 = time.time()
    # print("xhj_trie len={} and read cost time:{}(s)".format(len(xhj_trie),(t1-t0)))
    # save_pickle(xhj_trie,os.path.join("file","xhj_trie.pkl"))
    #
    # # print("xhj no filter:{}".format(xhj_no_filter))
    # # save_pickle(xhj_no_filter,os.path.join("file","xhj_no_filter.pkl"))
    #
    # t0 = time.time()
    # qingyun_file = u"D:\\jwh\\machine2person\\语料\\raw_chat_corpus\\qingyun-11w\\12万对话语料青云库.csv"
    # qy_trie = read_qingyun(qingyun_file,filter_file)
    # t1 = time.time()
    # print("qingyun_trie len={} and read cost time:{}(s)".format(len(qy_trie),(t1-t0)))
    # save_pickle(qy_trie,os.path.join("file","qy_trie.pkl"))


    # classify_trie = douban_classify_files(os.path.join(cur_dir,"corpus"))
    # save_pickle(classify_trie,os.path.join(cur_dir,"file","classify_trie.pkl"))
    # time_s1 = time.time()
    # print("load trie cost time: %.2f(s)" %(time_s1-time_s))
    #
    # trie = {}
    # for file in os.listdir("trie_file"):
    #     if file.endswith("pkl"):
    #         temp_trie = load_pickle(os.path.join("file",file))
    #         trie.update(temp_trie)
    #
    # t0 = time.time()
    # xhj_trie = load_pickle(os.path.join("file","xhj_trie.pkl"))
    # qy_trie = load_pickle(os.path.join("file","qy_trie.pkl"))
    # douban_trie = load_pickle(os.path.join("file","trie.pkl"))
    # trie = {}
    # trie.update(douban_trie)
    # trie.update(qy_trie)
    # trie.update(xhj_trie)
    # t1 = time.time()
    # print("load trie and update cost time: %.f(s)" %(t1-t0))
    cache = {}
    while True:
        try:
            input_sentence = raw_input("user:")
            t_q = time.time()
            #result = choose_output(trie,input_sentence,random_ans)
            # try:
            result,cache = choose_answer_from_cache(cache,input_sentence,t_q)
            # except:
            #     result = ""
            #     cache.update({str(t_q):input_sentence})
            t_a = time.time()
            print("chatbot: %s" %result)
        except (KeyboardInterrupt,SystemExit,EOFError,RuntimeError):
            break
        time_check = time.time()
        check_delta = time_check - t_a
        if check_delta >= 3:
            random_index = np.random.randint(len(topic))
            choose_topic = topic[random_index]
            print("chatbot:让我们聊聊其他热门的话题吧—",choose_topic)




