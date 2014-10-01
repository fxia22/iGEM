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
   



cut = [74, 172, 271, 357, 450, 549, 647, 747, 847, 935, 994, 1094, 1192, 1291, 1377, 1470, 1569, 1667,1734 ]
cut.append(0)
cut.sort()
print(cut)

d = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
for seq in gen:
    fullseq = head+seq+rear;
    for k in range(19):
        repeat = fullseq[cut[k]:cut[k+1]+4]
        if not repeat in d[k]:
            d[k].append(repeat)
        #print(repeat)
    repeat = (fullseq[cut[19]:]+'AACG')
    if not repeat in d[19]:
        d[19].append(repeat)
    #print(repeat)

for i in range(20):
    print("sequence #", i)
    print(d[i])
    
