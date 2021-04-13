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

#interval de temps
dt = 0.1
#Nombre de particule
n = 20

#Définition des mur
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

sortie = np.array([[5,6],[0,0]])

mur_class_tab=np.array([mur(f1,vect1),mur(f2,vect2),mur(f3,vect3),mur(f4,vect4,sortie)])

#Initialisation des particules
PosVi_tab , classe_tab , R =initial(n,x=10,y=10)

R=100*R

#Sauvegarde des position initiales
savefile(PosVi_tab)

PosViprec_tab = pos_ini(PosVi_tab, dt)

#Définition du temps de fin de simulation
t_fin = 100
#Discrétisation du temps
t = np.linspace(0,t_fin,int(t_fin/dt))

#Effectuer la simulation
for i in t:
    #Calcul du tableau des forces
    F_tab_part = tab_force(classe_tab,100) #Tableau des forces entre particules
    #A intetegrer dans l'integrateur
    F_tab_mur = tab_force_mur(mur_class_tab,classe_tab) #Tableau des forces de sortie
    
    #Calcul des nouvelles position
    PosViprec_tab , PosVi_tab = change_posvi(PosVi_tab,PosViprec_tab,F_tab_part,classe_tab,mur_class_tab,dt,n)
    #Sauvegarde des nouvelles positions
    savefile(PosVi_tab)
    
# %% Représentation graphique

#Lecture des fichiers de positions au cours du temps
tab_pos , tab_vitesse = readfile()

#Définition de la figure
fig=plt.figure(1)
fig.set_sizes=(10,10)

#Visualisation des murs ?
M=[0,10,10,0,0] ; N =[0,0,10,10,0]

#Définition de l'axe
ax = plt.axes(xlim=(-1, 11), ylim=(-1, 11))

A=np.zeros(n) # Sert à donner la bonne dimension a X,Y avant que les données soit introduites. Ne pas le faire pose des problèmes de dimension de R.

#Définition des points représentant une personne
scat = ax.scatter(A, A, s=R , facecolors='none', edgecolors='blue')

#Plot de la figure
plt.plot(M,N)

#Animation
ani = anim.FuncAnimation(fig, animate, frames=int(t_fin/dt), blit=True, 
                             interval=0.1, repeat=False , save_count= int(t_fin/dt) , fargs = (tab_pos,dt,t_fin,scat,R))

