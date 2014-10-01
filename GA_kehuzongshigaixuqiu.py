# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import random
import pickle


def input(filename):
    fin = file(filename,'r')
    seq = ''
    for i in range(0,16):
        seq += fin.readline()[0:-1]
    fin.close()
    return seq
def createCodonDic(filename):
    dict = {}
    fin = file(filename,'r')
    line = fin.readline()
    while line:
        sline = line[0:-1].split(',')
        #print sline
        dict[sline[2]] = sline[0]
        line = fin.readline()
    fin.close()
    return dict

def createEnzymeList(filename):
    lst = [];
    fin = file(filename,'r')
    line = fin.readline()
    while line:
        sline = line[0:-1].split(',')
        #print sline
        lst.append(sline[0])
        line = fin.readline()
    fin.close()
    return lst


def createUsageDic(filename):
    dict = {}
    fin = file(filename,'r')
    line = fin.readline()
    while line:
        sline = line[0:-1].split(',')
        #print sline
        dict[sline[2]] = float(sline[3])
        line = fin.readline()
    fin.close()
    return dict

def createAmoDic(filename):
    dict = {}
    fin = file(filename,'r')
    line = fin.readline()
    while line:
        sline = line[0:-1].split(',')
        #print sline
        key = sline[0];
        if dict.get(key,None) == None:
            dict[key] = [sline[2]]
        else:
            dict[key] += [sline[2]]

        line = fin.readline()
    fin.close()
    return dict

def score(seq,dict,dictU,dictA,listE):
    #coefficient lambda
    usageScore = 0.0
    l =  0.05
    #print seq
    for i in range(0,16*34):
        usg = dictU[seq[i*3:i*3+3]]
        if (usg>0.09):
            usageScore+=usg
        else:
            usageScore-=300
    #print usageScore

    repScore = 0.0
    for i in range(0,16):
        for j in range(i+1,16):
            seq1 = seq[i*34*3:(i+1)*34*3]
            seq2 = seq[j*34*3:(j+1)*34*3]
            for k in range(0,34*3):
                if seq1[k] != seq2[k]:
                    repScore += 1
    #print repScore
    pnt = 0.0
    listE1 = listE[0:6]
    listE2 = listE[6:-1]
    for pattern in listE1:
        if pattern in seq:
            pnt -=300
            
    for pattern in listE2:
        if pattern in seq:
            pnt -=20
            
           # print 'found'
        #    print pattern
            
    
    
    score = repScore*l + usageScore*(1-l)+pnt
    #print('rep:',repScore);
    #print('usg:',usageScore);
    #print('enz:',pnt);
    return score

def mutation(seq,dict,dictA):
    mSeq = seq
    point = random.randint(1,16*34)
    reserved = [92,93,94,95,191,192,193,194,277,278,279,280,370,371,372,373,469,470,471,472,567,568,569,570,667,668,669,670,767,768,769,770,855,856,857,858,914,915,916,917,1014,1015,1016,1017,1112,1113,1114,1115,1211,1212,1213,1214,1297,1298,1299,1300,1390,1391,1392,1393,1489,1490,1491,1492,1587,1588,1589,1590]
    
    #print point
    while (point % 34 == 12) or (point % 34 == 13) or (point*3-3 in reserved) or (point*3-2 in reserved) or ((point*3-1 in reserved)):
        point = random.randint(1,16*34)
        #print point
    #print seq[point*3-3:point*3]
    #print dict[seq[point*3-3:point*3]]
    #print dictA[dict[seq[point*3-3:point*3]]]
    lst = dictA[dict[seq[point*3-3:point*3]]]
    length = len(lst)
    #print length

    sel = random.randint(0,length-1)
    while (lst[sel]==seq[point*3-3:point*3]) and (length>1):
        sel = random.randint(0,length-1)
    #print lst[sel]
    mSeq = seq[:point*3-3] + lst[sel] + seq[point*3:]
    return mSeq

def crossover(seq1,seq2):
    point = random.randint(1,16*34)
    reserved = [92,93,94,95,191,192,193,194,277,278,279,280,370,371,372,373,469,470,471,472,567,568,569,570,667,668,669,670,767,768,769,770,855,856,857,858,914,915,916,917,1014,1015,1016,1017,1112,1113,1114,1115,1211,1212,1213,1214,1297,1298,1299,1300,1390,1391,1392,1393,1489,1490,1491,1492,1587,1588,1589,1590]
    while (point % 34 == 12) or (point % 34 == 13) or (point*3-3 in reserved) or (point*3-2 in reserved) or ((point*3-1 in reserved)):
        point = random.randint(1,16*34)
    mSeq1 = seq1[:point*3]+seq2[point*3:]
    mSeq2 = seq2[:point*3]+seq1[point*3:]
    return mSeq1,mSeq2

def selection(gen,dict,dictU,dictA,listE,f):
     scores = []
     for ch in gen:
         scores += [score(ch,dict,dictU,dictA,listE)]
         #print ch
     #print scores
     scores2 = sorted(scores)
     #print scores2
     h = scores2[1]
     l = scores2[-1]
     su = 0
     for s in scores2:
         su += s
     avg = su/200
     f.write(str(h)+','+str(l)+','+str(avg)+'\n')
     thr = scores2[100]
     print(thr)
     li = 200
     for i in range(200):
         li -= 1
         if scores[li] < thr:
             del gen[li]
     return gen

def main_run():
    #initialize
    orgSeq = input('orgSeqPart.txt')
    aaSeq = 'ltpdqvvaias**ggkqaletvqrllpvlcqdhg'
    #print orgSeq
    dict = createCodonDic('dic.txt')
    dictU = createUsageDic('dic.txt')
    dictA = createAmoDic('dic.txt')
    listE = createEnzymeList('enzyme.txt')
    print(listE)
    print(dict)
    print(dictU)
    print(dictA)

    #建立初始种群
    #建立初始种群的策略是对原始的序列进行一个位置的变异
    s = score(orgSeq,dict,dictU,dictA,listE)
    print(s)
    seq2 = mutation(orgSeq,dict,dictA)
    print(score(mutation(orgSeq,dict,dictA),dict,dictU,dictA,listE))
    print(score(mutation(seq2,dict,dictA),dict,dictU,dictA,listE))
    out = file("result.csv",'w')
    gen = []
    for i in range(200):
        gen += [mutation(orgSeq,dict,dictA)]
    #print gen
    selection(gen,dict,dictU,dictA,listE,out)
    #print len(gen)
    
    #交配和变异
  
    for i in range(600):
        oldgen = gen
        gen = []
        for i in range(100):
            x = random.randint(0,99)
            y = random.randint(0,99)
            while y == x:
                y = random.randint(0,99)
            seq1,seq2 = crossover(oldgen[x],oldgen[y])
            seq1 = mutation(seq1,dict,dictA)
            seq2 = mutation(seq2,dict,dictA)
            gen += [seq1,seq2]

        selection(gen,dict,dictU,dictA,listE,out)
    
        #检查一下:
        reserved = [92,93,94,95,191,192,193,194,277,278,279,280,370,371,372,373,469,470,471,472,567,568,569,570,667,668,669,670,767,768,769,770,855,856,857,858,914,915,916,917,1014,1015,1016,1017,1112,1113,1114,1115,1211,1212,1213,1214,1297,1298,1299,1300,1390,1391,1392,1393,1489,1490,1491,1492,1587,1588,1589,1590]
        rd = random.randint(0,99)
        seq = gen[rd]
        for i in reserved:
            print(seq[i],end = '')
        print('\n')
    
    for sequence in gen:
        out.write(sequence+','+str(score(sequence,dict,dictU,dictA,listE))+'\n')
        print(sequence)
        print(score(sequence,dict,dictU,dictA,listE))
    
    
    with open('objs.pickle', 'w') as f:
        pickle.dump([gen], f)
    
    out.close()
    return

if __name__ == "__main__":
   main_run()
