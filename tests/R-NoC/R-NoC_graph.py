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
    
        # Mesh parameters
        self.NoC_x = 2
        self.NoC_y = 2
        self.NoC_nbR = self.NoC_x*self.NoC_y
        self.pos = [0,0]
    
        # RNoC parameters
        self.pos_buffers=[]
        self.width=0.8
        self.pos_InputPorts=[]
        self.size_buffers = []
        self.nb_switchs = 0
        self.position_switchs = []
        #self.nb_Lanes = 5
        self.nb_Lanes = 3
        self.para_ratio = 1
        self.modules=[]  
        self.nbModule = 0
        self.MuxDirOrder=["Local","South","East","North","West"] # direction of mux in ouput lane
        
        #self.InputDict = {"West":0,"Local":6,"North":27,"South":38,"East":42}
        #self.OutputDict = {"West":67,"Local":68,"North":66,"South":64,"East":65}
        self.InputDict = {"West":0,"Local":4,"North":13,"South":24,"East":28}
        self.OutputDict = {"West":40,"Local":41,"North":39,"South":37,"East":38}
        
        
        
        # self.creation()
        
    def add_module(self, module):
        self.modules.append(module)
        self.nbModule += 1
         
        
    # def creation(self):    #To Do _ fully create the R-NoC from parameters
        
    
    
    # def get_NetworkX_graph(self):    #To Do _ create corresponding NetworkX type graph
    
    # def get_AdjacencyMatrix(self):    #To Do _ gt adjacency matrix from networkx graph.
    
## Lane options
# IC|B|PC|B|M|B| OC |B|PC|B|IC|B|M|B| OC |B|PC|B|IC|B|M|B| OC |B|PC|B|IC|B|M|B| OC |B|PC|B|IC|B|M|B| OC
    def creation(self):    #To Do _ fully create the R-NoC from parameters
        ## 1/ Initialise roundabout table
        RdTable = []
        for i in range(self.nb_Lanes):
            RdTable.append([])
            for j in range(30):
                RdTable[i].append(Module(-1, "", i, -1))
                
        ## 2/ place buffers
        idx_buffer = 0
        for pos in self.pos_buffers:
            b_lane = pos[0]
            b_place = pos[1]
            b_size = self.size_buffers[idx_buffer]
            RdTable[b_lane][b_place].NodeType = "Buffer"
            RdTable[b_lane][b_place].bufferSize = b_size
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            idx_buffer+=1
            
 #   self.id = ID
 #       self.NodeType = NodeType
 #       self.Next = []
 #       self.Output = [] # if output controller
 #       self.bufferSize = bufferSize
 #       self.lane = lane    
 #       self.pos=[0,0,0]
    
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

class NoC_RNoC():
    def __init__(self, nX, nY, RNoC_model_creator):
        self.nbX = nX
        self.nbY = nY
        self.nbRNoC = nX*nY
        self.RNoC_creator = RNoC_model_creator
        self.RNoC_model = self.RNoC_creator()
        self.RNoCs = []
        self.modules = []
        self.nbModules = self.nbRNoC*self.RNoC_model.nbModule
        self.localSRC = self.RNoC_model.InputDict["Local"]
        self.localDST = self.RNoC_model.OutputDict["Local"]
        
        self.create_NoC()
        
    def create_NoC(self):
        ## Create all RNoC
        for i in range(self.nbRNoC):
            RNoC_to_add = self.RNoC_creator()
            RNoC_to_add.place_modules()
            self.RNoCs.append(RNoC_to_add)
            
            ## update ids
            id_offset = i*self.RNoC_model.nbModule
            
            for m in RNoC_to_add.modules:
                m.id = m.id+id_offset
                for j in range(len(m.Next)):
                    m.Next[j] += id_offset
                self.modules.append(m)
                
        ## Complete RNoC positions
        for i in range(self.nbY):
            for j in range(self.nbX):
                index_RNoC = j+i*self.nbX
                posx = j
                posy = i
                print("RNoC ",index_RNoC, " position: x=",posx, " y=",posy) 
                self.RNoCs[index_RNoC].pos[0] = posx
                self.RNoCs[index_RNoC].pos[1] = posy
        
        ## Complete connections
        for i in range(self.nbRNoC):
            for j in range(self.nbRNoC): 
                id_offset_i = i*self.RNoC_model.nbModule
                id_offset_j = j*self.RNoC_model.nbModule
            
                if i==j:
                    pass
                else:
                    if self.RNoCs[i].pos[0] == self.RNoCs[j].pos[0]: # same column
                        if self.RNoCs[i].pos[1] == self.RNoCs[j].pos[1]+1: # direction N->S / i->j / connection S->N
                            local_src_id = self.RNoC_model.OutputDict["South"]
                            local_dst_id = self.RNoC_model.InputDict["North"]
                            src_id = local_src_id+id_offset_i
                            dst_id = local_dst_id+id_offset_j
                            self.modules[src_id].Next.append(dst_id)
                            
                        elif self.RNoCs[i].pos[1] == self.RNoCs[j].pos[1]-1: # direction S->N / i->j / connection N->S
                            local_src_id = self.RNoC_model.OutputDict["North"]
                            local_dst_id = self.RNoC_model.InputDict["South"]
                            src_id = local_src_id+id_offset_i
                            dst_id = local_dst_id+id_offset_j
                            self.modules[src_id].Next.append(dst_id)
                        
                        else:
                            pass
                    
                    if self.RNoCs[i].pos[1] == self.RNoCs[j].pos[1]: # same row
                        if self.RNoCs[i].pos[0] == self.RNoCs[j].pos[0]+1: # direction E->W / i->j / connection W->E
                            local_src_id = self.RNoC_model.OutputDict["West"]
                            local_dst_id = self.RNoC_model.InputDict["East"]
                            src_id = local_src_id+id_offset_i
                            dst_id = local_dst_id+id_offset_j
                            self.modules[src_id].Next.append(dst_id)
                            
                        elif self.RNoCs[i].pos[0] == self.RNoCs[j].pos[0]-1: # direction W->E / i->j / connection E->W
                            local_src_id = self.RNoC_model.OutputDict["East"]
                            local_dst_id = self.RNoC_model.InputDict["West"]
                            src_id = local_src_id+id_offset_i
                            dst_id = local_dst_id+id_offset_j
                            self.modules[src_id].Next.append(dst_id)
                            
                        else:
                            pass
                            
        ## Complete modules positions
        for i in range(len(self.modules)):
            RNoC_id = self.modules[i].id//self.RNoC_model.nbModule
            #print("NoC_moduleID = ", self.modules[i].id, " _ RNoC ID = ", RNoC_id)
            self.modules[i].pos[0] += self.RNoCs[RNoC_id].pos[0]
            self.modules[i].pos[1] += self.RNoCs[RNoC_id].pos[1]
            
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
            

        plt.axis('equal')
        #plt.grid()
        plt.show() 
                
    def XML_writer(self, config_ini_path):    #To Do _ create the network.xml and config.xml file
        configuration = configure.Configuration(config_ini_path)

        writer = writers.ConfigWriter(configuration)
        writer.write_config('config/config.xml')

        writer = writers.NetworkWriter_RNoC(configuration, self.modules, self.localSRC, self.localDST, self.nbRNoC)
        writer.write_network('config/network.xml')


    
    
def RNoC_byHand():
    RNoC = RNoC_Graph()
    s_buf = 32
    
    # Circuit 0 _ West & Local inputs
    ## Lane 0
    InputController1 = Module(0,"InputController", 0, 1)
    InputController1.Next.append(1)
    RNoC.add_module(InputController1)
    
    Buffer1 = Module(1,"Buffer", 0, s_buf)
    Buffer1.Next.append(2)
    RNoC.add_module(Buffer1)
    
    OutputController1 = Module(2,"OutputController", 0, 1)
    OutputController1.Next.append(3)
    OutputController1.Next.append(68)
    OutputController1.Output.append("Local")
    RNoC.add_module(OutputController1)
    
    Buffer2 = Module(3,"Buffer", 0, s_buf)
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
    
    Buffer2 = Module(5,"Buffer", 0, s_buf)
    Buffer2.Next.append(6)
    RNoC.add_module(Buffer2)
    
    InputController2 = Module(6,"InputController", 0, 1)
    InputController2.Next.append(7)
    RNoC.add_module(InputController2)
    
    Buffer3 = Module(7,"Buffer", 0, s_buf)
    Buffer3.Next.append(8)
    RNoC.add_module(Buffer3)
    
    OutputController2 = Module(8,"OutputController", 0, 1)
    OutputController2.Next.append(9)
    OutputController2.Next.append(64)
    OutputController2.Output.append("South")
    RNoC.add_module(OutputController2)
    
    Buffer4 = Module(9,"Buffer", 0, s_buf)
    Buffer4.Next.append(10)
    RNoC.add_module(Buffer4)
    
    OutputController3 = Module(10,"OutputController", 0, 1)
    OutputController3.Next.append(11)
    OutputController3.Next.append(65)
    OutputController3.Output.append("East")
    RNoC.add_module(OutputController3)
    
    Buffer5 = Module(11,"Buffer", 0, s_buf)
    Buffer5.Next.append(12)
    RNoC.add_module(Buffer5)
    
    OutputController4 = Module(12,"OutputController", 0, 1)
    OutputController4.Next.append(13)
    OutputController4.Next.append(66)
    OutputController4.Output.append("North")
    RNoC.add_module(OutputController4)
    
    Buffer6 = Module(13,"Buffer", 0, s_buf)
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
    
    Buffer6 = Module(16,"Buffer", 3, s_buf)
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
    
    Buffer7 = Module(19,"Buffer", 3, s_buf)
    Buffer7.Next.append(20)
    RNoC.add_module(Buffer7)
    
    OutputController7 = Module(20,"OutputController", 3, 1)
    OutputController7.Next.append(21)
    OutputController7.Next.append(64)
    OutputController7.Output.append("South")
    RNoC.add_module(OutputController7)
    
    Buffer8 = Module(21,"Buffer", 3, s_buf)
    Buffer8.Next.append(22)
    RNoC.add_module(Buffer8)
    
    OutputController8 = Module(22,"OutputController", 3, 1)
    OutputController8.Next.append(23)
    OutputController8.Next.append(65)
    OutputController8.Output.append("East")
    RNoC.add_module(OutputController8)
    
    Buffer9 = Module(23,"Buffer", 3, s_buf)
    Buffer9.Next.append(24)
    RNoC.add_module(Buffer9)
    
    OutputController9 = Module(24,"OutputController", 3, 1)
    OutputController9.Next.append(25)
    OutputController9.Next.append(66)
    OutputController9.Output.append("North")
    RNoC.add_module(OutputController9)
    
    Buffer10 = Module(25,"Buffer", 3, s_buf)
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
    
    Buffer11 = Module(28,"Buffer", 1, s_buf)
    Buffer11.Next.append(29)
    RNoC.add_module(Buffer11)
    
    OutputController11 = Module(29,"OutputController", 1, 1)
    OutputController11.Next.append(30)
    OutputController11.Next.append(67)
    OutputController11.Output.append("West")
    RNoC.add_module(OutputController11)
    
    Buffer12 = Module(30,"Buffer", 1, s_buf)
    Buffer12.Next.append(31)
    RNoC.add_module(Buffer12)
    
    OutputController12 = Module(31,"OutputController", 1, 1)
    OutputController12.Next.append(32)
    OutputController12.Next.append(68)
    OutputController12.Output.append("Local")
    RNoC.add_module(OutputController12)
    
    Buffer13 = Module(32,"Buffer", 1, s_buf)
    Buffer13.Next.append(33)
    RNoC.add_module(Buffer13)
    
    OutputController13 = Module(33,"OutputController", 1, 1)
    OutputController13.Next.append(34)
    OutputController13.Next.append(64)
    OutputController13.Output.append("South")
    RNoC.add_module(OutputController13)
    
    Buffer14 = Module(34,"Buffer", 1, s_buf)
    Buffer14.Next.append(35)
    RNoC.add_module(Buffer14)
    
    OutputController14 = Module(35,"OutputController", 1, 1)
    OutputController14.Next.append(36) 
    OutputController14.Next.append(65)
    OutputController14.Output.append("East")
    RNoC.add_module(OutputController14)
    
    Buffer1400 = Module(36,"Buffer", 1, s_buf)
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
    
    Buffer15 = Module(39,"Buffer", 2, s_buf)
    Buffer15.Next.append(40)
    RNoC.add_module(Buffer15)
    
    OutputController15 = Module(40,"OutputController", 2, 1)
    OutputController15.Next.append(41)
    OutputController15.Next.append(65)
    OutputController15.Output.append("East")
    RNoC.add_module(OutputController15)
    
    Buffer16 = Module(41,"Buffer", 2, s_buf)
    Buffer16.Next.append(42)
    RNoC.add_module(Buffer16)
    
    InputController5 = Module(42,"InputController", 2, 1)
    InputController5.Next.append(43)
    RNoC.add_module(InputController5)
    
    Buffer17 = Module(43,"Buffer", 2, s_buf)
    Buffer17.Next.append(44)
    RNoC.add_module(Buffer17)
    
    OutputController16 = Module(44,"OutputController", 2, 1)
    OutputController16.Next.append(45)
    OutputController16.Next.append(66)
    OutputController16.Output.append("North")
    RNoC.add_module(OutputController16)
    
    Buffer18 = Module(45,"Buffer", 2, s_buf)
    Buffer18.Next.append(46)
    RNoC.add_module(Buffer18)
    
    PathController3 = Module(46,"PathController", 2, 1)
    PathController3.Next.append(47)
    PathController3.Next.append(57)
    PathController3.Output.append("South")
    PathController3.Output.append("West")
    PathController3.Output.append("Local")
    RNoC.add_module(PathController3)
    
    Buffer19 = Module(47,"Buffer", 2, s_buf)
    Buffer19.Next.append(48)
    RNoC.add_module(Buffer19)
    
    OutputController17 = Module(48,"OutputController", 2, 1)
    OutputController17.Next.append(49)
    OutputController17.Next.append(67)
    OutputController17.Output.append("West")
    RNoC.add_module(OutputController17)
    
    Buffer20 = Module(49,"Buffer", 2, s_buf)
    Buffer20.Next.append(50)
    RNoC.add_module(Buffer20)
    
    OutputController18 = Module(50,"OutputController", 2, 1)
    OutputController18.Next.append(51)
    OutputController18.Next.append(68)
    OutputController18.Output.append("Local")
    RNoC.add_module(OutputController18)
    
    Buffer21 = Module(51,"Buffer", 2, s_buf)
    Buffer21.Next.append(52)
    RNoC.add_module(Buffer21)
    
    OutputController19 = Module(52,"OutputController", 2, 1)
    OutputController19.Next.append(53)
    OutputController19.Next.append(64)
    OutputController19.Output.append("South")
    RNoC.add_module(OutputController19)
    
    
    ## lane 4  A FAIRE ###################################################################################
    Buffer22 = Module(53,"Buffer", 4, s_buf)
    Buffer22.Next.append(54)
    RNoC.add_module(Buffer22)
    
    OutputController20 = Module(54,"OutputController", 4, 1)
    OutputController20.Next.append(55)
    OutputController20.Next.append(65)
    OutputController20.Output.append("East")
    RNoC.add_module(OutputController20)
    
    Buffer23 = Module(55,"Buffer", 4, s_buf)
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
    
    Buffer24 = Module(58,"Buffer", 4, s_buf)
    Buffer24.Next.append(59)
    RNoC.add_module(Buffer24)
    
    OutputController22 = Module(59,"OutputController", 4, 1)
    OutputController22.Next.append(60)
    OutputController22.Next.append(67)
    OutputController22.Output.append("West")
    RNoC.add_module(OutputController22)
    
    Buffer25 = Module(60,"Buffer", 4, s_buf)
    Buffer25.Next.append(61)
    RNoC.add_module(Buffer25)
    
    OutputController23 = Module(61,"OutputController", 4, 1)
    OutputController23.Next.append(62)
    OutputController23.Next.append(68)
    OutputController23.Output.append("Local")
    RNoC.add_module(OutputController23)
    
    Buffer26 = Module(62,"Buffer", 4, s_buf)
    Buffer26.Next.append(63)
    RNoC.add_module(Buffer26)
    
    OutputController24 = Module(63,"OutputController", 4, 1)
    OutputController24.Next.append(64)
    OutputController24.Output.append("South")
    RNoC.add_module(OutputController24)
    
    # Output MUX
    # South
    Mux3 = Module(64,"Mux", 5, 1)
    #Mux3.Next.append(-1)
    RNoC.add_module(Mux3)
    
    # East
    Mux4 = Module(65,"Mux", 5, 1)
    #Mux4.Next.append(-1)
    RNoC.add_module(Mux4)
    
    # North
    Mux5 = Module(66,"Mux", 5, 1)
    #Mux5.Next.append(-1)
    RNoC.add_module(Mux5)
    
    # West
    Mux6 = Module(67,"Mux", 5, 1)
    #Mux6.Next.append(-1)
    RNoC.add_module(Mux6)
    
    # Local
    Mux7 = Module(68,"Mux", 5, 1)
    #Mux7.Next.append(-1)
    RNoC.add_module(Mux7)
    
    return RNoC
    
def RNoC_byHand2():
    RNoC = RNoC_Graph()
    s_buf = 4
    
    # Circuit 0 _ West & Local inputs
    ## Lane 0
    InputController1 = Module(0,"InputController", 0, 1)
    InputController1.Next.append(1)
    RNoC.add_module(InputController1)
    
    Buffer1 = Module(1,"Buffer", 0, s_buf)
    Buffer1.Next.append(2)
    RNoC.add_module(Buffer1)
    
    OutputController1 = Module(2,"OutputController", 0, 1)
    OutputController1.Next.append(3)
    OutputController1.Next.append(41)
    OutputController1.Output.append("Local")
    RNoC.add_module(OutputController1)
    
    Buffer2 = Module(3,"Buffer", 0, s_buf)
    Buffer2.Next.append(4)
    RNoC.add_module(Buffer2)
    
    InputController2 = Module(4,"InputController", 0, 1)
    InputController2.Next.append(5)
    RNoC.add_module(InputController2)
    
    Buffer3 = Module(5,"Buffer", 0, s_buf)
    Buffer3.Next.append(6)
    RNoC.add_module(Buffer3)
    
    OutputController2 = Module(6,"OutputController", 0, 1)
    OutputController2.Next.append(7)
    OutputController2.Next.append(37)
    OutputController2.Output.append("South")
    RNoC.add_module(OutputController2)
    
    Buffer4 = Module(7,"Buffer", 0, s_buf)
    Buffer4.Next.append(8)
    RNoC.add_module(Buffer4)
    
    OutputController3 = Module(8,"OutputController", 0, 1)
    OutputController3.Next.append(9)
    OutputController3.Next.append(38)
    OutputController3.Output.append("East")
    RNoC.add_module(OutputController3)
    
    Buffer5 = Module(9,"Buffer", 0, s_buf)
    Buffer5.Next.append(10)
    RNoC.add_module(Buffer5)
    
    OutputController4 = Module(10,"OutputController", 0, 1)
    OutputController4.Next.append(11)
    OutputController4.Next.append(39)
    OutputController4.Output.append("North")
    RNoC.add_module(OutputController4)
    
    Buffer6 = Module(11,"Buffer", 0, s_buf)
    Buffer6.Next.append(12)
    RNoC.add_module(Buffer6)
    
    OutputController5 = Module(12,"OutputController", 0, 1)
    OutputController5.Next.append(40)
    OutputController5.Output.append("West")
    RNoC.add_module(OutputController5)
    
    # Circuit 1 _ North input
    ## lane 1
    InputController3 = Module(13,"InputController", 1, 1)
    InputController3.Next.append(14)
    RNoC.add_module(InputController3)
    
    Buffer11 = Module(14,"Buffer", 1, s_buf)
    Buffer11.Next.append(15)
    RNoC.add_module(Buffer11)
    
    OutputController11 = Module(15,"OutputController", 1, 1)
    OutputController11.Next.append(16)
    OutputController11.Next.append(40)
    OutputController11.Output.append("West")
    RNoC.add_module(OutputController11)
    
    Buffer12 = Module(16,"Buffer", 1, s_buf)
    Buffer12.Next.append(17)
    RNoC.add_module(Buffer12)
    
    OutputController12 = Module(17,"OutputController", 1, 1)
    OutputController12.Next.append(18)
    OutputController12.Next.append(41)
    OutputController12.Output.append("Local")
    RNoC.add_module(OutputController12)
    
    Buffer13 = Module(18,"Buffer", 1, s_buf)
    Buffer13.Next.append(19)
    RNoC.add_module(Buffer13)
    
    OutputController13 = Module(19,"OutputController", 1, 1)
    OutputController13.Next.append(20)
    OutputController13.Next.append(37)
    OutputController13.Output.append("South")
    RNoC.add_module(OutputController13)
    
    Buffer14 = Module(20,"Buffer", 1, s_buf)
    Buffer14.Next.append(21)
    RNoC.add_module(Buffer14)
    
    OutputController14 = Module(21,"OutputController", 1, 1)
    OutputController14.Next.append(22) 
    OutputController14.Next.append(38)
    OutputController14.Output.append("East")
    RNoC.add_module(OutputController14)
    
    Buffer1400 = Module(22,"Buffer", 1, s_buf)
    Buffer1400.Next.append(23)
    RNoC.add_module(Buffer1400)
    
    OutputController1400 = Module(23,"OutputController", 1, 1)
    OutputController1400.Next.append(39) # end circuit 1
    OutputController1400.Output.append("North")
    RNoC.add_module(OutputController1400)
    
    
    # Circuit 2 _ South & East inputs
    ## Lane 2
    InputController4 = Module(24,"InputController", 2, 1)
    InputController4.Next.append(25)
    RNoC.add_module(InputController4)
    
    Buffer15 = Module(25,"Buffer", 2, s_buf)
    Buffer15.Next.append(26)
    RNoC.add_module(Buffer15)
    
    OutputController15 = Module(26,"OutputController", 2, 1)
    OutputController15.Next.append(27)
    OutputController15.Next.append(38)
    OutputController15.Output.append("East")
    RNoC.add_module(OutputController15)
    
    Buffer16 = Module(27,"Buffer", 2, s_buf)
    Buffer16.Next.append(28)
    RNoC.add_module(Buffer16)
    
    InputController5 = Module(28,"InputController", 2, 1)
    InputController5.Next.append(29)
    RNoC.add_module(InputController5)
    
    Buffer17 = Module(29,"Buffer", 2, s_buf)
    Buffer17.Next.append(30)
    RNoC.add_module(Buffer17)
    
    OutputController16 = Module(30,"OutputController", 2, 1)
    OutputController16.Next.append(31)
    OutputController16.Next.append(39)
    OutputController16.Output.append("North")
    RNoC.add_module(OutputController16)
    
    Buffer18 = Module(31,"Buffer", 2, s_buf)
    Buffer18.Next.append(32)
    RNoC.add_module(Buffer18)
    
    OutputController17 = Module(32,"OutputController", 2, 1)
    OutputController17.Next.append(33)
    OutputController17.Next.append(40)
    OutputController17.Output.append("West")
    RNoC.add_module(OutputController17)
    
    Buffer20 = Module(33,"Buffer", 2, s_buf)
    Buffer20.Next.append(34)
    RNoC.add_module(Buffer20)
    
    OutputController18 = Module(34,"OutputController", 2, 1)
    OutputController18.Next.append(35)
    OutputController18.Next.append(41)
    OutputController18.Output.append("Local")
    RNoC.add_module(OutputController18)
    
    Buffer21 = Module(35,"Buffer", 2, s_buf)
    Buffer21.Next.append(36)
    RNoC.add_module(Buffer21)
    
    OutputController19 = Module(36,"OutputController", 2, 1)
    OutputController19.Next.append(37)
    OutputController19.Output.append("South")
    RNoC.add_module(OutputController19)
    
    
    # Output MUX
    # South
    Mux3 = Module(37,"Mux", 3, 1)
    #Mux3.Next.append(-1)
    RNoC.add_module(Mux3)
    
    # East
    Mux4 = Module(38,"Mux", 3, 1)
    #Mux4.Next.append(-1)
    RNoC.add_module(Mux4)
    
    # North
    Mux5 = Module(39,"Mux", 3, 1)
    #Mux5.Next.append(-1)
    RNoC.add_module(Mux5)
    
    # West
    Mux6 = Module(40,"Mux", 3, 1)
    #Mux6.Next.append(-1)
    RNoC.add_module(Mux6)
    
    # Local
    Mux7 = Module(41,"Mux", 3, 1)
    #Mux7.Next.append(-1)
    RNoC.add_module(Mux7)
    
    return RNoC
    

def main():

   # RNoC = RNoC_byHand()
    
   # RNoC.place_modules()
    
   # RNoC.plot()
    
   # RNoC.XML_writer('config.ini')
    
    NoC = NoC_RNoC(4, 4, RNoC_byHand2)
    NoC.plot()
    NoC.XML_writer('config.ini')
###############################################################################


if __name__ == "__main__":
    main()
    
    
    
    
    
    
    

