#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Défini la classe et les fonctions liées au mur et la (les) sorties
"""


from personne_class import * 
import numpy as np

class mur:
    def __init__(self,f,vect,sortie):
        """
        f est la fonction représentative en fonction de x et y du mur
        """
        self.f = f
        self.vect=vect
        self.sortie = sortie
        
    def collision(self,particule):
        """
        Retourne true si la particule touche le mur
        """
        answer = self.f(particule.x , particule.y ) #== particule.y + particule.r
        return answer        
    
        
    def change_v_part(self,particule):
        """
        Change la vitesse la particule en lui supprimant sa composante 
        perpendiculaire au mur sauf si il est dans la zone de sortie
        """
        
        
        vect_mur = self.vect
        
        v_part = np.array([particule.vx , particule.vy])
        
        prod_sca = np.vdot(vect_mur,v_part)
        
        new_v = prod_sca * vect_mur
        
        return new_v
    
    def force_exit(self,particule):
        """
        Retourne la force qu'exerce la sortie sur une particule
        """
        
        pos_sortie = [np.mean(self.sortie[0]) , np.mean(self.sortie[1])]
        
        d = np.sqrt((pos_sortie[0]-particule.x)**2+(pos_sortie[1]-particule.y)**2)
        
        if d == 0:
            F = np.array([0,0])
            
        else :
            F = np.array([10,10])
            
        return F
    
    
        
        
        
        
        
        
    
    # def sortie(self,pos):
    #     """
    #     Defini la sortie du mur. La position pos est (xmin,xmax,ymin,ymax)
    #     le domaine de la sortie. La force de sortie est appliquée au point
    #     au centre de la sortie
    #     """
        
        
        
        
        
        
        
        
    
if __name__ == '__main__':
    
    def f(x):
        y = 3
        return y
    
    mur_test = mur(f)
    part = personne(2,2,1,1,1,1,0)
    collision = mur_test.collision(part)
    if collision == True:
        v = mur_test.change_v_part(part)
    
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
    
    mur_class_tab=np.array([mur(f1,vect1),mur(f2,vect2),mur(f3,vect3),mur(f4,vect4)])
    
    
