#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Definit la classe personne, la fonction permettant de calculer la force entre
deux particules et la fonction permettant de calculer le tableau de force entre
toutes les particules.
"""
import numpy as np
import numpy.random as rd
import itertools

class personne:
    """
    caractéristiques :
    position x,y
    vitesse vx,vy
    (mouvement oui ou non)
    rayon r
    masse m
    numéro de particule
    """
    def __init__(self,x,y,vx,vy,r,m,num):
        """Définition des parametre initiaux"""
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.r = r
        self.m = m
        self.num = num
        
    def distance(self,autre):
        """Retourne la distance entre la particule et une autre, sur l'axe x
        et y"""
        dx = self.x - autre.x
        dy = self.y - autre.y
        return np.sqrt(dx**2+dy**2),dx,dy
    
    def superpose(self,autre):
        """Retourne True si les deux particules se superposent"""
        answer = self.distance(autre) < self.r + autre.r
        return answer
    





#Définition d'un tableau avec l'ensemble des positions, des vitesses, 
#des accélérations et des forces de chaque particule.
# ligne = particule
# colonne 0 = x
# colonne 1 = y
# colonne 2 = vx
# colonne 3 = vy
# colonne  = x

#tab = 


def force(part1,part2,detection):
    """ 
    Retourne la force de repulsion entre la particule et une autre.
    Les particule en dehors du rayon de detection sont negligées
    """
    if part1.distance(part2)[0] < detection:
        
        if part1.distance(part2)[1] == 0: #Eviter une division par 0
            Fx = 0
        else:
            Fx = -1/part1.distance(part2)[1]**7 * part1.m * part2.m * 0.5
        
            
        if part1.distance(part2)[2] == 0: #Eviter une division par 0
            Fy = 0
        else:
            Fy = -1/part1.distance(part2)[2]**7 * part1.m * part2.m * 0.5
                
        F = np.array([Fx,Fy])
    
    else :
        F = np.zeros(2)
    
    
    return F

def tab_force(classe_tab,detection):
    """
    Retourne le tableau de force entre N particules = len(class_tab). 
    class_tab est le tableau des objets particules. 
    detecttion est le seuil de detection pour la force
    """
    F_tab_x = np.zeros((len(classe_tab),len(classe_tab)))
    F_tab_y = np.zeros((len(classe_tab),len(classe_tab)))
    ls = np.arange(0,len(classe_tab))
    couple = list(itertools.permutations(ls,2))
    for ij in couple:
        i = ij[0]
        j = ij[1]
        F_tab_x[i,j] = force(classe_tab[i],classe_tab[j],detection)[0]
        F_tab_y[i,j] = force(classe_tab[i],classe_tab[j],detection)[1]
    F_tab = np.array([F_tab_x,F_tab_y])
        
    return F_tab

def initial(n,x=1,y=1,vx=1,vy=1,r=1,m=1):
    PosVi_tab=rd.rand(n,2,2)
    PosVi_tab[:,0,0]=PosVi_tab[:,0,0]*x
    PosVi_tab[:,0,1]=PosVi_tab[:,0,1]*y
    PosVi_tab[:,1,0]=PosVi_tab[:,1,0]*vx
    PosVi_tab[:,1,1]=PosVi_tab[:,1,1]*vy
    classe_tab=[]
    j=0
    R=np.zeros(n)
    for i in PosVi_tab:
        
        mi=rd.rand()*m + 1
        ri=rd.rand()*r
        R[j]=ri
        classe_tab=classe_tab+[personne(i[0,0],i[0,1],i[1,0],i[1,1],ri,mi,j)]
        j=j+1
    classe_tab=np.array(classe_tab)
    return PosVi_tab , classe_tab , R

if __name__ == '__main__':
    
    part1 = personne(0,0,0,0,1,1,0)
    part2 = personne(1,0,0,0,1,1,1)
    part3 = personne(1,1,0,0,1,1,2)
    
    classe_tab = np.array([part1,part2,part3])
    
    F_tab = tab_force(classe_tab,10)
        
        
        
        
        