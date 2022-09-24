#!/usr/bin/env python3
# encoding: utf-8


import os
import getopt
import sys

''' fix 1s FOD for all elements other than H atom. This script finds the closest FOD to each atom and change its coordinates to the atom's.
Usage: python fix1s.py [-i]
-i option for in place modification
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
for i in up:
    tmp = i.split()
    i = "  ".join(tmp[0:3])
for i in dn:
    tmp = i.split()
    i = "  ".join(tmp[0:3])
fp = open('CLUSTER', 'r')
lines = fp.readlines()
fp.close()
num_atoms = int(lines[2].split()[0])
atoms = lines[3:num_atoms+3]
fix_list = []
for i in atoms:
    tmp = i.split()
    if int(tmp[3]) != 1:
        pos = [float(tmp[0]), float(tmp[1]), float(tmp[2])]
        fix_list.append(pos)


def get_dis(pos, fod):
    tmp = [float(i) for i in fod.split()[:3]]
    return((tmp[0]-pos[0])**2 + (tmp[1]-pos[1])**2 + (tmp[2]-pos[2])**2)


# print(fix_list)


def fix(fods, num):
    fixed = []
    for i in fix_list:
        index = -1
        dis = 100
        for j in range(len(fods)):
            tmp = get_dis(i, fods[j])
            if tmp < dis:
                index = j
                dis = tmp
        if dis > 0.0 and dis < 0.001:
            fixed.append(index+num)
    return fixed


optlist, args = getopt.getopt(sys.argv[1:], 'i')
fixed_up = 0
fixed_dn = 0
print(fix(up, 0))
print(fix(dn, len(up)))
