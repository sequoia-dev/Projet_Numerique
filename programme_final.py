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
import os

# %%initialisation

#Suppression des anciens fichiers
ans_user = input('Voulez-vous supprimer les anciens fichiers de position ? y/n    ')
if ans_user == 'y':
    os.remove('tab_pos.txt')
    os.remove('tab_vitesse.txt')
    print('Fichiers supprimés.')

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

sortie1 = np.array([[5,6],[0,0.1]])
sortie2 = np.array([[5,6],[9.8,10]])

mur_class_tab=np.array([mur(f1,vect1,sortie1),mur(f2,vect2),mur(f3,vect3),mur(f4,vect4)])

#Initialisation des particules
PosVi_tab , classe_tab , R =initial(n,x=10,y=10)

R=50*R

#Sauvegarde des position initiales
savefile(PosVi_tab)

PosViprec_tab = pos_ini(PosVi_tab, dt)

#Définition du temps de fin de simulation
t_fin = 100
#Discrétisation du temps
#Peut être faire un tant qu'il y a des particules
t = np.linspace(0,t_fin,int(t_fin/dt))

#Liste du nombre de particules
n_liste = [n]

#Effectuer la simulation
for i in t: 
    #Calcul des nouvelles position
    PosViprec_tab , PosVi_tab = change_posvi(PosVi_tab,PosViprec_tab,classe_tab,mur_class_tab,dt,n)
    #Sauvegarde des nouvelles positions
    savefile(PosVi_tab)
    #Test de la distance à la sortie
    n_inside = n_liste[-1]
    for num , part in enumerate(classe_tab):
        for mur in mur_class_tab:
            if mur.handle_part_exit(part) == True: #La particule sort
                n_inside = n_inside - 1
                #Supprime la particule de classe_tab
                classe_tab = np.delete(classe_tab,num)
                #Supprime la ligne lié a la position de la particule
                PosViprec_tab = np.delete(PosViprec_tab,num,0)
                PosVi_tab = np.delete(PosVi_tab,num,0)
    n_liste.append(n_inside)
    n = n_inside
    
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

A=np.zeros(n_liste[0]) # Sert à donner la bonne dimension a X,Y avant que les données soit introduites. Ne pas le faire pose des problèmes de dimension de R.

#Définition des points représentant une personne
scat = ax.scatter(A, A , s=R, facecolors='none', edgecolors='blue')

#Plot de la figure
plt.plot(M,N)

#Animation
ani = anim.FuncAnimation(fig, animate, frames=int(t_fin/dt), blit=True, 
                             interval=10, repeat=False , save_count= int(t_fin/dt) , fargs = (tab_pos,dt,t_fin,scat,R,n_liste))

#Sauvegarde de l'animation en fichier .mp4
ans_user = input('Sauvegarder animation ? y/n    ')
if ans_user == 'y':
    Writer = anim.writers['ffmpeg']
    writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)
    ani.save('simulation.mp4', writer=writer)