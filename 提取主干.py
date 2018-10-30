# -*- coding: utf-8 -*-
"""
Created on Tue Oct 23 17:23:01 2018

@author: Administrator
"""

from stanfordcorenlp import StanfordCoreNLP
 

sentence = '碗有问题'
nlp = StanfordCoreNLP(r'D:\anaconda\anaconda\Lib\site-packages\stanford-corenlp-full-2018-02-27', lang='zh')
print (nlp.word_tokenize(sentence))

print (nlp.dependency_parse(sentence))




sentence = '碗的质量非常好'
#分词
word = nlp.word_tokenize(sentence)
#句法分结构分析
res = nlp.dependency_parse(sentence)
#算法规则
def parese(sentence):
    res = nlp.dependency_parse(sentence)
    text = []
    for i in range(len(res)):
        text.append(res[i][0])
    for i in range(len(res)):
        a = ''
        b = ''
        c = ''
        if 'neg' in text:
            for j in range(len(res)):
                if res[j][0] == 'nsubj':
                    a = res[j][2]
                if res[j][0] == 'neg':
                    b = res[j][2]
                    c = res[j][1]
            break
        if len(res) ==1:
            a = res[i][2]
            name = word[a-1]
            break
        if res[i][0] == 'dep':
            a = res[i][2]
            b = res[i][1]
            j = i+1
            if res[j][0] == 'dobj':
                c= res[j][2]
            else:
                j+=1
            break
        if res[i][0] == 'nsubj':
            a = res[i][2]
            b = res[i][1]
            if 'dobj' in text:
                for j in range(len(res)):
                    if res[j][0] == 'dobj':
                        c = res[j][2]
            break
        if res[i][0] == 'compound:nn':
            if 'nsubj' in text:
                continue
            else:
                a = res[i][2]
                b = res[i][1]
                break
    if c != '':
        name = word[a-1]+word[b-1] +word[c-1]   
    elif b != '' and c == '':
        name = word[a-1]+word[b-1]
    else :
        name = word[a-1]
            
    return name
parese(sentence)