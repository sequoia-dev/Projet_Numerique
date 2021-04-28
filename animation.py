#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Animation de la simulation
"""
# %% Importation des librairies
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anim
from matplotlib.artist import Artist
# %% Définition de la fonction

def animate(i,tab_pos,ax,R,n_liste,dt,L):
    """
    Fonction qui retire les persones affiché au temps t-dt et affiche celle au temps t
    """
    # if i!=0 :
    #     Artist.set_visible(L[i-1], False)
    # Artist.set_visible(L[i], True)
    #Retire les anciens objets correspondant aux personnes au temps t-dt
    for obj in ax.findobj(match = type(plt.Circle(1, 1))):
        
        obj.remove()
    #Extrait les positions des personnes à afficher
    M=tab_pos[int(np.sum(n_liste[0:i])):int(np.sum(n_liste[0:i]))+n_liste[i]]
    #Affiche un cercle pour représenter la personne. Sont centre est la postion de la
    #personne et son rayon est le rayon de la personne.
    
    for u , j in enumerate(M):
        
        ax.add_artist(plt.Circle(j,radius=R[i][u],fill=False))
        
    return

# %% Tests
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