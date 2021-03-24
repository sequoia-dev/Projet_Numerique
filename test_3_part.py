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

part1 = personne(0,0,0,0,1,1,0)
part2 = personne(1,0,0,0,1,1,1)
part3 = personne(1,1,0,0,1,1,2)
    
classe_tab = np.array([part1,part2,part3])

dt = 1
n = len(classe_tab)

PosVi_tab = np.array([[[0,0],[0,0]],[[1,0],[0,0]],[[1,1],[0,0]]])

PosViprec_tab = pos_ini(PosVi_tab, dt)

t_fin = 100

t = np.linspace(0,t_fin,int(t_fin/dt))

for i in t:
    F_tab = tab_force(classe_tab,100)
    PosViprec_tab , PosVi_tab = change_posvi(PosVi_tab,PosViprec_tab,F_tab,classe_tab,dt,n)
    savefile(PosVi_tab)
    
tab_pos , tab_vitesse = readfile()

fig=plt.figure(1)
fig.set_sizes=(10,10)
plt.xlim(-1000,1000)
plt.ylim(-1000,1000)
ani = anim.FuncAnimation(fig, animate, frames=100, blit=True, 
                             interval=100, repeat=False,fargs = (tab_pos,20,1))
