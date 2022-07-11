#!/usr/bin/env python3
# encoding: utf-8
import numpy as np

'''
find the minimal distances between FODs for both spins to detect any ill-defined FOD.
'''
fp = open('FRMORB', 'r')
lines = fp.readlines()
for i in range(len(lines)):
    lines[i] = lines[i].replace('D', 'E')
fp.close()
head = lines[0]
nums = head.split()
up = lines[1:int(nums[0])+1]
dn = lines[-int(nums[1]):]
he = []
x = []
for i in up:
    tmp = i.split()
    he.append([float(j) for j in tmp[0:3]])
for i in dn:
    tmp = i.split()
    x.append([float(j) for j in tmp[0:3]])

he = np.array(he)
x= np.array(x)
def get_min(fod):
    length = len(fod)
    dis = np.zeros([length,length])
    for i in range(length):
        for j in range(length):
            if i==j:
                dis[i,j] = 100
            else:
                dis[i,j] = np.linalg.norm(fod[i]-fod[j])
    print(np.min(dis))
    print(np.where(dis == np.min(dis)))
get_min(he)
get_min(x)
