# -*- coding: utf-8 -*-
"""
Codage d'une première version de l'intégrateur des positions et des vitesses
"""
import numpy as np
from mur_class import *
from personne_class import *
import itertools

def acceleration(sumF_tab,classe_tab,n):
    
    """Calcul un tableau contenant les accélérations de chaque particules
selon chaque axes. La forme du tableau est donc (n,2)"""
    
    a_tab= np.zeros((n,2))
    for i in range(0,n):
        a_tab[i,:] = sumF_tab[i,:]/classe_tab[i].m
        
    return a_tab

def change_posvi(PosVi_tab,PosViprec_tab,classe_tab,mur_class_tab, dt,n):
    
    """Calcul les vitesses des particules au nouveau pas de temps"""
    (V,D,P)=v0_part(mur_class_tab,classe_tab)
    Vmoy = (1/2)*(PosVi_tab[:,1,:]+V)
    for num_part , part in enumerate(classe_tab) :
        for k in mur_class_tab :
           if k.collision(part):
              
              V[num_part,:]=k.change_v_part(V[num_part])
              Vmoy[num_part,:]=k.change_v_part(Vmoy[num_part])
              
    for num_part , v in enumerate(Vmoy) :
        if v.any()==0:
            direction=np.array(P[num_part,0]-classe_tab[num_part].x,P[num_part,1]-classe_tab[num_part].y)
            Vmoy[num_part]=(classe_tab[num_part].v_max * direction)/np.linalg.norm(direction)
    X=PosVi_tab[:,0,:]+dt*Vmoy
    i=0
    for j in classe_tab:
        j.x= X[i,0]
        j.y= X[i,1]
        j.vx= V[i,0]
        j.vy= V[i,1]
        i=i+1
    
    ls = np.arange(0,len(classe_tab))
    couple = list(itertools.combinations(ls,2))
    
    for ij in couple:
        i = ij[0]
        j = ij[1]
        if classe_tab[i].superpose(classe_tab[j]):
            
            
            if D[i]>D[j]:
                classe_tab[i].x=PosVi_tab[i,0,0]
                classe_tab[i].x=PosVi_tab[i,0,1]
                X[i]=PosVi_tab[i,0,:]
            else:
                classe_tab[j].x=PosVi_tab[j,0,0]
                classe_tab[j].x=PosVi_tab[j,0,1]
                X[j]=PosVi_tab[j,0,:]
            
    X , V = np.reshape(X,(n,1,2)) , np.reshape(V,(n,1,2))
    PosViprec_tab , PosVi_tab = PosVi_tab , np.concatenate((X,V),axis=1)
    
    
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