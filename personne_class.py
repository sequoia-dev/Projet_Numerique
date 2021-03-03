#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 14:29:44 2020

@author: comecattin
"""
import numpy as np

class personne:
    """
    caractéristiques :
    position x,y
    vitesse vx,vy
    (mouvement oui ou non)
    rayon r
    masse m
    """
    def __init__(self,x,y,vx,vy,r,m):
        """Définition des parametre initiaux"""
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.r = r
        self.m = m
        
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
    
    def force(self,autre,detection):
        """ 
        Retourne la force de repulsion entre la particule et une autre.
        Les particule en dehors du rayon de detection sont negligées
        """
        if self.distance(autre) < detection:
            Fx = -1/self.distance(autre)[1]**7 * self.m * autre.m * 0.5
            Fy = -1/self.distance(autre)[2]**7 * self.m * autre.m * 0.5
            F = np.array([Fx,Fy])
        else :
            F = np.zeros(2)
        return F
        
        
        
        
        
    
    def change_vitesse(self,personne):
        """
        Change la vitesse de la particule quand il y a contact avec une autre
        """
        #Acceleration de la particule
        self.a = 1/self.m * self.sum_force() 
        
def sum_force():
    pass
        
        
        
        
        
        