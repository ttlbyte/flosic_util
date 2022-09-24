#!/usr/bin/env python3
# encoding: utf-8
import numpy as np

## 6 planes, 12 edges and 8 vertices
vertices=[[1,1,1],[1,-1,1],[-1,1,1],[1,1,-1],[-1,-1,-1],[-1,-1,1],[1,-1,-1],[-1,1,-1]]
def find_cub_by_shell(n, tot):
    k = 2*tot + 1
    ind = np.zeros(k**3, dtype=bool)
    if n==0:
        res=[[0,0,0]]
#    print(sorted([[1,0,0],[-1,0,0],[0,1,0],[0,-1,0],[0,0,1],[0,0,-1],[1,1,0],[1,0,1],[0,1,1],[1,-1,0],[-1,1,0],[1,0,-1],[-1,0,1],[0,1,-1],[0,-1,1],[-1,-1,0],[-1,0,-1],[0,-1,-1],
#            [1,1,1],[1,-1,1],[-1,1,1],[1,1,-1],[-1,-1,-1],[-1,-1,1],[1,-1,-1],[-1,1,-1]]))
    else:
        res = []
        for i in np.array(vertices)*n:
            res.append(list(i))
        for i in range(-n+1,n):
            res.append([n,n,i])
            res.append([n,i,n])
            res.append([i,n,n])
            res.append([-n,n,i])
            res.append([-n,i,n])
            res.append([i,-n,n])
            res.append([n,-n,i])
            res.append([n,i,-n])
            res.append([i,n,-n])
            res.append([-n,-n,i])
            res.append([-n,i,-n])
            res.append([i,-n,-n])
        for i in range(-n+1,n):
            for j in range(-n+1,n):
                res.append([i,j,n])
                res.append([i,j,-n])
                res.append([i,n,j])
                res.append([i,-n,j])
                res.append([n,i,j])
                res.append([-n,i,j])
    res = np.array(res) + [tot,tot,tot]
    ksq = k**2
    for i in range(len(res)):
        ind[res[i][0]*ksq + res[i][1] * k + res[i][2]] = True


    return ind

if __name__ == "__main__":
#    shell = find_cub_by_shell(100,300)
#    a = []
#    for i,j,k in shell:
#        a.append(i*1201**2 + j*1201 + k)
#    print(shell)
#    print(np.sum(shell))
#    print(len(shell))
    for i in range(600):
        mask = find_cub_by_shell(i,600)
        np.savez(str(i), mask)
    mask = find_cub_by_shell(600,600)
    np.savez("600", mask)

