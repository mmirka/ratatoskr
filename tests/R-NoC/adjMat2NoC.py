#!/bin/python
import numpy as np
import matplotlib.pyplot as plt
import random
from random import randint
import math
import pickle
import copy
from Create_AdjacencyMatrix import AdjMat_Creator

class Node(object):
    def __init__(self, ID):
        self.id = ID
        self.links = []
        

class Archi:

    def load_matrix(self, adj_mat):
        self.adj_mat = adj_mat
        self.nbRouters = len(self.adj_mat)
     

    def get_graph(self):
        # Step 1: create graph:
        self.graph = {}
        ## get all nodes and links
        for i in range(len(self.adj_mat)):
            if sum(self.adj_mat[i]) >= 1:
                ls = []
                ID = i
                for j in range(len(self.adj_mat)):
                    if self.adj_mat[ID][j] > 0:
                        ls.append(j)
                self.graph[ID] = ls

    def get_links_to_place(self):
        self.links_to_place=[]
        for keys,values in self.graph.items():
            for l in values:
                link_1 = [l, keys]
                link_2 = [keys, l]
                if link_1 in self.links_to_place:
                    pass
                elif link_2 in self.links_to_place:
                    pass
                else:
                    self.links_to_place.append(link_2)
           

    def __init__(self, mat):
        self.adj_mat = None
        self.load_matrix(mat)
        self.get_graph()

        self.get_links_to_place()
        #print("links_to_place : ",self.links_to_place)
        self.num_nodes = len(self.graph) 
        
        self.placed = []

        self.positions={}

        self.links=[]

        self.nbLanes = 5
        self.nbPrimaryLanes = 3
        self.nbSecondaryLanes = 2
        self.inputLane0 = {"L":2, "W":1}
        self.inputLane1 = {"S":8, "E":9}
        self.inputLane2 = {"N":14}
        self.endLaneLink = {5:16, 7:23, 13:-1, 15:-1, 17:-1}
        self.switchs = {-1:-1}
        self.intermediairesBuf = {-1:-1}
        self.nbPorts = 5
        self.NoC_x = 2
        self.NoC_y = 2
        self.nbRouters_NoC = self.NoC_x * self.NoC_y # mesh
        self.nbRouters_Roundabout = (self.nbLanes + 1) * self.nbPorts + 1
        self.nbRouters_R_NoC = self.nbRouters_NoC * self.nbRouters_Roundabout
        self.in_local = 2
    


    def check_noCrossing(self, start, next):
        output = 1
        c_link = [start, next]
        c_link_x = [min(self.positions[start][0],self.positions[next][0]), max(self.positions[start][0],self.positions[next][0])]
        c_link_y = [min(self.positions[start][1],self.positions[next][1]), max(self.positions[start][1],self.positions[next][1])]

        if c_link_x[0] == c_link_x[1]:# 0 = horizontal, 1 = vertical
            c_link_or = 1      
        else :
            c_link_or = 0 
            
        for link in self.links:
            #print("# Check no crossing #")
            #print(link)
            #print(self.positions)
            p_ls = self.positions[link[0]]
            #print(p_ls)
            p_le = self.positions[link[1]]
            #print(p_le)
            link_x = [min(p_ls[0],p_le[0]), max(p_ls[0],p_le[0])]
            link_y = [min(p_ls[1],p_le[1]), max(p_ls[1],p_le[1])]
            if link_x[0] == link_x[1]:# 0 = horizontal, 1 = vertical
                link_or = 1
                #print(link_length)
            else :
                link_or = 0
        
            if c_link_or == link_or: # same orientation --> no crossing
                if link_or == 1: #links vertical
                    if (link_x[0] == c_link_x[0]):
                        if (c_link_y[0] in range(link_y[0]+1, link_y[1])) or (c_link_y[1] in range(link_y[0]+1, link_y[1])): # crossing links
                            output = 0
                            break
                    else:
                        pass
                else: #links horizontal   
                    if (link_y[0] == c_link_y[0]):
                       if (c_link_x[0] in range(link_x[0]+1, link_x[1])) or (c_link_x[1] in range(link_x[0]+1, link_x[1])): # crossing links
                           output = 0
                           break
                    else:
                        pass
            else:
                if link_or == 1: #link vertical, c_link horizontal
                    if (link_x[0] in range(c_link_x[0]+1, c_link_x[1])) and (c_link_y[0] in range(link_y[0]+1, link_y[1])): # crossing links
                        output = 0
                        break
                    else:
                        pass
                else: #link horizontal, c_link vertical   
                    if (link_y[0] in range(c_link_y[0]+1, c_link_y[1])) and (c_link_x[0] in range(link_x[0]+1, link_x[1])): # crossing links
                        output = 0
                        break
                    else:
                        pass

        ## check no crossing a node thqt is not part of the link
        for node in self.placed:
            if c_link_or == 1: #v link
                if self.positions[node][0] == c_link_x[0]:
                    if self.positions[node][1] in range(c_link_y[0]+1, c_link_y[1]):
                        output = 0
            else:
                if self.positions[node][1] == c_link_y[0]:
                    if self.positions[node][0] in range(c_link_x[0]+1, c_link_x[1]):
                        output = 0
        return output    

    def check_position(self, start, next):
        s_p = self.positions.get(start)
        #print(s_p)
        n_p = self.positions.get(next)
        #print(n_p)
        if s_p[0] == n_p[0]:
            linkable = 1
        elif s_p[1] == n_p[1]:
            linkable = 1
        else:
            linkable = 0

        if linkable == 1:
            ret = self.check_noCrossing(start, next)
            if ret == 1:
                link_1 = [start, next]
                link_2 = [next, start]
                if link_1 in self.links:
                    output = 0
                elif link_2 in self.links:
                    output = 0
                else:
                    output = 1
            else:
                output = -1
        else:
            output = -1

        return output
    

    def check_onLink(self, p):
        output = 0
        for link in self.links:
            a = link[0]
            b = link[1]
            if (a not in self.placed) or (b not in self.placed):
                #print(a, " or ", b, " not in ", self.placed)
                output = 0
            else:
                #print(a, " or ", b, " in ", self.placed)
                p_a = self.positions[a]
                p_b = self.positions[b]
                if p_a[0] == p_b[0]:    # v link 
                    if (p[0] == p_a[0]) and (p[1] in range(min(p_a[1], p_b[1]), max(p_a[1], p_b[1])+1)): # supperposed
                        output = 1 
                        break
                    else:
                        output = 0
                else:       # h link
                    if (p[1] == p_a[1]) and (p[0] in range(min(p_a[0], p_b[0]), max(p_a[0], p_b[0])+1)): # supperposed
                        output = 1
                        break
                    else:
                        output = 0

        return output

    def in_positions(self, p):
        output = 0
        for keys,values in self.positions.items():
            if (values[0] == p[0]) and (values[1] == p[1]):
                output = 1
                break
            else:
                pass
        #print("positions: ", self.positions)
        #print("p: ", p)
        #print("output: ", output)
        return output

    def check_allLinks(self):
        for link in self.links_to_place:
            link_1 = link
            link_2 = [link[1], link[0]]
            
            if link_1 in self.links:
                #print(link_1, " in ", self.links)
                pass
            elif link_2 in self.links:
                pass
            else:
                return False
        return True

    def place_nodes(self):
        width_roundabout = 0.8
        step_lane = (width_roundabout/2)/(self.nbLanes+1)
        print("step_lane = ",step_lane)
        angles_start = np.zeros(self.nbLanes+1)
        angle_step = (2*math.pi)/(self.nbPorts-1)
        angle_local = 5*math.pi/4
        
        #for k, value in self.graph.items():
        for k in range(self.nbRouters_R_NoC):
            R_id = k
            if R_id%self.nbRouters_Roundabout == 0:
                RNoC_id = R_id//self.nbRouters_Roundabout
                x = RNoC_id%self.NoC_x
                y = RNoC_id//self.NoC_y
                self.positions[R_id] = [x,y]
                print(R_id, " ", RNoC_id)
                print(x," ",y)
                
            else:
                RNoC_id = R_id//self.nbRouters_Roundabout
                offset_x = self.positions[RNoC_id*self.nbRouters_Roundabout][0]
                offset_y = self.positions[RNoC_id*self.nbRouters_Roundabout][1]
                center_x = offset_x + width_roundabout/2
                center_y = offset_y+width_roundabout/2  # 0.3/2 + 0.05
                
                inR_id = R_id%self.nbRouters_Roundabout
                id_lane = (inR_id-1)//self.nbPorts
                id_port = (inR_id-1)%self.nbPorts
                print(R_id, " ", inR_id, " ", id_lane)
                radius = step_lane+id_lane*step_lane
                print("radius = ", radius)
                if inR_id%5 == 1:
                    print("local output")
                    angle_r = angle_local
                else:
                    print("other output")
                    if inR_id%self.nbPorts == 0:
                        angle_r = math.pi
                    else:
                        angle_r = -angle_step + angle_step*(inR_id%self.nbPorts - 2)
        
                if id_lane == self.nbLanes:
                    angle_r += math.pi/16
                                
                relative_x = math.cos(angle_r) * radius  
                relative_y = math.sin(angle_r) * radius 
                
                x = relative_x + center_x
                y = relative_y + center_y
                
                self.positions[R_id] = [x,y]
                print(x," ",y)    
                 
        for n0, value in self.graph.items():
            for n1 in self.graph[n0]:
                if [n1, n0] in self.links:
                    pass
                else:
                    self.links.append([n0, n1]) 
                    
                    

    def old_place_nodes(self):
        N = self.num_nodes
        c = int(math.sqrt(N))
        r = N-c**2
 
        print("N = ", N, ", c = ", c, ", r = ", r)

        P_x = range(c+1)
        P_y = range(c)

        idr = 0
        for x in range(c+1):
            if x == c:
                for y in range(r):
                    self.positions[idr] = [x,y]
                    idr = idr+1
            else:
                for y in range(c):
                    self.positions[idr] = [x,y]
                    idr = idr+1    

        for n0 in range(N):
            for n1 in self.graph[n0]:
                if [n1, n0] in self.links:
                    pass
                else:
                    self.links.append([n0, n1])
                    
                 

    def plot(self):
        fig = plt.figure()
        print(len(self.positions)) 
        x = np.zeros(self.nbRouters_R_NoC)
        y = np.zeros(self.nbRouters_R_NoC)
        i = 0
        self.key2id = {}
        self.id2key = {}
        for keys,values in self.positions.items():
            self.key2id[keys] = i
            self.id2key[i] = keys
            x[i] = values[0]
            y[i] = values[1]
            i += 1
       # print(self.key2id)
       # print(self.id2key)
       # print(x) 
       # print(y)
        for i in range(len(x)):
            if i%self.nbRouters_Roundabout == 0:
                plt.scatter(x[i], y[i], s=50, c='g')
            else:
                plt.scatter(x[i], y[i], s=40, c='b')
            
        i = 0
        
        for l in self.links:
            l1 = l[0]
            l2 = l[1]
            x_l = [self.positions[l1][0], self.positions[l2][0]]
            y_l = [self.positions[l1][1], self.positions[l2][1]]
            
            plt.arrow(x_l[0], y_l[0], (x_l[1]-x_l[0]), (y_l[1]-y_l[0]), fc='k', ec='k',head_width=0.02, head_length=0.05,linewidth=1, length_includes_head=True)
            
            
        for xi,yi in zip(x,y):
          #  print(self.id2key[i])
            label = "{:.0f}".format(self.id2key[i])
            plt.annotate(label, (xi, yi), textcoords='offset points',xytext=(-5,-10), ha='center', c = 'r')
            i += 1

        plt.axis('equal')
        #plt.grid()
        plt.show()

        
                    
link_length_max = 1          


class Data(object):
    def __init__(self):
        self.positions = None
        self.links = None

def NoC_plot(data):
        fig = plt.figure()
        
        x = np.zeros(len(data.positions))
        y = np.zeros(len(data.positions))
        i = 0
        key2id = {}
        id2key = {}
        for keys,values in data.positions.items():
            key2id[keys] = i
            id2key[i] = keys
            x[i] = values[0]
            y[i] = values[1]
            i += 1
       # print(self.key2id)
       # print(self.id2key)
       # print(x) 
       # print(y)
        plt.scatter(x, y, s=10, c='b')
        i = 0
        for xi,yi in zip(x,y):
          #  print(self.id2key[i])
            label = "{:.0f}".format(id2key[i])
            plt.annotate(label, (xi, yi), textcoords='offset points',xytext=(-15,-15), ha='center')
            i += 1
        for l in data.links:
            l1 = l[0]
            l2 = l[1]
            x_l = [data.positions[l1][0], data.positions[l2][0]]
            y_l = [data.positions[l1][1], data.positions[l2][1]]
            plt.plot(x_l, y_l)

        plt.axis('equal')
        plt.grid()
        plt.show()

def main():

    AM_creator = AdjMat_Creator()
    RNoC_mat = AM_creator.R_NoC_AM()

    adj = RNoC_mat
    print(adj)
    NoC = Archi(adj)
    print("Archi: ",Archi)
    print("   adj_mat: ",NoC.adj_mat)
    print("   graph: ",NoC.graph)
    print("   positions: ",NoC.positions)
    print("   placed: ",NoC.placed)
    print("   links: ",NoC.links)
    print("   links to place: ",NoC.links_to_place)
    ret = NoC.place_nodes() 

    print("positions: ",NoC.positions)
    print("placed: ",NoC.placed)
    print("links: ",NoC.links)
    print("links to place: ",NoC.links_to_place)
    print("graph: ",NoC.graph)
    NoC.plot()
          
    ### For netWork Writer: Memorize Positions and Links
    filename = 'NoCs_data/Mat2NoC'
    data = Data()
    data.positions = NoC.positions
    data.links = NoC.links
       
    with open(filename, 'wb') as f:
        pickle.dump(data, f)  

    with open(filename, 'rb') as f:
        load_data = pickle.load(f)
            
    NoC_plot(load_data)

    print("####### MIRACLE #########")
    
if __name__ == "__main__":
    main()


