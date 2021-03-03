#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Faire une fonction qui affiche le mouvement de particule dans un espace donné.
"""

# Importation des librairies
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anim
from matplotlib.patches import Circle
# Definition des fonctions

def init():
    line.set_data([],[])
    return line,

def positions(i):
    return [(i,2*i),(2*i,i),(6*i+500,-5*i+500),(0.5*i+900,-2*i+900)]


def animate(i,n=20,R=20):
    M=positions(i)
    angles=np.linspace(0,2*np.pi,n)
    Lx=np.array([])
    Ly=np.array([])
    for J in M:
        (xc,yc)=J
        Lx=np.hstack((Lx,R*np.cos(angles)+xc))
        Ly=np.hstack((Ly,R*np.sin(angles)+yc))
    line.set_data(Lx,Ly)
    return line,

# Programme principal
if __name__ == "__main__":
   M=[0,1000,1000,0,0]
   N=[0,0,1000,1000,0]
   fig=plt.figure(1)
   fig.set_sizes=(10,10)
   plt.xlim(-10,1010)
   plt.ylim(-10,1010)
   line, = plt.plot([],[],'.')
   plt.plot(M,N)
   ani = anim.FuncAnimation(fig, animate, frames=1000, blit=True, interval=20, repeat=False)
   plt.show()
