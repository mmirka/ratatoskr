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
### Global variables

# roundabout info
nbLanes = 2
nbPorts = 5
NoC_x = 2
NoC_y = 2
nbRouters_NoC = NoC_x * NoC_y # mesh
nbRouters_Roundabout = (nbLanes + 1) * nbPorts + 1
nbRouters_R_NoC = nbRouters_NoC * nbRouters_Roundabout
in_local = 2


"""
graph = {'A': set(['B', 'C', 'D', 'E']),
         'B': set(['A', 'C', 'E', 'F']),
         'C': set(['A', 'B', 'F', 'G']),
         'D': set(['A', 'G', 'H', 'I']),
         'E': set(['A', 'B', 'H', 'I']),
         'F': set(['B', 'C', 'G', 'H']),
         'G': set(['C', 'D', 'F', 'I']),
         'H': set(['D', 'E', 'F', 'I']),
         'I': set(['D', 'E', 'G', 'H'])}


## From Sancho's paper
Graph = {'A': ['E', 'C', 'B', 'D'],
         'B': ['A', 'C', 'E', 'F'],
         'C': ['A', 'B', 'F', 'G'],
         'D': ['A', 'G', 'H', 'I'],
         'E': ['A', 'B', 'H', 'I'],
         'F': ['B', 'C', 'G', 'H'],
         'G': ['F', 'C', 'D', 'I'],
         'H': ['I', 'E', 'F', 'D'],
         'I': ['G', 'D', 'E', 'H']}


graphNum = {0: [4, 2, 1, 3],
         1: [0, 2, 4, 5],
         2: [0, 1, 5, 6],
         3: [0, 6, 7, 8],
         4: [0, 1, 7, 8],
         5: [1, 2, 6, 7],
         6: [5, 2, 3, 8],
         7: [8, 4, 5, 3],
         8: [6, 3, 4, 7]}


graph = {'A': set(['B', 'C', 'D', 'E']),
         'B': set(['A', 'C', 'F']),
         'C': set(['A', 'B', 'F', 'G']),
         'D': set(['A', 'H', 'I']),
         'E': set(['A', 'H', 'I']),
         'F': set(['B', 'C', 'G']),
         'G': set(['C', 'F']),
         'H': set(['D', 'E', 'I']),
         'I': set(['D', 'E', 'H'])}

## Mesh 3x3
graph = {0: [1, 3],
           1: [2, 4, 0],
           2: [1, 5],
           3: [6, 4, 0],
           4: [1, 3, 7, 5],
           5: [2, 4, 8],
           6: [3, 7],
           7: [8, 4, 6],
           8: [7, 5]}

## Irregular Mesh3x3
graph = {0: set([1, 3]),
           1: set([2, 4, 0]),
           2: set([1, 5]),
           3: set([6, 4, 0]),
           4: set([1, 3, 5]),
           5: set([2, 4, 7]),
           6: set([3, 7]),
           7: set([5, 6])}
"""
###############################################################################
#def dfs(graph, start):
#    visited, stack = set(), [start]
#    while stack:
#       vertex = stack.pop()
#        if vertex not in visited:
#            visited.add(vertex)
#            stack.extend(graph[vertex] - visited)
#    return visited
#
#def dfs_r(graph, start, visited=None):
#    if visited is None:
#        visited = set()
#    visited.add(start)
#    for next in graph[start] - visited:
#        dfs_r(graph, next, visited)
#    return visited
###############################################################################
#def SpanningTree(network_file):
class Node(object):
    def __init__(self, ID):
        self.id = ID
        self.DFSlinks = []
        self.Remaininglinks = []
        self.label = None
        self.dist_from_root = 0

    def add_DFSlink(self, obj):
        self.DFSlinks.append(obj)

    def add_Remaininglinks(self, obj):
        self.Remaininglinks.append(obj)

class Channel(object):
    def __init__(self, up, down):
        self.edges = [down, up]
        self.UpEdge = up

class Router(object):
    def __init__(self, ID):
        self.ID = ID
        self.x = 0
        self.y = 0
        self.z = 0
        self.connections = {}        

######### Get graphe and connections from network.xml file #############

DIR_classic = {'L': 0, 'E': 1, 'W': 2, 'N': 3, 'S': 4, 'U': 5, 'D': 6}
DIR = {'Out': 0, 'Switch': 1, 'Keep': 2, 'In1': 3, 'In2': 4, 'In3': 5, 'In4': 6}

def get_GrapheAndConnections_old(noc_file):
    try:
        tree = ET.parse(noc_file)
    except FileNotFoundError:
        raise FileNotFoundError
    else:
        root = tree.getroot()

        my_graphe = {}

        config = configparser.ConfigParser()
        config.read('config.ini')

        proc_elemnt_ids = []
        for nodeType in root.find('nodeTypes').iter('nodeType'):
            if nodeType.find('model').attrib['value'] == 'ProcessingElement':
                proc_elemnt_ids.append(int(nodeType.attrib['id']))
     
        num_of_layers = int(config['Hardware']['z'])
        #print("Number of layers = ", num_of_layers)

        num_of_routers = 0
        routers = []

        excluded_points = []
        for node in root.find('nodes').iter('node'):
            # Don't include processing elements
            if int(node.find('nodeType').attrib['value']) not in proc_elemnt_ids:
                num_of_routers += 1

                router_ID = int(node.attrib['id'])
                router = Router(router_ID)
                router.x = float(node.find('xPos').attrib['value'])
                router.y = float(node.find('yPos').attrib['value'])
                router.z = float(node.find('zPos').attrib['value'])

                routers.append(router)
                my_graphe[router.ID] = []
            else:
                
                excluded_points.append(int(node.attrib['id']))
        
        #print("my_graphe = ", my_graphe, " Routers = ", routers)
    
        for con in root.find('connections').iter('con'):
            valid_con = True
            for port in con.find('ports').iter('port'):
                if (int(port.find('node').attrib['value']) in excluded_points):
                    valid_con = False
                    break
            connections = []
            if valid_con:
                connection = []
                connection.append(int(con.find('ports')[0].find('node').attrib['value']))
                connection.append(int(con.find('ports')[1].find('node').attrib['value']))
                connections.append(connection)

                #Update Graphe
                my_graphe[connection[0]].append(connection[1])
                my_graphe[connection[1]].append(connection[0])

                #Update router's connections
                
                for i in range(len(routers)):
                    ## Router0
                    if routers[i].ID == connection[0]:
                        router0 = routers[i]
                    ## Router1
                    if routers[i].ID == connection[1]:
                        router1 = routers[i]
                  
                ## dir0 =  from r1 to r0, and dir1 from r0 to r1
                if router1.x != router0.x:
                    if router0.x > router1.x:
                        dir0 = 'E'
                        dir1 = 'W'
                    else:
                        dir0 = 'W'
                        dir1 = 'E'

                elif router1.y != router0.y:
                    if router0.y > router1.y:
                        dir0 = 'N'
                        dir1 = 'S'
                    else:
                        dir0 = 'S'
                        dir1 = 'N'

                elif  router1.z != router0.z:
                    if router0.z > router1.z:
                        dir0 = 'U'
                        dir1 = 'D'
                    else:
                        dir0 = 'D'
                        dir1 = 'U'

                else:
                    dir0 = 'L'

                
                for i in range(len(routers)):
                    if routers[i].ID == router0.ID:
                        routers[i].connections[connection[1]] = dir1
                    if routers[i].ID == router1.ID:
                        routers[i].connections[connection[0]] = dir0
    return my_graphe, routers

def computeAngle(r0, r1):
    dx = r1.x - r0.x
    dy = r1.y - r0.y
    adx = abs(dx)
    hypo = math.sqrt(pow(dx,2)+pow(dy,2))

    if (dx>=0):
        if (dy>=0):
            angle = math.asin(adx/hypo)
        else:
            angle = pi - math.asin(adx/hypo)
    else:
        if (dy>=0):
            angle = 2*pi - math.asin(adx/hypo)
        else:
            angle = pi + math.asin(adx/hypo)

    return angle;


def Compute_directions(routers):
    for r0 in routers:
        angles = []
        connIDs = []
        nbConn = len(r0.connections)
        r0_ID = r0.ID
        r0_roundabout_ID = r0_ID % nbRouters_Roundabout # id of r0 into its roundabout
        r0_roundabout_ID_min = r0_ID - r0_roundabout_ID # id min into the roundabout
        r0_roundabout_ID_max = r0_ID + (nbRouters_Roundabout-r0_roundabout_ID-1)
        if r0_roundabout_ID == 0:
            r0_lane = nbLanes + 1
        else:
            r0_lane = (r0_roundabout_ID-1) // nbPorts
        print(r0_ID, r0_roundabout_ID, r0_roundabout_ID_min, r0_roundabout_ID_max)
        print("lane = ", r0_lane)

        for key, val in r0.connections.items():
            r1_ID = key
            r1_roundabout_ID = r1_ID % nbRouters_Roundabout # id of r0 into its roundabout
            r1_roundabout_ID_min = r1_ID - r1_roundabout_ID # id min into the roundabout
            r1_roundabout_ID_max = r1_ID + (nbRouters_Roundabout-r1_roundabout_ID-1)
            if r1_roundabout_ID == 0:
                r1_lane = nbLanes + 1
            else:
                r1_lane = (r1_roundabout_ID-1) // nbPorts
            print('___ ', r1_ID, r1_roundabout_ID, r1_roundabout_ID_min, r1_roundabout_ID_max)
            print("___ lane = ", r0_lane)
           
            # check if it is an internal router (from same roundabout)
            fromSameRbt = False
            if (r1_roundabout_ID_min == r0_roundabout_ID_min) and (r1_roundabout_ID_max == r0_roundabout_ID_max): # only one comparison is enough but can highlights error...
                fromSameRbt = True
            #if r0_    
            if fromSameRbt:
                if r1_ID == r0_ID - 1: #receive next
                    direction = 'In1'
                elif r1_ID == r0_ID + 1: #send next
                    if r1_lane == nbLanes:
                        direction = 'Out'
                    else:
                        direction = 'Keep'
                elif r1_ID > r0_ID: # change lane --> switch or out  
                    if r1_lane == nbLanes:
                        if r0_roundabout_ID == 0:
                            direction = 'In1'
                        else:
                            direction = 'Out'
                    else:
                        direction = 'Switch'
                else: # receive from a switching or outing
                    if r1_roundabout_ID == 0:
                        direction = 'Out'
                    elif r1_lane == r0_lane-1: #previous lane --> higher priority
                        direction = 'In1'
                    else: # for now only 2 input max ################################## !!!!!! IMPORTANT !!!!!! #############################
                        direction = 'In2'
            else:
                if r0_lane < r1_lane: # receive from other roundabout
                    direction = 'In2'
                else:
                    direction = 'Out' # send to other roundabout
            
            routers[r0_ID].connections[r1_ID] = direction     
            
    return routers

def get_GrapheAndConnections(noc_file):
    try:
        tree = ET.parse(noc_file)
    except FileNotFoundError:
        raise FileNotFoundError
    else:
        root = tree.getroot()

        my_graphe = {}

        config = configparser.ConfigParser()
        config.read('config.ini')

        proc_elemnt_ids = []
        for nodeType in root.find('nodeTypes').iter('nodeType'):
            if nodeType.find('model').attrib['value'] == 'ProcessingElement':
                proc_elemnt_ids.append(int(nodeType.attrib['id']))
     
        num_of_layers = int(config['Hardware']['z'])
        #print("Number of layers = ", num_of_layers)

        num_of_routers = 0
        routers = []

        excluded_points = []
        for node in root.find('nodes').iter('node'):
            # Don't include processing elements
            if int(node.find('nodeType').attrib['value']) not in proc_elemnt_ids:
                num_of_routers += 1

                router_ID = int(node.attrib['id'])
                router = Router(router_ID)
                router.x = float(node.find('xPos').attrib['value'])
                router.y = float(node.find('yPos').attrib['value'])
                router.z = float(node.find('zPos').attrib['value'])

                routers.append(router)
                my_graphe[router.ID] = []
            else:
                
                excluded_points.append(int(node.attrib['id']))
        
        #print("my_graphe = ", my_graphe, " Routers = ", routers)
    
        for con in root.find('connections').iter('con'):
            valid_con = True
            for port in con.find('ports').iter('port'):
                if (int(port.find('node').attrib['value']) in excluded_points):
                    valid_con = False
                    break
            connections = []
            if valid_con:
                connection = []
                connection.append(int(con.find('ports')[0].find('node').attrib['value']))
                connection.append(int(con.find('ports')[1].find('node').attrib['value']))
                connections.append(connection)

                #Update Graphe
                my_graphe[connection[0]].append(connection[1])
                my_graphe[connection[1]].append(connection[0])

                #Update router's connections
                routers[connection[1]].connections[connection[0]] = ''
                routers[connection[0]].connections[connection[1]] = ''        

        for i in range(len(routers)):
            print("Routeur ", routers[i].ID, ", connected to: ", routers[i].connections)

    #Update directions
    routers = Compute_directions(routers)
    for i in range(len(routers)):
        print("Routeur ", routers[i].ID, ", connected to: ", routers[i].connections)

    return my_graphe, routers

######### Routing Table compouting ##########


def RoutingTable():

    # r-noc info in global variables    
    
    ### 1. Macro routing table: XY routing
    XY_NoC_RT = -np.ones((nbRouters_NoC,nbRouters_NoC))
    
    for src in range(nbRouters_NoC):
        for dst in range(nbRouters_NoC):
            if src == dst:
                pass
            else:
                src_x = src%NoC_x
                src_y = src//NoC_y
                dst_x = dst%NoC_x
                dst_y = dst//NoC_y
                
                if dst_x > src_x:
                    next = src+1
                elif dst_x < src_x:
                    next = src-1
                elif dst_y > src_y:
                    next = src+NoC_x
                else:
                    next = src-NoC_x
                
                XY_NoC_RT[src,dst] = next
    print(XY_NoC_RT)    
    
    ### 2. Micro routing table: roundabout
    roundabout_RT = -np.ones((nbRouters_Roundabout,1,nbLanes))
    
    for src in range(nbRouters_Roundabout):
        dst = 0
        if src == dst:
            pass
        else:
            next = -np.ones(nbLanes)
            r_lane = (src-1)//nbPorts
            r_port = (src-1)%nbPorts
            if src == 12:
                next[0] = 0
                roundabout_RT[src,dst] = next
            elif src > 6:
                pass
            else:
                next[0] = src + nbPorts*nbLanes + 1
                next[1] = src + 1    
                roundabout_RT[src,dst] = next
        
        
    print(roundabout_RT)
        
    return RT

###############################################################################


def main():
    noc_file = './config/network.xml'
    my_graphe, routers = get_GrapheAndConnections(noc_file)
"""
    nbRout = len(routers)
    Conn_Mat = -1*np.ones((nbRout, nbRout))

    for i in range(nbRout):
        for key, val in routers[i].connections.items():
            Conn_Mat[i, key] = DIR[val]
 
    np.savetxt('Direction_Mat.txt', Conn_Mat, fmt='%d', delimiter = ' ')
 
#    Main Execution Point
    
    RT = RoutingTable()
"""

"""   
    RT_Dir = np.empty(RT.shape, dtype=str)
    for i in range(l_RT):
        for j in range(l_RT):
            val = RT[i,j]
            #d_val = ''
            if val != -1:
                for k in range(l_RT):
                    router = routers[k]
                    if router.ID == j:
                        idx = k
                        break
                val = routers[idx].connections[val]
            else:
                val = 'L'
            RT_Dir[i,j] = val

    #print("RT directions = \n", RT_Dir)
    
    RT_DirNum = np.empty(RT.shape, dtype=int)
    for i in range(l_RT):
        for j in range(l_RT):
            val = RT_Dir[i,j]
            RT_DirNum[i,j] = DIR[val]
            
    #print("RT directions number = \n", RT_DirNum)
    
    #Create text file from routing table
    np.savetxt('RT.txt', RT_DirNum, fmt='%d', delimiter = ' ') 
###############################################################################
"""

if __name__ == "__main__":
    main()
