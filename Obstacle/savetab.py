#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Permet de lire et d'écrire les tableau dans un fichier au fur et à mesure du temps
"""

import numpy as np

def savefile(tab, name_pos='tab_pos.txt',name_vitesse='tab_vitesse.txt'):
    """
    Sauvegarde le np.array tab dans les fichier name_pos et name_vitesse
    """
    with open(name_pos,'a') as f_pos:
        f_pos.write("\n")
        pos = tab[:,0,:]
        np.savetxt(f_pos,pos)
        
    with open(name_vitesse,'a') as f_vitesse:
        f_vitesse.write("\n")
        vitesse = tab[:,1,:]
        np.savetxt(f_vitesse,vitesse)
        

def readfile(name_pos='tab_pos.txt',name_vitesse='tab_vitesse.txt'):
    """
    Retourne les tableaux contenus dans les tab.txt, sauvegardés avec savefile
    """
    tab_pos = np.loadtxt(name_pos)
    tab_vitesse = np.loadtxt(name_vitesse)
    
    return tab_pos , tab_vitesse

if __name__ == '__main__':
    a = np.arange(0,3)
    b = np.arange(3,6)
    savefile(a)
    savefile(b)
    
    tab = readfile()