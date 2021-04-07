# -*- coding: utf-8 -*-
"""
Codage d'une première version de l'intégrateur des positions et des vitesses
"""
import numpy as np

def acceleration(F_tab,classe_tab):
    
    """Calcul un tableau contenant les accélérations de chaque particules
selon chaque axes. La forme du tableau est donc (n,2)"""
        
    sumF_tab=np.sum(F_tab,axis=2)
    n = len(classe_tab)
    a_tab= np.zeros((2,n))
    for i in range(0,n):
        a_tab[:,i] = sumF_tab[:,i]/classe_tab[i].m
        
    a_tab = np.reshape(a_tab,(n,2))
    return a_tab

def change_posvi(PosVi_tab,PosViprec_tab,F_tab,classe_tab,mur_class_tab, dt,n):
    
    """Calcul les vitesses des particules au nouveau pas de temps"""
    a_tab=acceleration(F_tab,classe_tab)
    V=PosViprec_tab[:,1,:] + 2*a_tab*dt
    i=0
    for j in classe_tab :
        for k in mur_class_tab :
           if k.collision(j):
              PosVi_tab[i,1,:]=k.change_v_part(j)
        i=i+1
    i=0
    for j in V :
        Vtot=np.sqrt(j[0]**2+j[1]**2)
        if Vtot > 1 :
            V[i,0] ,V[i,1] = j[0]/Vtot , j[1]/Vtot
        i=i+1
    X=PosVi_tab[:,0,:]+(dt/2)*(PosVi_tab[:,1,:]+V)
    X , V = np.reshape(X,(20,1,2)) , np.reshape(V,(20,1,2))
    #PosViprec_tab , PosVi_tab = PosVi_tab , np.concatenate((np.reshape(2*PosVi_tab[:,0,:]-PosViprec_tab[:,0,:]+a_tab*dt**2,(n,1,2)),np.reshape(PosViprec_tab[:,1,:]+2*a_tab*dt,(n,1,2))),axis=1)
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