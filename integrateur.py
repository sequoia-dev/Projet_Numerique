# -*- coding: utf-8 -*-
"""

Programme permettant à partir des positions et vitesses des personnes 
à un temps t ainsi que des positions des sorties de connaitre les positions
et vitesses au temps t+dt.

"""
# %% Importation des librairies
import numpy as np
from mur_class import *
from personne_class import *
import itertools
import random

# %% Définition des fonctions
def v_sortie(classe_tab,mur_class_tab,n):
    
    """
    Calcul les vitesses de chaque personnes par rapport à la sortie la plus proche.
    """
    
    V=np.zeros((n,2))
    
    for num_part, part in enumerate(classe_tab):
        
        d,v= part.distances_sortie(mur_class_tab)
        i_min=np.argmin(d)
        d=d[i_min]
        v=(v[i_min,:]*part.v_max)/d
        V[num_part] = v
    
    return V
    
def change_v_part(vect,pers,PosVi):
        """
        Change la vitesse la particule en lui supprimant sa composante 
        perpendiculaire à un obstacle (mur ou autre peronne).
        """
        
        v = np.array([pers.vx , pers.vy])
        v_prec = PosVi[1,:]
        v_moy = (1/2)*( v_prec + v )
        prod_sca = np.vdot(vect , v )
        prod_sca_moy = np.vdot(vect , v_moy )
        v_nouv = prod_sca * vect
        v_nouv_moy = prod_sca_moy * vect
        
        return v_nouv , v_nouv_moy

def change_posvi(PosVi_tab,classe_tab,mur_class_tab,dt,n):
    
    """Calcul les vitesses et les positions des personnes au nouveau pas de temps"""
    
    #Calcul naif des vitesses et positions au pas de temps suivant
    V=v_sortie(classe_tab,mur_class_tab,n)
    V_moy = (1/2)*(PosVi_tab[:,1,:]+V)
    X=PosVi_tab[:,0,:]+dt*V_moy
    
    #Définition des couples de particules en intéraction
    ls = np.arange(0,len(classe_tab))
    couple = list(itertools.permutations(ls,2))
    
    #Mise à jour des vitesses et positions dans la classe personne
    for num_pers , pers in enumerate(classe_tab):
        
        pers.x= X[num_pers,0]
        pers.y= X[num_pers,1]
        pers.vx= V[num_pers,0]
        pers.vy= V[num_pers,1]
    
    #Décompte des superpositions et du nombre de pas de calcul
    a=1 ; p=0 ; p_max = max(5,int(n/2))
    
    while a!=0 and p<=p_max:
        
        a=0
        
        #Intéraction avec les murs
        for num_pers , pers in enumerate(classe_tab):
            
            c=0
            
            for mur in mur_class_tab :
                
                   if mur.collision(pers) and not mur.handle_part_exit(pers):
                      
                      #Compte le nombre de mur en contact avec la personne
                      c=c+1
                      a=a+1
                      #Change la vitesse de la personne pour que celle-ci ne traverse pas le mur
                      vect = mur.vect
                      (V[num_pers,:] , V_moy[num_pers,:]) = change_v_part(vect,pers,PosVi_tab[num_pers])
        
        #Intéraction de deux personnes entre elles
        random.shuffle(couple)
        for ij in couple:
            
            i = ij[0]
            j = ij[1]
            
            #Test de superposition
            if classe_tab[i].superpose(classe_tab[j]):
                
                a=a+1
                #Calcul du vecteur allant de la personne i à j
                vect_par = PosVi_tab[i,0,:]-PosVi_tab[j,0,:]
                vect_par=vect_par/np.linalg.norm(vect_par)
                
                #Projection de la vitesse sur un vecteur perpendiculaire au vecteur
                #allant de i à j si cette vitesse amène la personne sur l'autre.
                if np.vdot(vect_par,V_moy[i,:])<=0:
                    
                    #Calcul du vecteur perpendiculaire
                    vect_per = classe_tab[i].calcul_vect_per(vect_par)
                    #Projection de la vitesse
                    (V[i,:] , V_moy[i,:]) = change_v_part(vect_per,classe_tab[i],PosVi_tab[i])
                
                elif np.vdot(vect_par,V_moy[j,:])>=0:
                    
                    #Calcul du vecteur perpendiculaire
                    vect_per = classe_tab[j].calcul_vect_per(vect_par)
                    #Projection de la vitesse
                    (V[j,:] , V_moy[j,:]) = change_v_part(vect_per,classe_tab[j],PosVi_tab[j])
                    
        X=PosVi_tab[:,0,:]+dt*V_moy
        p=p+1
        #Mise à jour des vitesses et positions dans la classe personne
        for num_pers , pers in enumerate(classe_tab):
            
            pers.x= X[num_pers,0]
            pers.y= X[num_pers,1]
            pers.vx= V[num_pers,0]
            pers.vy= V[num_pers,1]
    #Mise à jour de PosVi_tab
    X , V = np.reshape(X,(n,1,2)) , np.reshape(V,(n,1,2))
    PosVi_tab = np.concatenate((X,V),axis=1) 
    
    return PosVi_tab

# %% Tests
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