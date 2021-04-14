#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Animation de la simulation
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anim

def animate(i,tab_pos,dt,t_fin,scater,R,n_liste):
    scat=scater
    (npas,c)=np.shape(tab_pos)
    M=tab_pos[int(np.sum(n_liste[0:i])):int(np.sum(n_liste[0:i]))+n_liste[i]]
    scat.set_offsets(M)
    return scat,

if __name__ == '__main__':

    def positions(i):
        return [(i,2*i),(2*i,i),(6*i+500,-5*i+500),(0.5*i+900,-2*i+900)]
   
    M=[0,1000,1000,0,0]
    N=[0,0,1000,1000,0]
    fig=plt.figure(1)
    fig.set_sizes=(10,10)
    plt.xlim(-10,1010)
    plt.ylim(-10,1010)
    line, = plt.plot([],[],'.')
    plt.plot(M,N)
    ani = anim.FuncAnimation(fig, animate, frames=1000, blit=True, 
                             interval=5, repeat=False)