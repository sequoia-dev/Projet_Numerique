# -*- coding: utf-8 -*-
"""
Codage d'une première version de l'intégrateur des positions et des vitesses
"""
import numpy as np
from mur_class import *
from personne_class import *

def acceleration(sumF_tab,classe_tab,n):
    
    """Calcul un tableau contenant les accélérations de chaque particules
selon chaque axes. La forme du tableau est donc (n,2)"""
    
    a_tab= np.zeros((n,2))
    for i in range(0,n):
        a_tab[i,:] = sumF_tab[i,:]/classe_tab[i].m
        
    return a_tab

def change_posvi(PosVi_tab,PosViprec_tab,classe_tab,mur_class_tab, dt,n):
    
    """Calcul les vitesses des particules au nouveau pas de temps"""
    F_tab_part = tab_force(classe_tab,100) #Tableau des forces entre particules
    sumF_tab=np.reshape(np.sum(F_tab_part,axis=2),(n,2))
    F_tab_mur = tab_force_mur(mur_class_tab,classe_tab) #Tableau des forces de sortie
    sumF_tab = sumF_tab + F_tab_mur
    a_tab=acceleration(sumF_tab,classe_tab,n)
    V=PosViprec_tab[:,1,:] + 2*a_tab*dt
    i=0
    Vtot=np.sqrt(V[:,0]**2+V[:,1]**2)
    for j in V :
        vm=classe_tab[i].v_max
        Vtoti=Vtot[i]
        if Vtoti > vm :
           V[i,:]=j/Vtoti
        i=i+1
    Vmoy = (1/2)*(PosVi_tab[:,1,:]+V)
    i=0
    for j in classe_tab :
        vect=[]
        for k in mur_class_tab :
           if k.collision(j):
              
              V[i,:]=k.change_v_part(V[i])
              Vmoy[i,:]=k.change_v_part(Vmoy[i])
              
        
        i=i+1
    X=PosVi_tab[:,0,:]+dt*Vmoy
    X , V = np.reshape(X,(20,1,2)) , np.reshape(V,(20,1,2))
    PosViprec_tab , PosVi_tab = PosVi_tab , np.concatenate((X,V),axis=1)
    i=0
    for j in classe_tab:
        j.x= PosVi_tab[i,0,0]
        j.y= PosVi_tab[i,0,1]
        j.vx= PosVi_tab[i,1,0]
        j.vy= PosVi_tab[i,1,1]
        i=i+1
    return PosViprec_tab , PosVi_tab

def pos_ini(PosVi_tab,dt):
    pos_ini_tab = np.zeros(np.shape(PosVi_tab))
    pos_ini_tab[:,0,:] = PosVi_tab[:,0,:]-dt*PosVi_tab[:,1,:]
    return pos_ini_tab


if __name__=='__main__':

    (x,y,vx,vy,r,m)=(1,1,1,1,1,1)
    dt=1
    n=3
    PosVi_tab=np.array([[[1,1],[1,1]],[[2,2],[2,2]],[[3,3],[3,3]]])
    PosViprec_tab=np.array([[[1,2],[1,2]],[[6,2],[6,2]],[[0,3],[0,3]]])
    F_tab=np.array([[[1,1],[2,1],[7,2]],[[2,1],[1,5],[8,3]],[[3,4],[1,4],[5,3]]])
    classe_tab=np.array([[1],[1],[1]])
    print(PosVi_tab , PosViprec_tab)
    M=change_posvi(PosVi_tab, PosViprec_tab, F_tab, classe_tab, dt , n)
    print(M)