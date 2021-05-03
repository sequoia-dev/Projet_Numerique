#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Definit la classe personne, la fonction permettant de calculer la force entre
deux particules et la fonction permettant de calculer le tableau de force entre
toutes les particules.
"""
# %% Importation des librairies
import numpy as np
import numpy.random as rd
import itertools
from mur_class import *

# %% Définition de la classe
class personne:
    """
    caractéristiques :
    position x,y
    vitesse vx,vy
    vitesse maximum
    rayon r
    numéro de personne
    """
    def __init__(self,x,y,vx,vy,r,v_max,num):
        
        """
        
        Définition de la personne.
        
        Parameters
        ----------
        x : Float
            Coordonée x de la position de la personne.
        y : Float
            Coordonée y de la position de la personne.
        vx : Float
            Coordonée x de la vitesse de la personnes.
        vy : Float
            Coordonée y  de la vitesse de la personne.
        r : Float
            Rayon de la personne (celle-ci à une forme de cercle vu du dessus).
        v_max : Float
            Norme de la vitesse maximale atteignable par la personne.
        num : Int
            Numéro de la personne.

        Returns
        -------
        None.

        """
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.r = r
        self.v_max = v_max
        self.num = num
        
    def distance(self,autre):
        """Retourne la distance entre la personne et une autre, sur l'axe x
        et y"""
        dx = self.x - autre.x
        dy = self.y - autre.y
        return np.sqrt(dx**2+dy**2),dx,dy
    
    def superpose(self,autre):
        """Retourne True si les deux personnes se superposent"""
        
        answer = self.distance(autre)[0] < self.r + autre.r
        return answer
    
    def distances_sortie(self,mur_class_tab):
    
        """
        Retourne la distance et la direction d'une personne à chaque sortie.
        """
        
        d = [] ; v = []
        for num_mur, mur in enumerate(mur_class_tab):
            
            if np.any(mur.sortie != None) == True:
                
                (vecteur,distance) = mur.d_mur(self)
                d.append(distance)  ; v.append(vecteur)
                
        d = np.array(d) ; v=np.array(v)
        
        return d , v

    def calcul_vect_per(self , vect_par):
        
        """Calcul le vecteur perpendicualaire à la direction entre deux personnes
        dont le produit scalaire avec le vecteur vitesse de la personne dont on modifie 
        la vitesse est positif"""
        
        v=np.array([self.vx , self.vy])
        
        if vect_par[1] == 0 :
            
            vect_1 = np.array([0,1])
            vect_2 = np.array([0,-1])
        
        else:
            
            vect_1 = np.array([1,-(vect_par[0]/vect_par[1])])
            vect_2 = np.array([-1,vect_par[0]/vect_par[1]])
            vect_1 = vect_1 / np.linalg.norm(vect_1)
            vect_2 = vect_2 / np.linalg.norm(vect_2)
        
        prod_sca_1 = np.vdot(vect_1 , v)
        
        if prod_sca_1 >= 0 :
            
            return vect_1
        
        return vect_2
# %% Définition de fonctions

def initial(n,x,y,poteau,Sim_forces,vm=7,r=0.3):
    """
    Placement aléatoire de n personnes et affectation de leurs caractéristiques
    en prenant en compte les poteaux
    """
    PosVi_tab=rd.rand(n,2,2)
    PosVi_tab[:,0,0]=PosVi_tab[:,0,0]*x+1
    PosVi_tab[:,0,1]=PosVi_tab[:,0,1]*y+1
    classe_tab=[]
    R=[]
    
    for num_part , PosVi in enumerate(PosVi_tab):
        
        ri=np.absolute(np.random.normal(r,0.05))
        v_max=np.absolute(np.random.normal(vm,0.8))
        R.append(ri)
        f=PosVi[1,0]+PosVi[1,1]
        
        if  f > 1 : 
            PosVi[1,0] , PosVi[1,1] = PosVi[1,0]/f , PosVi[1,1]/f
        
        classe_tab=classe_tab+[personne(PosVi[0,0],PosVi[0,1],PosVi[1,0]*v_max,PosVi[1,1]*v_max,ri,v_max,num_part)]
    
    classe_tab=np.array(classe_tab)
     
    #Ajout des personnes poteaux
    classe_tab = np.append(classe_tab,poteau)
    for part in poteau:
        PosVi_tab = np.append(PosVi_tab,[[part.x,part.y],[0,0]])
        PosVi_tab = PosVi_tab.reshape(len(classe_tab),2,2)
        R.append(part.r)
    
    #Replacement des personnes qui se superposent
    ls = np.arange(0,len(classe_tab))
    couple = list(itertools.combinations(ls,2))
    a=1 ; p=0
    
    while a!=0 and p<=100:
        
        a=0
        
        for ij in couple:
            
            i = ij[0]
            j = ij[1]
            #Test de superposition
            if classe_tab[i].superpose(classe_tab[j]):
                
                a=a+1
                classe_tab[i].x = rd.rand()*x+1
                classe_tab[i].y = rd.rand()*y+1
        p=p+1
    
    if p==101 :
        
        input('Trop de personnes dans la salle')
    for num_pers , pers in enumerate(classe_tab):
        
        PosVi_tab[num_pers,0,0]=pers.x
        PosVi_tab[num_pers,0,1]=pers.y
        
    a=0
    if Sim_forces:
        a=0.2
        
    def f1(pers) :
        return pers.y + (pers.r+a) >= 10

    def f2(pers) :
        return pers.y - (pers.r+a) <=0 

    def f3(pers) :
        return pers.x + (pers.r+a) >=10

    def f4(pers) :
        return pers.x - (pers.r+a) <=0

    vect1=np.array([1,0])

    vect2=np.array([1,0])

    vect3=np.array([0,1])

    vect4=np.array([0,1])

    sortie1 = np.array([[5,6],[0,0.5]])
    sortie2 = np.array([[5,6],[9.5,10]])

    mur_class_tab=np.array([mur(f1,vect1,sortie1),mur(f2,vect2),mur(f3,vect3),mur(f4,vect4)])

    return PosVi_tab , classe_tab , R , mur_class_tab

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





# def personne_poteau(x,y,r, PosVi_tab , classe_tab , rayon_autre):
#     """
#     Ajoute une personne avec un rayon r au coordonées x,y immobile à classe_tab
#     """
#     part = personne(x, y, 0, 0, r, 0, len(classe_tab))
#     classe_tab = np.append(classe_tab,personne(5,5,0,0,1,0,len(classe_tab)))
#     PosVi_tab = np.append(PosVi_tab,[[5,5],[0,0]])
#     PosVi_tab = PosVi_tab.reshape(len(classe_tab),2,2)
#     rayon_autre.append(r)
    
#     return classe_tab , PosVi_tab , rayon_autre


# def personne_poteau(x,y,r, PosVi_tab , classe_tab , rayon_autre):
#     """
#     Ajoute une personne avec un rayon r au coordonées x,y immobile à classe_tab
#     """
#     part = personne(x, y, 0, 0, r, 0, len(classe_tab))
#     classe_tab = np.append(classe_tab,personne(x,y,0,0,r,0,len(classe_tab)))
#     PosVi_tab = np.append(PosVi_tab,[[x,y],[0,0]])
#     PosVi_tab = PosVi_tab.reshape(len(classe_tab),2,2)
#     rayon_autre.append(r)
    
#     return classe_tab , PosVi_tab , rayon_autre
    

# %% Tests
if __name__ == '__main__':
    
    part1 = personne(0,0,0,0,1,1,0)
    part2 = personne(1,0,0,0,1,1,1)
    part3 = personne(1,1,0,0,1,1,2)
    
    classe_tab = np.array([part1,part2,part3])
        
        
        
        
        