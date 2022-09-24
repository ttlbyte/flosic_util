#!/usr/bin/env python3

import numpy as np
import sys
import os
import h5py

from find_cub import find_cub_by_shell

a2b = 1.8897259886
a2b3 = a2b**3

class CHD():
    def __init__(self):
        # This simply allocates the different data structures we need, all units are atomic:
        self.natoms = 0                                           #Number of atoms
        self.org = np.array([0,0,0])                              #Orginal coordinates
        self.pos = np.array([])                                   #Elements data and Postions of atoms
        self.grid = np.zeros(0, dtype=np.float32)                 #Grid data, with dtype set to float32 to save space
        self.v = np.zeros([3, 3])                                 #Increment in 3 directions
        self.N = np.array([0, 0, 0])                              #Number of points in each direction
        self.dV = 0                                               #Volumn of each grid point
        self.tot = 0                                              #Total density

    def set_dV(self):
        # The charge density is stored per volume. If we want to integrate the charge density
        # we need to know the size of the differential volume
        self.dV = 0
        x = self.v[:, 0]
        y = self.v[:, 1]
        z = self.v[:, 2]
        print(x, y, z)
        self.dV = np.dot(x, np.cross(y, z))

    def save(self):
#        np.savez("grid", self.natoms,self.org, self.pos, self.grid, self.v, self.N, self.dV, self.tot)  # Use HDF5 for better interoperability
        with h5py.File('cube.h5', 'w') as hf:
            hf.create_dataset("natoms", data=self.natoms)
            hf.create_dataset("org", data=self.org)
            hf.create_dataset("pos", data=self.pos)
            hf.create_dataset("grid", data=self.grid.astype(np.float32))
            hf.create_dataset("v", data=self.v)
            hf.create_dataset("N", data=self.N)
            hf.create_dataset("dV", data=self.dV)
            hf.create_dataset("tot", data=self.tot)

    def read_h5(self, filename='cube.h5'):
#        data = np.load(filename)
#        self.natoms = data['arr_0']
#        self.org = data['arr_1']
#        self.pos = data['arr_2']
#        self.grid = data['arr_3']
#        self.v = data['arr_4']
#        self.N = data['arr_5']
#        self.dV = data['arr_6']
#        self.tot = data['arr_7']
        with h5py.File('cube.h5', 'r') as hf:
            self.natoms = hf['natoms'][()]
            self.org = hf['org'][:]
            self.pos = hf['pos'][:]
            self.grid = hf['grid'][:].astype(float)
# convert grid data to float64 for higher accuracy
#            self.grid = self.grid.astype(np.float64)
            self.v = hf['v'][:]
            self.N = hf['N'][()]
            self.dV = hf['dV'][()]
            self.tot = round(hf['tot'][()])
            self.grid = self.grid*self.tot/(np.sum(self.grid)*self.dV)
    def write_cube(self):
# The grid data by default are in float32 which has about 7 decimal accuracy. To use more than .8e, one should set grid data to float64.
        f = open('dens.cube', 'w')
# denormalize the grid data
        self.grid = self.grid*self.tot/round(self.tot)
        f.write("Cube file converted from HDF5 wroten by Shiqi\n Use it at your own rish\n")
        f.write("{}   {}  {}  {}\n".format(self.natoms, self.org[0], self.org[1], self.org[2]))
        for i in range(3):
            f.write("{:3d}   {:.8f}   {:.8f}   {:.8f}\n".format(self.N[i], self.v[i][0], self.v[i][1], self.v[i][2]))
        for i in range(self.natoms):
            f.write("{:3d}   {:.8f}     {:.8f}     {:.8f}    {:.8f}\n".format(int(self.pos[i][0]), self.pos[i][1],self.pos[i][2],self.pos[i][3],self.pos[i][4]))
        for i in range(len(self.grid)//6):
            f.write("{:.8e}   {:.8e}   {:.8e}   {:.8e}   {:.8e}   {:.8e}\n".format(self.grid[6*i], self.grid[6*i+1], self.grid[6*i+2], self.grid[6*i+3], self.grid[6*i+4], self.grid[6*i+5]))
        for i in range(len(self.grid)%6,0,-1):
            f.write("{:.8e}   ".format(self.grid[-i]))

def read(cubefile):
    density = CHD()
    convert = False
    f = open(cubefile, 'r')
    next(f)
    line=next(f)
# the flag is used to detect cube file generated by flosic
    if "ANG" in line:
        convert = True
    line = next(f)
    density.natoms = int(line.split()[0])
    density.org = np.array([float(line.split()[1]), float(line.split()[2]), float(line.split()[3])])
    for i in range(0, 3):
        line = next(f).split()
        density.N[i] = int(line[0])
        for j in range(1, 4):
            density.v[i][j-1] = float(line[j])

    density.pos = np.zeros((density.natoms,5))
    for i in range(0, density.natoms):
        line = next(f).split()
        if not convert:
            density.pos[i] = np.array([ float(line[0]), float(line[1]), float(line[2]), float(line[3]), float(line[4])])
        else:
            density.pos[i] = np.array([ float(line[0]), float(line[1]), a2b*float(line[2]), a2b*float(line[3]), a2b*float(line[4])])
# if detected flosic cube, convert the unit to bohr
#    if convert:
#        density.org *= a2b
#        density.v *= a2b
    density.set_dV()
    density.grid = np.zeros([density.N[0]*density.N[1]*density.N[2]])

    # This reads the data into a 1D array of size nx*ny*nz
    count = 0
    for i in f:
        for j in i.split():
            density.grid[count] = float(j)
            count += 1
    f.close()

    density.tot = np.sum(density.grid)*density.dV
    #Normalize the number of electron to the closest integer
#This handles units mismatch between headers and grid data.
    if density.tot < 0.5*sum(density.pos)[0]:
        density.tot *= a2b3
        density.grid *= a2b3

    density.grid = density.grid*round(density.tot)/density.tot
#   uncomment the following line if you want store the density in 3-d array
#    density.grid = density.grid.reshape(density.N[0], density.N[1], density.N[2])
    return density


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Incorrect number of arguments, run as ./inte_cube.py CUBEFILELOCATION/HDFFILE")
        sys.exit(6)
    if 'cube.h5' not in os.listdir('.'):
        density = read(sys.argv[1])
        density.save()
    else:
        density = CHD()
        density.read_h5()
    print(density.tot)
#    density.write_cube()
    if len(sys.argv) == 3:
        ini=0
        fin=int(sys.argv[2])
        n = fin
    elif len(sys.argv)>3:
        ini=int(sys.argv[2])
        fin=int(sys.argv[3])
        n=int(sys.argv[-1])
        masks = os.listdir('/home/tuh14623/scratch/mask/' + str(n-1))
        for i in range(ini,fin):
            if str(i)+'.npz' in masks:
                mask =np.load('/home/tuh14623/scratch/mask/' + str(n-1) +'/' + str(i)+'.npz')['arr_0']
            else:
                mask = find_cub_by_shell(i, n-1)
            print("{}   {}".format(i,np.sum(density.grid, where=mask)*density.dV))
