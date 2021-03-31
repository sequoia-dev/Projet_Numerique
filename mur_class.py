#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Défini la classe et les fonctions liées au mur et la (les) sorties
"""


from personne_class import * 
import numpy as np

class mur:
    def __init__(self,f):
        """
        f est la fonction représentative en fonction de x et y du mur
        """
        self.f = f
        
    def collision(self,particule):
        """
        Retourne true si la particule touche le mur
        """
        answer = self.f(particule.x) == particule.y + particule.r
        return answer        
        
        
    def change_v_part(self,particule,dpos = np.array([1e-3,1e-3])):
        """
        Change la vitesse la particule en lui supprimant sa composante 
        perpendiculaire au mur
        """
        
        vect_mury = self.f(particule.x + dpos[0]) - self.f(particule.x)
        vect_murx = dpos[0]
        vect_mur = np.array([vect_murx,vect_mury])
        
        v_part = np.array([particule.vx , particule.vy])
        
        prod_sca = np.vdot(vect_mur,v_part)
        
        new_v = prod_sca * vect_mur
        
        return new_v
        
    
if __name__ == '__main__':
    
    def f(x):
        y = 3
        return y
    
    mur_test = mur(f)
    part = personne(2,2,1,1,1,1,0)
    collision = mur_test.collision(part)
    if collision == True:
        v = mur_test.change_v_part(part)
    
    
    
