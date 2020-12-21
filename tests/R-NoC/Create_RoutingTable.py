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
"""

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

"""
graph = {'A': set(['B', 'C', 'D', 'E']),
         'B': set(['A', 'C', 'F']),
         'C': set(['A', 'B', 'F', 'G']),
         'D': set(['A', 'H', 'I']),
         'E': set(['A', 'H', 'I']),
         'F': set(['B', 'C', 'G']),
         'G': set(['C', 'F']),
         'H': set(['D', 'E', 'I']),
         'I': set(['D', 'E', 'H'])}
"""
"""
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
"""
"""
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

DIR = {'L': 0, 'E': 1, 'W': 2, 'N': 3, 'S': 4, 'U': 5, 'D': 6}

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

        # 1. Get all connections
        for ID in r0.connections:
            # identify the connected router
            for r in routers:
                if r.ID == ID:
                    r1 = r
            # compute angle
            angle = computeAngle(r0, r1)
            angles.append(angle)
            connIDs.append(r1.ID)
       # print("Routeur ", r0.ID, ", connected to: ", connIDs, ", at angles: ", angles)
        # 2. Order the angles
        angles_ordered = []
        connIDs_ordered = []
        for i in range(nbConn):
            # a. append min angle
            min_a = min(angles)
            angles_ordered.append(min_a)
            
            # b. append corresponding ID
            for j in range(nbConn-i):
                if angles[j] == min_a:
                    idx = j
                    break
            min_id = connIDs[idx]
            connIDs_ordered.append(min_id)
       
            # c. remove placed items
            angles.remove(min_a)
            connIDs.remove(min_id)

        # 3. Assign directions
        for j in range(len(routers)):
            if routers[j].ID == r0.ID:
                idx_r0 = j
                break

        if nbConn == 0: # no connection, impossible, but considered anyway
            pass
        elif nbConn == 4: # all connnections possible --> assign directions clockwise
            for i in range(nbConn):
                if i == 0:
                    direction = 'N'
                elif i == 1:
                    direction = 'E'
                elif i == 2:
                    direction = 'S'
                else:
                    direction = 'W'
   
                routers[idx_r0].connections[connIDs_ordered[i]] = direction
                        

        elif nbConn == 3: # one empty link --> assign clother direction to smallest angle, then clockwise 
            min_a = angles_ordered[0]
            dN = min_a
            dE = abs(min_a - pi/2)
            dS = abs(min_a - pi)
            dW = abs(min_a - 3*pi/2)

            dmin = min([dN, dE, dS, dW])
            if dN == dmin:
                direction = 'N'        
            elif dE == dmin:
                direction = 'E'
            elif dS == dmin:
                direction = 'S'
            else:
                direction = 'W'
            
            direction_prev = direction

            routers[idx_r0].connections[connIDs_ordered[0]] = direction

            
            for i in range(1,3): 
                if direction_prev == 'N':
                    direction = 'E'
                elif direction_prev == 'E':
                    direction = 'S'
                elif direction_prev == 'S':
                    direction = 'W'
                else :
                    direction = 'N'
              
                direction_prev = direction
                routers[idx_r0].connections[connIDs_ordered[i]] = direction

        else: # 1 or 2 connection --> assign the clothest direction or 2nd best if both share the same best
            n = 0
            e = 0
            s = 0
            w = 0
            for i in range(nbConn): 
                min_a = angles_ordered[i]
                dN = min_a
                dE = abs(min_a - pi/2)
                dS = abs(min_a - pi)
                dW = abs(min_a - 3*pi/2)
               # print(dW==dS)
                dmin = min([dN, dE, dS, dW])
                if dN == dmin:
                    if n == 0:
                        direction = 'N'
                        n = 1
                    else:
                        dmin = min([dE, dS, dW])
                        if dE == dmin:
                            direction = 'E'
                        elif dS == dmin:
                            direction = 'S'
                        else:
                            direction = 'W'
                elif dE == dmin:
                    if e == 0:
                        direction = 'E'
                        e = 1
                    else:
                        dmin = min([dN, dS, dW])
                        if dN == dmin:
                            direction = 'N'
                        elif dS == dmin:
                            direction = 'S'
                        else:
                            direction = 'W'
                elif dS == dmin:
                    if s == 0:
                        direction = 'S'
                        s = 1
                    else:
                        dmin = min([dE, dN, dW])
                        if dE == dmin:
                            direction = 'E'
                        elif dN == dmin:
                            direction = 'N'
                        else:
                            direction = 'W'
                else:
                    if w == 0:
                        direction = 'W'
                        w = 1
                    else:
                        dmin = min([dE, dS, dN])
                        if dE == dmin:
                            direction = 'E'
                        elif dS == dmin:
                            direction = 'S'
                        else:
                            direction = 'N'

                routers[idx_r0].connections[connIDs_ordered[i]] = direction

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

                #for i in range(len(routers)):
                #    print("Routeur ", routers[i].ID, ", connected to: ", routers[i].connections)

    #Update directions
    routers = Compute_directions(routers)

    return my_graphe, routers

######### Routing Table compouting ##########


def RoutingTable():

    nbLanes = 2
    nbPorts = 5
    NoC_x = 2
    NoC_y = 2
    nbRouters_NoC = NoC_x * NoC_y # mesh
    nbRouters_Roundabout = (nbLanes + 1) * nbPorts + 1
    nbRouters_R_NoC = nbRouters_NoC * nbRouters_Roundabout
    in_local = 2    
    
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

    nbRout = len(routers)
    Conn_Mat = -1*np.ones((nbRout, nbRout))

    for i in range(nbRout):
        for key, val in routers[i].connections.items():
            Conn_Mat[i, key] = DIR[val]
 
    np.savetxt('Direction_Mat.txt', Conn_Mat, fmt='%d', delimiter = ' ')
    """
    Main Execution Point
    """
    
    RT = RoutingTable()
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
