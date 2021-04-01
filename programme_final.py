#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test avec 3 particules
"""

from personne_class import *
from savetab import *
from animation import *
from integrateur import *
import matplotlib.animation as anim
import matplotlib.pyplot as plt
import numpy as np

#initialisation

dt = 1
n = 20

PosVi_tab , classe_tab , R =initial(n,x=100,y=100)

PosViprec_tab = pos_ini(PosVi_tab, dt)

t_fin = 1000

t = np.linspace(0,t_fin,int(t_fin/dt))

for i in t:
    F_tab = tab_force(classe_tab,100)
    PosViprec_tab , PosVi_tab = change_posvi(PosVi_tab,PosViprec_tab,F_tab,classe_tab,dt,n)
    savefile(PosVi_tab)
    
# %%
tab_pos , tab_vitesse = readfile()


fig=plt.figure(1)
fig.set_sizes=(10,10)
ax = plt.axes(xlim=(-1000, 1000), ylim=(-1000, 1000))
A=np.zeros(n) # Sert à donner la bonne dimension a X,Y avant que les données soit introduites. Ne pas le faire pose des problèmes de dimension de R.
scat = ax.scatter(A, A, s=R , facecolors='none', edgecolors='blue')
ani = anim.FuncAnimation(fig, animate, frames=int(t_fin/dt), blit=True, 
                             interval=10, repeat=False,fargs = (tab_pos,dt,t_fin,scat,R))
