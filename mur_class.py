#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Défini la classe et les fonctions liées au mur et la (les) sorties
"""

# %% Importation des librairies
from personne_class import * 
import numpy as np

# %% Définition de la classe
class mur:
    def __init__(self,f,vect,sortie = None):
        """
        f est la fonction représentative en fonction de x et y du mur
        vect est le vecteur directeur du mur
        sortie est de la forme np.array([[xmin,xmax],[ymin,ymax]])
        """
        self.f = f
        self.vect=vect
        self.sortie = sortie
        
    def collision(self,pers):
        """
        Retourne true si la personne dépasse du mur
        """
        answer = self.f(pers)
        
        return answer
    
    def d_mur(self,particule):
        """
        Mesure la distance entre la particule et la sortie et le vecteur les rejoignant.
        """
        
        pos_sortie = [np.mean(self.sortie[0]) , np.mean(self.sortie[1])]
        v = np.array([pos_sortie[0]-particule.x,pos_sortie[1]-particule.y])
        norm_v = np.linalg.norm(v)
        
        return v , norm_v
    
    def handle_part_exit(self,part):
        """
        Retourne True si la particule sort
        """
        if np.all(self.sortie != None):
            if part.x >= self.sortie[0,0] and part.x <= self.sortie[0,1] and part.y >= self.sortie[1,0] and part.y <= self.sortie[1,1]:
                return True
        else: return False
        
    def force_exit(self,particule):
        """
        Retourne la force qu'exerce la sortie sur une particule
        """
        
        pos_sortie = [np.mean(self.sortie[0]) , np.mean(self.sortie[1])]
        v = np.array([pos_sortie[0]-particule.x,pos_sortie[1]-particule.y])
        norm_v = np.linalg.norm(v)
        
        if norm_v == 0:
            F = np.array([0,0])
            
        else :
            F = 10*v/norm_v
            
        return F
    


# %% Tests
if __name__ == '__main__':
    
    part = personne(2,2,1,1,1,1,0)
    
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
    
    sortie = np.array([[5,6],[0,0]])
    
    mur_class_tab=np.array([mur(f1,vect1),mur(f2,vect2),mur(f3,vect3),mur(f4,vect4,sortie)])
    
    tab_ans = []
    for mur in mur_class_tab:
        ans = mur.collision(part)
        tab_ans.append(ans)
        
    F_tab = tab_force_mur(mur_class_tab,[part])
    
    
