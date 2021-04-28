# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 13:39:15 2021

@author: piere
"""
import numpy as np
import numpy.random as rd

def initial(n,x=1,y=1,vx=1,vy=1,r=1,m=1):
    PosVi_tab=rd.rand(n,2,2)
    PosVi_tab[:,0,0]=PosVi_tab[:,0,0]*x
    PosVi_tab[:,0,1]=PosVi_tab[:,0,1]*y
    PosVi_tab[:,1,0]=PosVi_tab[:,1,0]*vx
    PosVi_tab[:,1,1]=PosVi_tab[:,1,1]*vy
    classe_tab=[]
    j=0
    for i in PosVi_tab:
        
        mi=rd.rand()*m
        ri=rd.rand()*r
        classe_tab=classe_tab+[personne(i[0,0],i[0,1],i[1,0],i[1,1],ri,mi,j)]
        j=j+1
    classe_tab=np.array(classe_tab)
    return PosVi_tab , classe_tab

