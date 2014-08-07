# -*- coding: utf-8 -*-

import os
import random


def input(filename):
    fin = file(filename,'r')
    seq = ''
    for i in range(0,17):
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

def score(seq,dict,dictU,dictA):
    #coefficient lambda
    usageScore = 0.0
    l =  0.5
    #print seq
    for i in range(0,17*34):
        usageScore+=dictU[seq[i*3:i*3+3]]
    #print usageScore

    repScore = 0.0
    for i in range(0,17):
        for j in range(i+1,17):
            seq1 = seq[i*34*3:(i+1)*34*3]
            seq2 = seq[j*34*3:(j+1)*34*3]
            for k in range(0,34*3):
                if seq1[k] != seq2[k]:
                    repScore += 1
    #print repScore
    score = repScore*l + usageScore*(1-l)
    return score

def mutation(seq,dict,dictA):
    mSeq = seq
    point = random.randint(1,17*34)
    #print point
    while (point % 34 == 12) or (point % 34 == 13):
        point = random.randint(1,17*34)
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
    point = random.randint(1,17*34)
    mSeq1 = seq1[:point*3]+seq2[point*3:]
    mSeq2 = seq2[:point*3]+seq1[point*3:]
    return mSeq1,mSeq2

def selection(gen,dict,dictU,dictA,f):
     scores = []
     for ch in gen:
         scores += [score(ch,dict,dictU,dictA)]
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
     print thr
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
    print dict
    print dictU
    print dictA

    #建立初始种群
    #建立初始种群的策略是对原始的序列进行一个位置的变异
    s = score(orgSeq,dict,dictU,dictA)
    print s
    seq2 = mutation(orgSeq,dict,dictA)
    print score(mutation(orgSeq,dict,dictA),dict,dictU,dictA)
    print score(mutation(seq2,dict,dictA),dict,dictU,dictA)
    out = file("result.csv",'w')
    gen = []
    for i in range(200):
        gen += [mutation(orgSeq,dict,dictA)]
    #print gen
    selection(gen,dict,dictU,dictA,out)
    #print len(gen)

    #交配和变异
  
    for i in range(400):
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

        selection(gen,dict,dictU,dictA,out)
    
    for sequence in gen:
        out.write(sequence+','+str(score(sequence,dict,dictU,dictA))+'\n')
        print sequence
        print score(sequence,dict,dictU,dictA)
    out.close()
    return

if __name__ == "__main__":
   main_run()
