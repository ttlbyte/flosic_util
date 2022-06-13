#!/usr/bin/env python3
# encoding: utf-8

from ase.io import read
import sys
import os

##  Usage: ./cluster_from_xyz.py [filename] [method] [charge] [spin]

n2b=1.889726
if len(sys.argv) > 1:
    atoms=read(sys.argv[1])
else:
    for i in os.listdir():
        if 'xyz' in i:
            atoms = read(i)

if len(sys.argv) >= 3:
    method = argv[2]
else:
    method = "LDA-PW91"
if len(sys.argv) >=5:
    charge = float(sys.argv[3])
    spin = float(sys.argv[4])
else:
    charge = 0.0
    spin = 0.0

with open('CLUSTER', 'w') as f:
    f.write("{}*{}            (DF TYPE EXCHANGE*CORRELATION)\n".format(method,method))
    f.write("NONE                         (TD, OH, IH, X, Y, XY, ... OR GRP)\n")
    f.write("{}\n".format(len(atoms)))
    for i in atoms:
        f.write("{:14.8f}  {:14.8f}  {:14.8f}   {:2d}  ALL (R, Z, ALL-ELECTRON)\n".format((i.position*n2b), i.number))
    f.write("{:.2f} {:.2f}                      (NET CHARGE AND NET SPIN)".format(charge, spin))
