#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simulation de la sortie de n personnes depuis une salle fermée vers une ou plusieurs
sortie.
"""

# %% Importation des librairies

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
dt = 0.01
#Nombre de particule
n = 50

#Définition des murs
def f1(pers) :
    return pers.y + pers.r >= 10

def f2(pers) :
    return pers.y - pers.r <=0

def f3(pers) :
    return pers.x + pers.r >=10

def f4(pers) :
    return pers.x - pers.r <=0

vect1=np.array([1,0])

vect2=np.array([1,0])

vect3=np.array([0,1])

vect4=np.array([0,1])

sortie1 = np.array([[5,6],[0,0.5]])
sortie2 = np.array([[5,6],[9.5,10]])

mur_class_tab=np.array([mur(f1,vect1,sortie1),mur(f2,vect2),mur(f3,vect3),mur(f4,vect4)])

#Définition du centre de la salle
centre=np.array([5,5])

#Initialisation des particules
PosVi_tab , classe_tab , r = initial(n,x=8,y=8)

#Sauvegarde des position initiales
savefile(PosVi_tab)

#Définition du temps de fin de simulation
t_fin = 10

#Liste du nombre de personne et du rayon des personnes
n_liste = [n]
R=[r]

#Effectuer la simulation
p=0
while n!=0 and p*dt<=t_fin : 
    #Calcul des nouvelles positions
    PosVi_tab = change_posvi(PosVi_tab,classe_tab,mur_class_tab,centre,dt,n)
    #Test de la distance à la sortie
    n_inside = n_liste[-1]
    r_bis=r[:]
    c=0
    for num , part in enumerate(classe_tab):
        for mur in mur_class_tab:
            if mur.handle_part_exit(part) == True: #La personne sort
                n_inside = n_inside - 1
                #Supprime la personne de classe_tab
                classe_tab = np.delete(classe_tab,num-c)
                #Supprime la ligne lié a la position de la personne
                PosVi_tab = np.delete(PosVi_tab,num-c,0)
                #Supprime le rayon de la personne
                r_bis.pop(num-c)
                #Compte le nombre de personne supprimé ce pas de temps
                c=c+1
    #Actualise les listes de rayons et de nombre de particules
    r=r_bis[:]
    R=R+[r[:]]
    n_liste.append(n_inside)
    n = n_inside
    #Compte le nombre de pas de temps
    p=p+1
    #Sauvegarde des nouvelles positions
    savefile(PosVi_tab)
    
# %% Représentation graphique

#Lecture des fichiers de positions au cours du temps
tab_pos , tab_vitesse = readfile()

#Définition de la figure
fig, ax = plt.subplots()
fig.set_sizes=(10,10)

#Visualisation des murs ?
M=[0,10,10,0,0] ; N =[0,0,10,10,0]

#Définition de l'axe
ax.axis('equal')
ax.set(xlim=(-1, 11), ylim=(-1, 11))

#Fonction d'initialisation
def init():
    pass
    return

A=np.zeros(n_liste[0]) # Sert à donner la bonne dimension a X,Y avant que les données soit introduites. Ne pas le faire pose des problèmes de dimension de R.

#Plot de la figure
plt.plot(M,N)

#Animation
ani = anim.FuncAnimation(fig, animate, frames=p, init_func= init, blit=False,save_count=p, 
                             interval=100, repeat=False , fargs = (tab_pos,ax,R,n_liste))

# #Sauvegarde de l'animation en fichier .mp4
# ans_user = input('Sauvegarder animation ? y/n    ')
# if ans_user == 'y':
#     Writer = anim.writers['ffmpeg']
#     writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)
#     ani.save('simulation.mp4', writer=writer)