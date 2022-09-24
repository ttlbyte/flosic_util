#!/usr/bin/env python3
# encoding: utf-8

import numpy as np

n2b = 1.889726
fp = open('XMOL.xyz' , 'r')
xyz = fp.readlines()
fp.close()
fp = open('FRMORB', 'r')
line = fp.readline()
x, y = int(line.split()[0]), int(line.split()[1])
fp.close()
frmorb = np.loadtxt('FRMORB', skiprows=1)
frmorb = frmorb/n2b
with open('output.xyz', 'w') as f:
    f.write("{}\n".format(int(xyz[0])+x+y))
    for i in xyz[1:]:
        f.write(i)
    for i in range(x):
        f.write("{:>2s}  {:10.5f} {:10.5f} {:10.5f}\n".format('He', frmorb[i][0], frmorb[i][1], frmorb[i][2]))
    for i in range(x,x+y):
        f.write("{:>2s}  {:10.5f} {:10.5f} {:10.5f}\n".format('X', frmorb[i][0], frmorb[i][1], frmorb[i][2]))

