#!/bin/python
import numpy as np
import matplotlib.pyplot as plt
import random
from random import randint
import math
import pickle
import copy
#for i in range(8,-1,-1):
#    print(i)
np.random.seed(10)
adj_1 = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
 [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0,],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0,],
 [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0,],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
 [0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,]]

adj_2 = [[0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
 [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
 [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
 [0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,],
 [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
 [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
 [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
 [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,]]

adj_3 = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
 [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0,],
 [0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
 [0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
 [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0,],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0,],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0,],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0,],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
 [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,]]


class Node(object):
    def __init__(self, ID):
        self.id = ID
        self.links = []

class Archi:

    def load_matrix(self, adj_mat):
        self.adj_mat = adj_mat

    def get_graph(self):
        # Step 1: create graph:
        self.graph = {}
        ## get all nodes and links
        for i in range(len(self.adj_mat)):
            if sum(self.adj_mat[i]) >= 1:
                ls = []
                ID = i
                for j in range(len(self.adj_mat)):
                    if self.adj_mat[ID][j] == 1:
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
           
    def build_mainDFS(self, start=None, visited=None, tree=None, dist=None):
        if start is None:
            start = list(self.graph.keys())[0]
        if visited is None:
            visited = set()
            visited.add(start)
        if tree is None:
            tree = {}
            s_node = Node(start)
            tree[start] = s_node
        if dist is None:
            dist = 0

        tree[start].dist_from_root = dist

        for next in self.graph[start]:#-visited:
            if next in visited:
                pass
            else:
                #print("###############")
                #print(visited)
                #print("tree :")
                #for keys,values in tree.items():
                #    print(keys, " : ", values.links)
                tree[start].links.append(next)     
                tree[next] = Node(next)
                visited.add(next)
                self.build_mainDFS(next, visited, tree, dist+1)

        self.tree = tree

    def build_PrevTree(self):
        self.prev_tree = {}
        for keys,values in self.tree.items():
            for val in values.links:
                self.prev_tree[val] = keys

        #print("Prev Tree: ", self.prev_tree)

    def __init__(self, mat):
        self.adj_mat = None
        self.load_matrix(mat)
        self.get_graph()

        self.build_mainDFS()
        #print("tree :")
        #for keys,values in self.tree.items():
        #    print(keys, " : ", values.links)
        self.build_PrevTree()
        self.get_links_to_place()
        #print("links_to_place : ",self.links_to_place)
        self.num_nodes = len(self.graph) 
        
        self.placed = []

        self.positions={}

        self.links=[]


    


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
 

    def place_nodes_recursif (self, link_length_max, start=None, tree_Lvisited=None): # no crossing, superposition, etc.
        if tree_Lvisited is None:
            tree_Lvisited = copy.deepcopy(self.tree)
            for keys, values in tree_Lvisited.items():
                tree_Lvisited[keys] = []
                #print("graph_Lvisited[",keys, "] = ", graph_Lvisited[keys])
        

        if start is None:
            start = list(self.tree.keys())[0]
            self.placed.append(start) 
            self.positions[start] = [0, 0]
        #print("length placed: ",len(self.placed))
        #print("length graph: ",len(self.graph))
        #print("\nstart: ", start)
        #print("positions: ", self.positions)
        #print("links: ", self.links)
        #print("links to place: ", self.links_to_place)
        #print("placed: ", self.placed)
        #print(graph_Lvisited)
        # Base case to stop
        if (len(self.placed) == len(self.graph)) and self.check_allLinks():
            #print("###### Finished ######")
            return 1
        else:                        
            ## connect all possible
            for node in self.graph[start]:
                #print("node test: ", node)
                #print(self.positions)
                if node in self.placed: # check if the already placed node is linkable
                    ret = self.check_position(start, node)
                    #print(ret)
                    if ret == 0:
                        pass
                    elif ret == 1:
                        self.links.append([start, node])
                        if (len(self.placed) == len(self.graph)) and self.check_allLinks():
                            #print("###### Finished ######")
                            return 1
                    else:
                        #print("## no solution ##")
                        return -1
                else:
                    pass
            next_to_place = []
            # If no next available, go back:
            for next in self.tree[start].links:
                #if next in tree_Lvisited[start]:
                if next in self.placed:
                    pass
                else:
                    next_to_place.append(next)
            #print("still to place: ", next_to_place)
            if not next_to_place:
                #print("no placement")
                # go back in DFS tree
                previous = self.prev_tree[start]
                tree_Lvisited[start].append(previous)
                #print("next back: ",previous)
                r = self.place_nodes(link_length_max, previous, tree_Lvisited)
                if r == 1:
                    return 1
                else:
                    return -1 

            else:
                
                for next in next_to_place:
                    #print("next: ", next)
                    tree_Lvisited[start].append(next)
                    #stop = -1
                    #while stop == -1:
                    pos_start = self.positions.get(start)
                    x_start = pos_start[0]
                    y_start = pos_start[1]
                    for x in range(0,link_length_max+1,1): #[-link_length, 0, link_length]:
                        for sign_x in [-1, 1]:
                            for y in range(0,link_length_max+1,1):
                                for sign_y in [-1, 1]:
                                    xf = x*sign_x
                                    yf = y*sign_y
                                    #print(xf,", ", yf)
                                    if xf == yf:
                                        pass
                                    elif (xf != 0) and (yf != 0):
                                        pass
                                    else:
                                        p = [xf+x_start,yf+y_start]
                                        ret = self.check_onLink(p)
                                        #print("ret = ",ret)
                                        if ret == 1:
                                            pass
                                        elif self.in_positions(p) == 1:
                                            pass
                                        else:
                                            #print("next ", next ,"p = ", p)
                                            self.positions[next] = p
                                            self.placed.append(next)
                                            #self.links.append([start, next])###
                                            #print(self.positions[next])
    
                                        
    
                                            ## memorize state
                                            #print("next: ",next)
                                            r = self.place_nodes(link_length_max, next, tree_Lvisited)
                                            if r == 1:
                                                return 1
                                                #return 0
                                            else:
                                                ## delete last modif
                                                del self.positions[next]
                                                self.placed.remove(next)
                                                links2del = []
                                                for link in self.links:
                                                    if next in link:
                                                        links2del.append(link)
                                                for link in links2del:
                                                    self.links.remove(link)
                                                tree_Lvisited[next] = []
                                
                    return -1


                         
                                ## No solutions
                                # try with longer links
                                #link_length += 1
                                #if link_length > 5:
                                #    return False
                    #previous = self.prev_tree[start]
                    #tree_Lvisited[start].append(previous)
                    #r = self.place_nodes(previous, tree_Lvisited)
                    #if r == 1:
                    #    return 1
                    #    #return 0
                    #else:
                    
                 

    def plot(self):
        fig = plt.figure()
        
        x = np.zeros(len(self.graph))
        y = np.zeros(len(self.graph))
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
        plt.scatter(x, y, s=500, c='b')
        i = 0
        for xi,yi in zip(x,y):
          #  print(self.id2key[i])
            label = "{:.0f}".format(self.id2key[i])
            plt.annotate(label, (xi, yi), textcoords='offset points',xytext=(-15,-15), ha='center')
            i += 1
        for l in self.links:
            l1 = l[0]
            l2 = l[1]
            x_l = [self.positions[l1][0], self.positions[l2][0]]
            y_l = [self.positions[l1][1], self.positions[l2][1]]
            plt.plot(x_l, y_l)

        plt.axis('equal')
        plt.grid()
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
        plt.scatter(x, y, s=500, c='b')
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

    
    link_length_max = 1
    #adj = adj_1
    #NoC = Archi(adj)
    #print("Archi: ",Archi)
    #print("   adj_mat: ",NoC.adj_mat)
    #print("   graph: ",NoC.graph)
    #print("   positions: ",NoC.positions)
    #print("   placed: ",NoC.placed)
    #print("   links: ",NoC.links)
    #print("   links to place: ",NoC.links_to_place)


    #print("### Start recurrence ###")

    #ret = NoC.place_nodes()
    #print("positions: ",NoC.positions)
    #print("placed: ",NoC.placed)
    #print("links: ",NoC.links)
    #print("links to place: ",NoC.links_to_place)
    #print("graph: ",NoC.graph)
    #print("ret = ", ret)

    #NoC.plot()
   
    filename = 'Dataset_1M_adjMat_r9_i1'
    with open(filename, 'rb') as f:
        load_data = pickle.load(f)
    
    for i in range(1):
        ret = 0
        link_length_max = 1
        while ret != 1:
            adj = load_data[13,:,:]
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
            print("ret = ", ret)
            if ret == 1:
                print("positions: ",NoC.positions)
                print("placed: ",NoC.placed)
                print("links: ",NoC.links)
                print("links to place: ",NoC.links_to_place)
                print("graph: ",NoC.graph)
                NoC.plot()

            else:
                print("######### Increase  link_length_max ###########")
                #global link_length_max
                link_length_max += 1
                print("######### link_length_max = ", link_length_max)
            
        ### For netWork Writer: Memorize Positions and Links
        filename = 'Mat2NoC_test2'
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


