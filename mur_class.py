#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Défini la classe et les fonctions liées au mur et la (les) sorties
"""


from personne_class import * 
import numpy as np

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
        v = np.array([pos_sortie[0]-particule.x,pos_sortie[1]-particule.y])
        norm_v = np.linalg.norm(v)
        
        if norm_v == 0:
            F = np.array([0,0])
            
        else :
            F = 10 * v/norm_v
            
        return F
    
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
    
    
