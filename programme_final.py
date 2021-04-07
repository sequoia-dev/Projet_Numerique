#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test avec 3 particules
"""

from personne_class import *
from savetab import *
from animation import *
from integrateur import *
from mur_class import *
import matplotlib.animation as anim
import matplotlib.pyplot as plt
import numpy as np

# %%initialisation

dt = 0.001
n = 20

def f1(x,y) :
    return y>=9.9

def f2(x,y) :
    return y<=0.1

def f3(x,y) :
    return x>=9.9

def f4(x,y) :
    return x<=0.1

vect1=np.array([1,0])

vect2=np.array([1,0])

vect3=np.array([0,1])

vect4=np.array([0,1])

mur_class_tab=np.array([mur(f1,vect1),mur(f2,vect2),mur(f3,vect3),mur(f4,vect4)])

PosVi_tab , classe_tab , R =initial(n,x=10,y=10)

R=100*R

savefile(PosVi_tab)

PosViprec_tab = pos_ini(PosVi_tab, dt)

t_fin = 100

t = np.linspace(0,t_fin,int(t_fin/dt))

for i in t:
    F_tab = tab_force(classe_tab,100)
    PosViprec_tab , PosVi_tab = change_posvi(PosVi_tab,PosViprec_tab,F_tab,classe_tab,mur_class_tab,dt,n)
    savefile(PosVi_tab)
    
# %%
tab_pos , tab_vitesse = readfile()


fig=plt.figure(1)
fig.set_sizes=(10,10)

M=[0,10,10,0,0] ; N =[0,0,10,10,0]



ax = plt.axes(xlim=(-1, 11), ylim=(-1, 11))

A=np.zeros(n) # Sert à donner la bonne dimension a X,Y avant que les données soit introduites. Ne pas le faire pose des problèmes de dimension de R.
scat = ax.scatter(A, A, s=R , facecolors='none', edgecolors='blue')
plt.plot(M,N)
ani = anim.FuncAnimation(fig, animate, frames=int(t_fin/dt), blit=True, 
                             interval=0.1, repeat=False , save_count= int(t_fin/dt) , fargs = (tab_pos,dt,t_fin,scat,R))

