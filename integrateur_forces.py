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
        a_tab[i,:] = sumF_tab[i,:]
        
    return a_tab

def force(part1,part2,detection):
    """ 
    Retourne la force de repulsion entre la particule et une autre.
    Les particule en dehors du rayon de detection sont negligées
    """
    if part1.distance(part2)[0] < detection:
        
        if part1.distance(part2)[1] == 0: #Eviter une division par 0
            Fx = 0
        else:
            Fx = -1/part1.distance(part2)[1]**7 
        
            
        if part1.distance(part2)[2] == 0: #Eviter une division par 0
            Fy = 0
        else:
            Fy = -1/part1.distance(part2)[2]**7 
                
        F = np.array([Fx,Fy])
    
    else :
        F = np.zeros(2)
        
    norm_F=np.linalg.norm(F)
    
    if norm_F>10:
        
        F=F/norm_F
        
    return F

def pos_ini(PosVi_tab,dt):
    pos_ini_tab = np.zeros(np.shape(PosVi_tab))
    pos_ini_tab[:,0,:] = PosVi_tab[:,0,:]-dt*PosVi_tab[:,1,:]
    return pos_ini_tab

def tab_force(classe_tab,detection):
    """
    Retourne le tableau de force entre N particules = len(class_tab). 
    class_tab est le tableau des objets particules. 
    detecttion est le seuil de detection pour la force
    """
    F_tab_x = np.zeros((len(classe_tab),len(classe_tab)))
    F_tab_y = np.zeros((len(classe_tab),len(classe_tab)))
    ls = np.arange(0,len(classe_tab))
    #couple = list(itertools.permutations(ls,2)) 
    couple = list(itertools.combinations(ls,2))
    for ij in couple:
        i = ij[0]
        j = ij[1]
        F_tab_x[i,j] = force(classe_tab[i],classe_tab[j],detection)[0]
        F_tab_x[j,i] = - F_tab_x[i,j]
        F_tab_y[i,j] = force(classe_tab[i],classe_tab[j],detection)[1]
        F_tab_y[j,i] = - F_tab_y[i,j]
    F_tab = np.array([F_tab_x,F_tab_y])
        
    return F_tab

def tab_force_mur(mur_class_tab,classe_tab):
    """
    Retourne le tableau de force sur chaque particule des mur
    tableau de taille (nbr_part,2)
    Reflechir au sens de cette fonction, que ce passe-t-il si la part est au centre ? Elle doit prendre la sortie la plus proche et si elles sont toutes a distances = alors faire un choix aléatoire
    """
    
    F_tab = np.zeros([len(classe_tab),2])
    
    for num_part, part in enumerate(classe_tab):
        #d = np.array([100 * np.ones(len(mur_class_tab)),mur_class_tab])
        #np.reshape(d,(len(mur_class_tab),2))
        d = []
        for num_mur, mur in enumerate(mur_class_tab):
            if np.any(mur.sortie != None) == True:
                pos_sortie = [np.mean(mur.sortie[0]) , np.mean(mur.sortie[1])]
                v = np.array([pos_sortie[0]-part.x,pos_sortie[1]-part.y])
                distance = np.linalg.norm(v)
                d.append([distance,mur])
                
        d = np.array(d)
        i_min = np.argmin(d,axis=0)
                
        mur_proche = d[i_min[0]][1]
        
        F = np.array([mur_proche.force_exit(part)[0],mur_proche.force_exit(part)[1]])
        F_tab[num_part] = F
                
        
    return F_tab

def change_posvi_forces(PosVi_tab,PosViprec_tab,classe_tab,mur_class_tab, dt,n):
    
    """Calcul les vitesses des particules au nouveau pas de temps"""
    
    F_tab_part = tab_force(classe_tab,100) #Tableau des forces entre particules
    sumF_tab=np.reshape(np.sum(F_tab_part,axis=2),(n,2))
    F_tab_mur = tab_force_mur(mur_class_tab,classe_tab) #Tableau des forces de sortie
    sumF_tab = sumF_tab + F_tab_mur
    a_tab=acceleration(sumF_tab,classe_tab,n)
    V=PosViprec_tab[:,1,:] + 2*a_tab*dt
    Vtot=np.sqrt(V[:,0]**2+V[:,1]**2)
    
    for i , j in enumerate(V) :
        
        vm=classe_tab[i].v_max
        Vtoti=Vtot[i]
        
        if Vtoti > vm :
            
           V[i,:]=(j/Vtoti)*vm
           
    Vmoy = (1/2)*(PosVi_tab[:,1,:]+V)
        
    for i , j in enumerate(classe_tab) :
        
        j.vx = V[i,0]
        j.vy = V[i,1]
        
        for k in mur_class_tab :
            
           if k.collision(j):
              
              V[i,:] , Vmoy[i,:] =change_v_part(k.vect , j , PosVi_tab[i,:,:])
              
    X=PosVi_tab[:,0,:]+dt*Vmoy
    X , V = np.reshape(X,(n,1,2)) , np.reshape(V,(n,1,2))
    PosViprec_tab , PosVi_tab = PosVi_tab , np.concatenate((X,V),axis=1)
    
    for i , j in enumerate(classe_tab):
        
        j.x= PosVi_tab[i,0,0]
        j.y= PosVi_tab[i,0,1]
        j.vx= PosVi_tab[i,1,0]
        j.vy= PosVi_tab[i,1,1]
        
    return PosViprec_tab , PosVi_tab




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