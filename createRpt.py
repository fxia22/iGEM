from __future__ import print_function
import pickle
import sys
from termcolor import colored
from random import randint
with open('objs.pickle') as f:
   gen = pickle.load(f)
   gen = gen[0]

head = 'CTATCGCCAGCAACATTGGCGGCAAGCAAGCGCTCGAAACGGTGCAGCGGCTGTTGCCGGTGCTGTGCCAGGACCATGGC'
rear = 'CTGACCCCGGACCAAGTGGTGGCTATCGCCAGCAACGGTGGCGGCAAGCAAGCGCTCGAAAGCATTGTGGCCCAGCTGAGCCGGCCTGATCCGGCGTTGGCCGCGTTGACC'
   
cutting = 80;
cut = [];
for i in range(18):
    cut.append(cutting + 102*i);
print(cut)    
cut.append(10000)
# randomly create overhang position, and make sure each repeat's length is close 


for j in range(len(gen)):
    overhang = ['CTAT','GACC'];
    fullseq = head+gen[j]+rear;
    #print(fullseq)
    k = 0;
    cut2 = []
    for i in range(len(fullseq)):
        if i == cut[k]:
            temp = 0
            overhang1 = fullseq[i+temp:i+4+temp]
            while overhang1 in overhang:
                temp+=1
                overhang1 = fullseq[i+temp:i+4+temp]
            cut2.append(i+temp)    
            overhang.append(overhang1)
            i = i+4
            k += 1
    cut2.append(10000)
    k = 0
    i = 0
    while (i<len(fullseq)):
        if i == cut2[k]:
            print(colored(fullseq[i:i+4],'red'),end='')
            i += 4
            k = k+1
        else:
            print(fullseq[i],end = '')
            i += 1
    print("")
    print(cut)
    print(cut2)