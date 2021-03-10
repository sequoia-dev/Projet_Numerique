#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 14:29:44 2020

@author: comecattin
"""
import numpy as np
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
    if part1.distance(part2) < detection:
        Fx = -1/part1.distance(part2)[1]**7 * part1.m * part2.m * 0.5
        Fy = -1/part1.distance(part2)[2]**7 * part1.m * part2.m * 0.5
        F = np.array([Fx,Fy])
    else :
        F = np.zeros(2)
    return F

def tab_force(N):
    """
    Retourne le tableau de force entre N particules.
    """
    F_tab = np.zeros((N,N))
    ls = np.arange(0,N)
    couple = list(itertools.permutations(ls,2))
    for ij in couple:
        i = ij[0]
        j = ij[1]
        F_tab[i,j] = force(part.num[i],part.num[j])
        pass
    
        
        
        
        
        
    
def change_vitesse(self,personne):
    """
    Change la vitesse de la particule quand il y a contact avec une autre
    """
    #Acceleration de la particule
    self.a = 1/self.m * self.sum_force() 
        
def sum_force():
    pass
        
        
        
        
        
        