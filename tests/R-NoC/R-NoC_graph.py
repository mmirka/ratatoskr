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

import xml_writers_adjMat as writers
import configure_AdjMat as configure
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

class RNoC_Graph():
    def __init__(self):
    
        self.pos_buffers=[]
        self.width=0.8
        self.pos_InputPorts=[]
        self.size_buffers = []
        self.nb_switchs = 0
        self.position_switchs = []
        self.nb_Lanes = 5
        self.para_ratio = 1
        self.modules=[]  
        self.nbModule = 0
        # self.creation()
        
    def add_module(self, module):
        self.modules.append(module)
        self.nbModule += 1
         
        
    # def creation(self):    #To Do _ fully create the R-NoC from parameters
        
    
    
    # def get_NetworkX_graph(self):    #To Do _ create corresponding NetworkX type graph
    
    # def get_AdjacencyMatrix(self):    #To Do _ gt adjacency matrix from networkx graph.
    
    def XML_writer(self, config_ini_path):    #To Do _ create the network.xml and config.xml file
        configuration = configure.Configuration(config_ini_path)

        writer = writers.ConfigWriter(configuration)
        writer.write_config('config/config.xml')

        writer = writers.NetworkWriter_RNoC(configuration, self.modules)
        writer.write_network('config/network.xml')
        
        
    
    def place_modules(self):
        
        size_lanes = np.zeros(self.nb_Lanes+1) # number of modules per lane
        cpt_lanes = np.zeros(self.nb_Lanes+1) # follow the number of modules placed
        delta_lanes  = np.zeros(self.nb_Lanes+1) # delta position on si x axis 
        if self.nb_Lanes <= 1:
            y_delta = 0
        else:
            y_delta = self.width/(self.nb_Lanes)
        
            
        for m in self.modules:
            lane = m.lane
            size_lanes[lane] += 1
            
        for i in range(self.nb_Lanes+1):
            if size_lanes[i] <= 1:
                delta_lanes[i] = 0
            else:
                delta_lanes[i] = self.width/(size_lanes[i]-1)
                
        cpt_module = 0
        for m in self.modules:
            m_lane = m.lane
            
            y_pos = m_lane*y_delta
            x_pos = cpt_lanes[m_lane]*delta_lanes[m_lane]
            
            self.modules[cpt_module].pos = [x_pos, y_pos, 0]
            
            cpt_lanes[m_lane] += 1
            cpt_module += 1
            
    def plot(self):
        fig = plt.figure()
        for m in self.modules:
            plt.scatter(m.pos[0], m.pos[1], s=50, c='b')
            label = "{:.0f}".format(m.id)
            plt.annotate(label, (m.pos[0], m.pos[1]), textcoords='offset points',xytext=(-5,-10), ha='center', c = 'r')
            for i in m.Next:
                if i == -1:
                    break
                for next in self.modules:
                    if next.id == i:
                        break
                x_l = [m.pos[0], next.pos[0]]
                y_l = [m.pos[1], next.pos[1]]
                plt.arrow(x_l[0], y_l[0], (x_l[1]-x_l[0]), (y_l[1]-y_l[0]), fc='k', ec='k',head_width=0.02, head_length=0.05,linewidth=1, length_includes_head=True)
                
            if m.id == self.nbModule-5:
                label = "South"
                plt.annotate(label, (m.pos[0], m.pos[1]), textcoords='offset points',xytext=(+5,+10), ha='center', c = 'g')
            elif m.id == self.nbModule-4:
                label = "East"
                plt.annotate(label, (m.pos[0], m.pos[1]), textcoords='offset points',xytext=(+5,+10), ha='center', c = 'g')
            elif m.id == self.nbModule-3:
                label = "North"
                plt.annotate(label, (m.pos[0], m.pos[1]), textcoords='offset points',xytext=(+5,+10), ha='center', c = 'g')
            elif m.id == self.nbModule-2:
                label = "West"
                plt.annotate(label, (m.pos[0], m.pos[1]), textcoords='offset points',xytext=(+5,+10), ha='center', c = 'g')
            elif m.id == self.nbModule-1:
                label = "Local"
                plt.annotate(label, (m.pos[0], m.pos[1]), textcoords='offset points',xytext=(+5,+10), ha='center', c = 'g')
            

        plt.axis('equal')
        #plt.grid()
        plt.show()
    
    
class Module():
    def __init__(self, ID, NodeType, lane, bufferSize):
        self.id = ID
        self.NodeType = NodeType
        self.Next = []
        self.Output = [] # if output controller
        self.bufferSize = bufferSize
        self.lane = lane    
        self.pos=[0,0,0]
    
def RNoC_byHand():
    RNoC = RNoC_Graph()
    
    
    # Circuit 0 _ West & Local inputs
    ## Lane 0
    InputController1 = Module(0,"InputController", 0, 1)
    InputController1.Next.append(1)
    RNoC.add_module(InputController1)
    
    Buffer1 = Module(1,"Buffer", 0, 4)
    Buffer1.Next.append(2)
    RNoC.add_module(Buffer1)
    
    OutputController1 = Module(2,"OutputController", 0, 1)
    OutputController1.Next.append(3)
    OutputController1.Next.append(68)
    OutputController1.Output.append("Local")
    RNoC.add_module(OutputController1)
    
    Buffer2 = Module(3,"Buffer", 0, 4)
    Buffer2.Next.append(4)
    RNoC.add_module(Buffer2)
    
    PathController1 = Module(4,"PathController", 0, 1)
    PathController1.Next.append(5)
    PathController1.Next.append(18)
    PathController1.Output.append("South")
    PathController1.Output.append("East")
    PathController1.Output.append("North")
    PathController1.Output.append("West")
    RNoC.add_module(PathController1)
    
    Buffer2 = Module(5,"Buffer", 0, 4)
    Buffer2.Next.append(6)
    RNoC.add_module(Buffer2)
    
    InputController2 = Module(6,"InputController", 0, 1)
    InputController2.Next.append(7)
    RNoC.add_module(InputController2)
    
    Buffer3 = Module(7,"Buffer", 0, 4)
    Buffer3.Next.append(8)
    RNoC.add_module(Buffer3)
    
    OutputController2 = Module(8,"OutputController", 0, 1)
    OutputController2.Next.append(9)
    OutputController2.Next.append(64)
    OutputController2.Output.append("South")
    RNoC.add_module(OutputController2)
    
    Buffer4 = Module(9,"Buffer", 0, 4)
    Buffer4.Next.append(10)
    RNoC.add_module(Buffer4)
    
    OutputController3 = Module(10,"OutputController", 0, 1)
    OutputController3.Next.append(11)
    OutputController3.Next.append(65)
    OutputController3.Output.append("East")
    RNoC.add_module(OutputController3)
    
    Buffer5 = Module(11,"Buffer", 0, 4)
    Buffer5.Next.append(12)
    RNoC.add_module(Buffer5)
    
    OutputController4 = Module(12,"OutputController", 0, 1)
    OutputController4.Next.append(13)
    OutputController4.Next.append(66)
    OutputController4.Output.append("North")
    RNoC.add_module(OutputController4)
    
    Buffer6 = Module(13,"Buffer", 0, 4)
    Buffer6.Next.append(14)
    RNoC.add_module(Buffer6)
    
    OutputController5 = Module(14,"OutputController", 0, 1)
    OutputController5.Next.append(15)
    OutputController5.Next.append(67)
    OutputController5.Output.append("West")
    RNoC.add_module(OutputController5)
    
    
    ## lane 3
    PathController2 = Module(15,"PathController", 3, 1)
    PathController2.Next.append(16)
    #PathController2.Output.append("South")
    #PathController2.Output.append("East")
    #PathController2.Output.append("North")
    #PathController2.Output.append("West")
    #PathController2.Output.append("Local")
    RNoC.add_module(PathController2)
    
    Buffer6 = Module(16,"Buffer", 3, 4)
    Buffer6.Next.append(17)
    RNoC.add_module(Buffer6)
    
    OutputController6 = Module(17,"OutputController", 3, 1)
    OutputController6.Next.append(18)
    OutputController6.Next.append(68)
    OutputController6.Output.append("Local")
    RNoC.add_module(OutputController6)
    
    Mux1 = Module(18,"Mux", 3, 1)
    Mux1.Next.append(19)
    RNoC.add_module(Mux1)
    
    Buffer7 = Module(19,"Buffer", 3, 4)
    Buffer7.Next.append(20)
    RNoC.add_module(Buffer7)
    
    OutputController7 = Module(20,"OutputController", 3, 1)
    OutputController7.Next.append(21)
    OutputController7.Next.append(64)
    OutputController7.Output.append("South")
    RNoC.add_module(OutputController7)
    
    Buffer8 = Module(21,"Buffer", 3, 4)
    Buffer8.Next.append(22)
    RNoC.add_module(Buffer8)
    
    OutputController8 = Module(22,"OutputController", 3, 1)
    OutputController8.Next.append(23)
    OutputController8.Next.append(65)
    OutputController8.Output.append("East")
    RNoC.add_module(OutputController8)
    
    Buffer9 = Module(23,"Buffer", 3, 4)
    Buffer9.Next.append(24)
    RNoC.add_module(Buffer9)
    
    OutputController9 = Module(24,"OutputController", 3, 1)
    OutputController9.Next.append(25)
    OutputController9.Next.append(66)
    OutputController9.Output.append("North")
    RNoC.add_module(OutputController9)
    
    Buffer10 = Module(25,"Buffer", 3, 4)
    Buffer10.Next.append(26)
    RNoC.add_module(Buffer10)
    
    OutputController10 = Module(26,"OutputController", 3, 1)
    OutputController10.Next.append(67) # end circuit 0
    OutputController10.Output.append("West")
    RNoC.add_module(OutputController10)
    
    # Circuit 1 _ North input
    ## lane 1
    InputController3 = Module(27,"InputController", 1, 1)
    InputController3.Next.append(28)
    RNoC.add_module(InputController3)
    
    Buffer11 = Module(28,"Buffer", 1, 4)
    Buffer11.Next.append(29)
    RNoC.add_module(Buffer11)
    
    OutputController11 = Module(29,"OutputController", 1, 1)
    OutputController11.Next.append(30)
    OutputController11.Next.append(67)
    OutputController11.Output.append("West")
    RNoC.add_module(OutputController11)
    
    Buffer12 = Module(30,"Buffer", 1, 4)
    Buffer12.Next.append(31)
    RNoC.add_module(Buffer12)
    
    OutputController12 = Module(31,"OutputController", 1, 1)
    OutputController12.Next.append(32)
    OutputController12.Next.append(68)
    OutputController12.Output.append("Local")
    RNoC.add_module(OutputController12)
    
    Buffer13 = Module(32,"Buffer", 1, 4)
    Buffer13.Next.append(33)
    RNoC.add_module(Buffer13)
    
    OutputController13 = Module(33,"OutputController", 1, 1)
    OutputController13.Next.append(34)
    OutputController13.Next.append(64)
    OutputController13.Output.append("South")
    RNoC.add_module(OutputController13)
    
    Buffer14 = Module(34,"Buffer", 1, 4)
    Buffer14.Next.append(35)
    RNoC.add_module(Buffer14)
    
    OutputController14 = Module(35,"OutputController", 1, 1)
    OutputController14.Next.append(36) 
    OutputController14.Next.append(65)
    OutputController14.Output.append("East")
    RNoC.add_module(OutputController14)
    
    Buffer1400 = Module(36,"Buffer", 1, 4)
    Buffer1400.Next.append(37)
    RNoC.add_module(Buffer1400)
    
    OutputController1400 = Module(37,"OutputController", 1, 1)
    OutputController1400.Next.append(66) # end circuit 1
    OutputController1400.Output.append("North")
    RNoC.add_module(OutputController1400)
    
    
    # Circuit 2 _ South & East inputs
    ## Lane 2
    InputController4 = Module(38,"InputController", 2, 1)
    InputController4.Next.append(39)
    RNoC.add_module(InputController4)
    
    Buffer15 = Module(39,"Buffer", 2, 4)
    Buffer15.Next.append(40)
    RNoC.add_module(Buffer15)
    
    OutputController15 = Module(40,"OutputController", 2, 1)
    OutputController15.Next.append(41)
    OutputController15.Next.append(65)
    OutputController15.Output.append("East")
    RNoC.add_module(OutputController15)
    
    Buffer16 = Module(41,"Buffer", 2, 4)
    Buffer16.Next.append(42)
    RNoC.add_module(Buffer16)
    
    InputController5 = Module(42,"InputController", 2, 1)
    InputController5.Next.append(43)
    RNoC.add_module(InputController5)
    
    Buffer17 = Module(43,"Buffer", 2, 4)
    Buffer17.Next.append(44)
    RNoC.add_module(Buffer17)
    
    OutputController16 = Module(44,"OutputController", 2, 1)
    OutputController16.Next.append(45)
    OutputController16.Next.append(66)
    OutputController16.Output.append("North")
    RNoC.add_module(OutputController16)
    
    Buffer18 = Module(45,"Buffer", 2, 4)
    Buffer18.Next.append(46)
    RNoC.add_module(Buffer18)
    
    PathController3 = Module(46,"PathController", 2, 1)
    PathController3.Next.append(47)
    PathController3.Next.append(57)
    PathController3.Output.append("South")
    PathController3.Output.append("West")
    PathController3.Output.append("Local")
    RNoC.add_module(PathController3)
    
    Buffer19 = Module(47,"Buffer", 2, 4)
    Buffer19.Next.append(48)
    RNoC.add_module(Buffer19)
    
    OutputController17 = Module(48,"OutputController", 2, 1)
    OutputController17.Next.append(49)
    OutputController17.Next.append(67)
    OutputController17.Output.append("West")
    RNoC.add_module(OutputController17)
    
    Buffer20 = Module(49,"Buffer", 2, 4)
    Buffer20.Next.append(50)
    RNoC.add_module(Buffer20)
    
    OutputController18 = Module(50,"OutputController", 2, 1)
    OutputController18.Next.append(51)
    OutputController18.Next.append(68)
    OutputController18.Output.append("Local")
    RNoC.add_module(OutputController18)
    
    Buffer21 = Module(51,"Buffer", 2, 4)
    Buffer21.Next.append(52)
    RNoC.add_module(Buffer21)
    
    OutputController19 = Module(52,"OutputController", 2, 1)
    OutputController19.Next.append(53)
    OutputController19.Next.append(64)
    OutputController19.Output.append("South")
    RNoC.add_module(OutputController19)
    
    
    ## lane 4  A FAIRE ###################################################################################
    Buffer22 = Module(53,"Buffer", 4, 4)
    Buffer22.Next.append(54)
    RNoC.add_module(Buffer22)
    
    OutputController20 = Module(54,"OutputController", 4, 1)
    OutputController20.Next.append(55)
    OutputController20.Next.append(65)
    OutputController20.Output.append("East")
    RNoC.add_module(OutputController20)
    
    Buffer23 = Module(55,"Buffer", 4, 4)
    Buffer23.Next.append(56)
    RNoC.add_module(Buffer23)
    
    OutputController21 = Module(56,"OutputController", 4, 1)
    OutputController21.Next.append(57)
    OutputController21.Next.append(66)
    OutputController21.Output.append("North")
    RNoC.add_module(OutputController21)
    
    Mux2 = Module(57,"Mux", 4, 1)
    Mux2.Next.append(58)
    RNoC.add_module(Mux2)
    
    Buffer24 = Module(58,"Buffer", 4, 4)
    Buffer24.Next.append(59)
    RNoC.add_module(Buffer24)
    
    OutputController22 = Module(59,"OutputController", 4, 1)
    OutputController22.Next.append(60)
    OutputController22.Next.append(67)
    OutputController22.Output.append("West")
    RNoC.add_module(OutputController22)
    
    Buffer25 = Module(60,"Buffer", 4, 4)
    Buffer25.Next.append(61)
    RNoC.add_module(Buffer25)
    
    OutputController23 = Module(61,"OutputController", 4, 1)
    OutputController23.Next.append(62)
    OutputController23.Next.append(68)
    OutputController23.Output.append("Local")
    RNoC.add_module(OutputController23)
    
    Buffer26 = Module(62,"Buffer", 4, 4)
    Buffer26.Next.append(63)
    RNoC.add_module(Buffer26)
    
    OutputController24 = Module(63,"OutputController", 4, 1)
    OutputController24.Next.append(64)
    OutputController24.Output.append("South")
    RNoC.add_module(OutputController24)
    
    # Output MUX
    # South
    Mux3 = Module(64,"Mux", 5, 1)
    Mux3.Next.append(-1)
    RNoC.add_module(Mux3)
    
    # East
    Mux4 = Module(65,"Mux", 5, 1)
    Mux4.Next.append(-1)
    RNoC.add_module(Mux4)
    
    # North
    Mux5 = Module(66,"Mux", 5, 1)
    Mux5.Next.append(-1)
    RNoC.add_module(Mux5)
    
    # West
    Mux6 = Module(67,"Mux", 5, 1)
    Mux6.Next.append(-1)
    RNoC.add_module(Mux6)
    
    # Local
    Mux7 = Module(68,"Mux", 5, 1)
    Mux7.Next.append(-1)
    RNoC.add_module(Mux7)
    
    return RNoC
    

def main():

    RNoC = RNoC_byHand()
    
    RNoC.place_modules()
    
    RNoC.plot()
    
    RNoC.XML_writer('config.ini')
###############################################################################


if __name__ == "__main__":
    main()
