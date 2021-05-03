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
from integrateur_forces import *
import matplotlib.animation as anim
import matplotlib.pyplot as plt
import numpy as np
import os
import random
import numpy.random as rd
from matplotlib.artist import Artist

# %%initialisation

#Définition des seed pour la reproductibilité

random.seed(2021)
rd.seed(2021)

#Suppression des anciens fichiers
ans_user = input('Voulez-vous supprimer les anciens fichiers de position ? y/n    ')
if ans_user == 'y':
    os.remove('tab_pos.txt')
    os.remove('tab_vitesse.txt')
    print('Fichiers supprimés.')

#interval de temps
dt = 0.01
#Nombre de particule
n = 20
#Type de simulation
Sim_forces =False # True pour du Newtonien, False sinon
#Initialisation des personnes, des murs et des sorties
#Particule qui seront en fait des obstacles
poteau = np.array([personne(5,5,0,0,1,0,0)])
#Nombre d'obstacle
n_obstacle = len(poteau)
#Particules à proprement parlé, murs et sorties
PosVi_tab , classe_tab , r , mur_class_tab = initial(n,8.5,8.5,poteau,Sim_forces)
#Positions précedentes
if Sim_forces:
    PosViprec_tab = pos_ini(PosVi_tab,dt)
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
    n_tot = n + n_obstacle
    #Calcul des nouvelles positions
    if Sim_forces:
        PosViprec_tab , PosVi_tab = change_posvi_forces(PosVi_tab,PosViprec_tab,classe_tab,mur_class_tab,dt,n_tot)
    else:
        PosVi_tab = change_posvi(PosVi_tab,classe_tab,mur_class_tab,dt,n_tot)
    #Test de la distance à la sortie
    n_inside = n_liste[-1]
    r_bis=r[:]
    c=0
    for num , part in enumerate(classe_tab):
        for mur in mur_class_tab:
            if mur.handle_part_exit(part) == True and part.v_max!=0: #La personne sort
                n_inside = n_inside - 1
                #Supprime la personne de classe_tab
                classe_tab = np.delete(classe_tab,num-c)
                #Supprime la ligne lié a la position de la personne
                PosVi_tab = np.delete(PosVi_tab,num-c,0)
                if Sim_forces:
                    PosViprec_tab = np.delete(PosViprec_tab,num-c,0)
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
print('Évacuation en {} s'.format(p*dt))
    
# %% Représentation graphique

#Transfert du fichier position en un tableau
tab_pos , tab_vitesse = readfile()

#Définition de la figure
fig, ax = plt.subplots()
fig.set_sizes=(10,10)

#Visualisation des murs ?
M=[0,10,10,0,0] ; N =[0,0,10,10,0]

#Définition de l'axe
ax.axis('equal')
ax.set(xlim=(-1, 11), ylim=(-1, 11))

L=[]
for i in range(p):
    s=str(i*dt)
    L=L+[plt.text(11,11,s)]
    Artist.set_visible(L[i], False)

#Fonction d'initialisation
def init():
    pass
    return

#Plot de la figure
plt.plot(M,N)

#Animation
ani = anim.FuncAnimation(fig, animate, frames=p, init_func= init, blit=False,save_count=p, 
                             interval=10, repeat=False , fargs = (tab_pos,ax,R,n_liste,L,n_obstacle))

#Sauvegarde de l'animation en fichier .mp4
# ans_user = input('Sauvegarder animation ? y/n    ')
# if ans_user == 'y':
#     Writer = anim.writers['ffmpeg']
#     writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)
#     ani.save('simulation.mp4', writer=writer)