#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Faire une fonction qui affiche le mouvement de particule dans un espace donné.
"""

# Importation des librairies
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anim
# Definition des fonctions

def init():
    line.set_data([],[])
    return line,

def animate(i): 
    x=i
    y=2*i
    line.set_data(x,y)
    return line,

# Programme principal
if __name__ == "__main__":
   M=[0,100,100,0,0]
   N=[0,0,200,200,0]
   fig=plt.figure(1)
   fig.set_sizes=(10,10)
   plt.xlim(-10,110)
   plt.ylim(-10,210)
   line, = plt.plot([],[],'bo')
   plt.plot(M,N)
   ani = anim.FuncAnimation(fig, animate, frames=100, blit=True, interval=20, repeat=False)
   plt.show()
