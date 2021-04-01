#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Animation de la simulation
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anim

def animate(i,tab_pos,dt,t_fin,nbr=20,R=1,):
    pas=int(t_fin/dt)
    (npas,c)=np.shape(tab_pos)
    n=int(npas/pas)
    M=tab_pos[n*i:n*(i+1)]
    angles=np.linspace(0,2*np.pi,nbr)
    Lx=np.array([])
    Ly=np.array([])
    for J in M:
        (xc,yc)=J
        Lx=np.hstack((Lx,R*np.cos(angles)+xc))
        Ly=np.hstack((Ly,R*np.sin(angles)+yc))
    
    return plt.plot(Lx,Ly,'.',color='r')

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