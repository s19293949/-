# -*- coding: utf-8 -*-
"""
Created on Wed Oct 10 10:47:24 2018

@author: Administrator
"""
import re
import pandas as pd
import jieba
import jieba.analyse
import jieba.posseg as pseg
from gensim import corpora,models,similarities
from snownlp import SnowNLP
from snownlp import sentiment

sentiment.load('D:\\anaconda\\anaconda\\pkgs\\snownlp-0.12.3\\snownlp\\sentiment\\sentiment.marshal')
jieba.load_userdict('D:\\anaconda\\anaconda\\pkgs\\jieba-0.39\\jieba\\jbj.txt')
#发现某类特征
def discover_feature(data,*text):
    key_list = []
    for key in data:
        #句子根据标点符号分句
        keys = re.split('[，～。！？、,. ]',key)
        for i in keys:
            for keyword in text:
                if keyword in i:
                    try:
                        #re匹配关键词之后的字段
                        match=re.compile(r"(?<=%s).+" %keyword).search(i)
                        words = match.group()
                        words = pseg.cut(words)
                        for word, flag in words:
                            #匹配修饰词
                            if 'a' in flag  or flag == 'vd' or flag == 'l' or flag == 'z' :
                                word1 = keyword+str(word)
                                key_list.append(word1)
                                break
                    except AttributeError:
                        pass
                    continue
    return key_list



def cut(data):
    data_cut=[]
    for i in range(0,len(data)):
        data_cut.append('/'.join(jieba.cut(data[i])).split('/'))
    return data_cut

def delect(data):
    dictionary=corpora.Dictionary(data)
    corpus=[dictionary.doc2bow(text) for text in data]
    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]        
    #删除包含某些字符的评论数据        
    query = '模板/积分/仙女/淘气值/没用/没有用/積分/繁荣昌盛/复制/送人/年级/京东/网购/模块/闲鱼/领导/阿里巴巴/乾隆/复制粘贴/合格/村/燕窝/七经八脉/凑'
    vec_bow = dictionary.doc2bow(query.split('/'))
    vec_tfidf = tfidf[vec_bow]
        
    index = similarities.MatrixSimilarity(corpus_tfidf)
    sims = index[vec_tfidf]
    sims_list = list(sims)
    c = {'评论':data,'sim':sims_list}
    df = pd.DataFrame(c)
    data1 = df[df.sim==0]
    return data1
def sentiment_mine(sen):
    pos_value = 0
    neg_value = 0
    sentences = '/'.join(jieba.cut(sen)).split('/')
    try:
        for i in sentences:
            if i in pos_list:
                pos_value +=1
            if i in neg_list:
                neg_value +=1
#        print(neg_value)
        if pos_value/neg_value>=1:
                return '好评'
        elif pos_value/neg_value<1:
                return '差评'
    except ZeroDivisionError:
        if pos_value>0:
            return '好评'
        return '其他'
def difference(left,right):
    left_list = left.评价.values.tolist()
    right_list = right.评价.values.tolist()
    final = []
    for i in left_list:
        if i not in right_list:
            final.append(i)
    df_final = pd.DataFrame(final,columns = ['评价'])
    return df_final
def keys_classification(data,*text):
    data_pos = []
    data_neg = []
    data_text = []
    for key in data:
        keys = re.split('[，～。！？、,. ]',key)
        for i in keys:
            for j in text:
                if j in i :
                    result = sentiment_mine(i)
                    if result == '好评':
                        data_pos.append(key)
                    elif result == '差评':
                        data_neg.append(key)
                    elif result == '中评':
                        data_mid.append(key)
                    elif result == '其他':
                        data_text.append(key) 
    df_pos = pd.DataFrame(data_pos,columns = ['评价'])
    df_neg = pd.DataFrame(data_neg,columns = ['评价'])
    senti=[SnowNLP(i).sentiments for i in data_text]
    c={"评价":data_text,"系数":senti}
    df = pd.DataFrame(c)
    df['情感'] = None
    df.loc[df.系数>0.4,'情感'] = '正向'
    df.loc[df.系数<0.4,'情感'] = '负向'
    pl_neg = df[['评价']][df['情感'] == '负向']
    pl_pos = df[['评价']][df['情感'] == '正向']
    
    #整合评论
    df_pos = pd.concat([df_pos,pl_pos])
    df_neg = pd.concat([df_neg,pl_neg])
    #去重
    df_pos = pd.DataFrame.drop_duplicates(df_pos, subset='评价', keep='first', inplace=False)
    df_neg = pd.DataFrame.drop_duplicates(df_neg, subset='评价', keep='first', inplace=False)
    #取差集
    df_neg = difference(df_neg,df_pos)
    return df_pos,df_neg
def sen(data_list):
    senti=[SnowNLP(i).sentiments for i in data_list]
    c={"评价":data_list,"系数":senti}
    df = pd.DataFrame(c)
    df['情感'] = None
    df.loc[df.系数>=0.4,'情感'] = '正向'
    df.loc[df.系数<0.4,'情感'] = '负向'
    pl_qg = df[['评价','情感']]
    pl_neg = df[df.情感 == '负向']
    
    pl_pos = df[df.情感 == '正向']
    return pl_neg,pl_pos



