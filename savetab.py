#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Permet de lire et d'écrire les tableau dans un fichier au fur et à mesure du temps
"""

import numpy as np

def savefile(tab, name='tab.txt'):
    """
    Sauvegarde le np.array tab dans le fichier name
    """
    with open(name,'a') as f:
        f.write("\n")
        np.savetxt(f,tab)
        
def readfile(name='tab.txt'):
    """
    Retourne les tableaux contenus dans tab.txt, sauvegardés avec savefile
    """
    tab = np.loadtxt(name)
    
    return tab






if __name__ == '__main__':
    a = np.arange(0,3)
    b = np.arange(3,6)
    savefile(a)
    savefile(b)
    
    tab = readfile()