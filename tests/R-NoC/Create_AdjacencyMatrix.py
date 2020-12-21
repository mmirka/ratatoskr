#!/bin/python

# Copyright 2018 Jan Moritz Joseph

# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# This script generates simple topology files for 2D or 3D meshes
###############################################################################
import sys
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
import configparser
from copy import deepcopy
import math
from math import pi
###############################################################################
# Global variables

#nbLanes = 2
#nbPorts = 5
#NoC_x = 2
#NoC_y = 2
#nbRouters_NoC = NoC_x * NoC_y # mesh
#nbRouters_Roundabout = (nbLanes + 1) * nbPorts + 1
#nbRouters_R_NoC = nbRouters_NoC * nbRouters_Roundabout
#in_local = 2 # input router for the local port
#nbOutputs = 2 # a router can switch or continue (except for the last one of the last lane)

###### Fonctions Adjacency Matrices (AMs)
class AdjMat_Creator():
    def __init__(self):
        self.nbLanes = 2
        self.nbPorts = 5
        self.NoC_x = 2
        self.NoC_y = 2
        self.nbRouters_NoC = self.NoC_x * self.NoC_y # mesh
        self.nbRouters_Roundabout = (self.nbLanes + 1) * self.nbPorts + 1
        self.nbRouters_R_NoC = self.nbRouters_NoC * self.nbRouters_Roundabout
        self.in_local = 2    
    ## Roundabout router AM
    def Roundabout_AM(self):
        # mat[src, dest]
        mat = np.zeros((self.nbRouters_Roundabout, self.nbRouters_Roundabout))
        # local I/O:
        mat[0, self.in_local] = 1
        mat[self.nbLanes*self.nbPorts+self.nbLanes, 0] = 1
        # the lanes:
        for i in range(self.nbLanes):
            for j in range(self.nbPorts):
                idx_src = j + i*self.nbPorts + 1
                
                idx_dest_out = (self.nbLanes*self.nbPorts + (idx_src%self.nbPorts) + 1)%(self.nbRouters_Roundabout)
                idx_dest_next = (idx_src + 1)%(self.nbRouters_Roundabout)
                
                mat[idx_src, idx_dest_next] = 2    # lower priority
                mat[idx_src, idx_dest_out] = 1   # higher priority --> if next == out : higher priority
        # the rest
        return mat
   
    ## Macro-Network AM
    def NoC_AM(self): # classic mesh connections
         mat = np.zeros((self.nbRouters_NoC, self.nbRouters_NoC))
         for i in range(self.nbRouters_NoC):
             for j in range(self.nbRouters_NoC):
                 if (((j == i+1) and (j%self.NoC_x != 0)) or ((j == i-1) and (i%self.NoC_x != 0))) or ((j == i+self.NoC_x) or (j == i-self.NoC_x)):
                     mat[i,j] = 1
                     
         return mat

    ## Roundabout network AM
    def R_NoC_AM(self):
        R_mat = self.Roundabout_AM()
        NoC_mat = self.NoC_AM()
        mat = np.zeros((self.nbRouters_R_NoC, self.nbRouters_R_NoC))
        # 1. copy R_mat in R_NoC_mat for all NoC routers
        for i in range(self.nbRouters_NoC): 
            for j in range(self.nbRouters_Roundabout):
                for k in range(self.nbRouters_Roundabout):
                    id_src_mat = i*self.nbRouters_Roundabout + j
                    id_dest_mat = i*self.nbRouters_Roundabout + k
                    mat[id_src_mat, id_dest_mat] = R_mat[j,k]
    
        # 2. Complete connections between NoC routers (roundabouts)
        for i in range(self.nbRouters_NoC):
            for j in range(self.nbRouters_NoC):
                if NoC_mat[i,j] == 1: # connections between roundabout
                    # determine if it is a N/S connection, S/N connection, E/W connection or W/E connection i.e. mesh
                    if j == i+1: # E/W connection
                        id_src = i*self.nbRouters_Roundabout + 14 
                        id_dest = j*self.nbRouters_Roundabout + 1
                        mat[id_src, id_dest] = 1    
                
                    elif j == i-1: # W/E connection
                        id_src = i*self.nbRouters_Roundabout + 11 
                        id_dest = j*self.nbRouters_Roundabout + 4
                        mat[id_src, id_dest] = 1
                    
                    elif j == i+self.NoC_x: # N/S connection
                        id_src = i*self.nbRouters_Roundabout + 15 
                        id_dest = j*self.nbRouters_Roundabout + 3
                        mat[id_src, id_dest] = 1
                    
                    elif j == i-self.NoC_x: # S/N connection
                        id_src = i*self.nbRouters_Roundabout + 13 
                        id_dest = j*self.nbRouters_Roundabout + 5
                        mat[id_src, id_dest] = 1
                    else:
                        print("Error connection")

        return mat



def main():

    AM = AdjMat_Creator()
    np.set_printoptions(threshold=sys.maxsize)
    
    R_mat = AM.Roundabout_AM()
    print(R_mat)
    
    NoC_mat = AM.NoC_AM()
    print(NoC_mat)
    
    R_NoC_mat = AM.R_NoC_AM()
    #print(R_NoC_mat)
    print(R_NoC_mat[16,18])
    print(R_NoC_mat[34,35])
    print(R_NoC_mat[34,45])
###############################################################################


if __name__ == "__main__":
    main()
