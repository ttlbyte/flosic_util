#!/usr/bin/env python3
# encoding: utf-8

import os
import sys

filenames = os.listdir('.')


def check_scf_iter():
    with open('NRLMOL_INPUT.DAT', 'r') as f:
        lines = f.readlines()
    for i in lines:
        if 'MAXSCFV' in i:
            maxiter = int(i.split()[2])
    if 'EVAL{:03d}'.format(maxiter-1) in filenames:
        print('MAXSCFV reached, probably scf not converged')
        sys.exit(-1)


def check_out():
    with open('out', 'r') as f:
        line = f.readlines()[-1]
    if '******' not in line:
        print('Running into error')
        sys.exit(-2)


def check_EVAL():
    try:
        with open('EVALUES', 'r') as f:
            lines = f.readlines()
        for i in lines:
            if 'OCC:' in i:
                if float(i.split()[-1]) < 0.999 and float(i.split()[-1]) > 0.001:
                    print('Fractional occupation detected')
                    print('{} calculation failed.'.format(caltype))
    except:
        print('EVALUES not found')


def read_ene():
    try:
        with open('SUMMARY', 'r') as f:
            line = f.readlines()[-1]
        return(float(line.split()[-2]))
    except:
        print('SUMMARY file not found')
        sys.exit(-5)


def check_frozen_sum():
    with open('SUMMARY', 'r') as f:
        lines = f.readlines()
    if lines[-1].split()[1] != '0.000000000' or lines[-2].split()[1] == '0.000000000':
        print('FOD forces not converged yet')
        sys.exit(6)


def check_fforce():
    try:
        with open('fforce.dat', 'r') as f:
            lines = f.readlines()
            forces = []
            for i in lines:
                a = [float(j)**2 for j in i.split()]
                forces.append(sum(a)**0.5)
            forces.sort()
        return forces
    except:
        print('fforce.dat not found')
        sys.exit(-6)


if 'SYMBOL' not in filenames or 'NRLMOL_INPUT.DAT' not in filenames or 'out' not in filenames:
    print('Error')
    sys.exit(-1)
elif 'FRMORB' not in filenames:
    caltype = 'scf'
elif 'LSIC_SCALE_FAC' in filenames:
    caltype = 'lsic'
elif 'fande.dat' in filenames:
    caltype = 'sic'
elif 'fande.out' in filenames:
    caltype = 'frozen'
else:
    caltype = 'unknown'
    print('Error')
    sys.exit(-3)
check_scf_iter()
ene = read_ene()
if caltype == 'scf' or caltype == 'lsic':
    check_out()
    check_EVAL()
    print('{} calculation finished with Final total energy: {:.8f} Hartree'.format(
        caltype, ene))
else:
    forces = check_fforce()
    if caltype == 'frozen':
        check_frozen_sum()
    print(
        'SIC calculation finished with max FOD force: {:.8f} Hartree/Bohr and final total energy: {:.8f} Hartree'.format(forces[-1], ene))
