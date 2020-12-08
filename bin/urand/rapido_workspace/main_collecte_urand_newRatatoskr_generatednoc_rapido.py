import numpy as np
import os
import matplotlib.pyplot as plt
from random import randint, randrange
import pickle

from tempfile import mkstemp
from shutil import move, copymode
from os import fdopen, remove

import adjMat2NoC
from adjMat2NoC import Archi, Data
import configure_AdjMat

import re
import glob

def get_nbC(g):
    nb = 0
    print(g)
    for keys,values in g.items():
        nr = len(values)
        nb = nb + nr
    nbC = nb/2
    print(nbC)

    return nbC
    
def get_graph(adj_mat):
    # Step 1: create graph:
    graph = {}
    ## get all nodes and links
    for i in range(len(adj_mat)):
        if sum(adj_mat[i]) >= 1:
            ls = []
            ID = i
            for j in range(len(adj_mat)):
                if adj_mat[ID][j] == 1:
                    ls.append(j)
            graph[ID] = ls
    return graph

def create_NoC_data(adj_mat, filename):
    
    NoC = Archi(adj_mat)
    print(NoC.graph)
    NoC.place_nodes()

    #NoC.plot()
    data = Data()
    data.positions = NoC.positions
    data.links = NoC.links
    #print(data.positions)
    #print(data.links)
    with open(filename, 'wb') as f:
        pickle.dump(data, f)

def config_writer(NoC_file):
    base_file = "config_template.ini"
    pattern = "data_file = "
    subst = "data_file = /home/mmirka/my_ratatoskr/bin/urand/" + NoC_file
    #Create temp file
    fh, abs_path = mkstemp()
    with fdopen(fh,'w') as new_file:
        with open(base_file) as old_file:
            for line in old_file:
                new_file.write(line.replace(pattern, subst))
    #Copy the file permissions from the old file to the new file
    copymode(base_file, abs_path)
    
    move(abs_path, "config.ini")


def read_results():
    print("read results")
    results_file = 'rawResults.pkl'
    
    results = None
    with open(results_file, 'rb') as f:
        results = pickle.load(f)
    #return results

    latenciesFlit = results['latenciesFlit']
    latenciesPacket = results['latenciesPacket']
    latenciesNetwork = results['latenciesNetwork']
    #print(latenciesFlit)
    #print(latenciesPacket)
    #print(latenciesNetwork)
    meanLatenciesFlit = np.mean(latenciesFlit, axis=1)
    meanLatenciesPacket = np.mean(latenciesPacket, axis=1)
    meanLatenciesNetwork = np.mean(latenciesNetwork, axis=1)
    #print(meanLatenciesFlit)
    #print(meanLatenciesPacket)
    #print(meanLatenciesNetwork)
    
    print("score flit = ", meanLatenciesFlit, ", score packet = ", meanLatenciesPacket, ", score Network = ",  meanLatenciesNetwork)
    s_f = float(meanLatenciesFlit)
    s_p = float(meanLatenciesPacket)
    s_n = float(meanLatenciesNetwork)
    
    return [s_f, s_p, s_n]  



def main():
# For each adj-mat:
# 1. create NoC data (adjMat2NoC)
# 2. from NoC data, create XML files (configure_adjMat)
# 3. run simulation
    # copy the folder
    #cmd = 'echo demo | sudo -S cp -r /media/sf_shared_folder/Dataset/Matrices /home/demo/ratagan/Ratatoskr/bin/Datasets/.'
    #os.system(cmd)
    # change owner
    #cmd = 'echo demo | sudo -S chown -R demo /home/demo/ratagan/Ratatoskr/bin/Datasets/Matrices' 
    #os.system(cmd)
    for j in range(2):
        if j == 3:
            filename = '/home/mmirka/my_ratatoskr/bin/urand/results_NoC-compare/set-rapido/test_set_W'
        if j == 2: 
            filename = '/home/mmirka/my_ratatoskr/bin/urand/results_NoC-compare/set-rapido/test_set_RW'
        if j == 0:
            filename = '/home/mmirka/my_ratatoskr/bin/urand/results_NoC-compare/set-rapido/test_set_cW'
        if j == 1:
            filename = '/home/mmirka/my_ratatoskr/bin/urand/results_NoC-compare/set-rapido/test_set_cRW'
        
        folder = '/home/mmirka/my_ratatoskr/bin/urand/results_NoC-compare/set-rapido/'
        name = filename.replace(folder, '')
        ##print('Filename = ', name)
        with open(filename, 'rb') as f:
            load_data = pickle.load(f)
        f.close()
       
        cpt_nbc = [0,0,0,0,0,0,0,0,0,0,0]
        #for i in range(len(load_data)):
        for i in range(5):
            mat = load_data[i]
            adj_mat = np.array(mat)
            g = get_graph(mat)
            nbc = get_nbC(g)
            oklm = 1
            #if cpt_nbc[int(nbc - 8)] >= 5 or (nbc!=11 and nbc!=15 and nbc!=16):
            if oklm == 0:
                pass
            else:
                print("nbc = ", nbc)
                print("cpt = ", cpt_nbc[int(nbc - 8)])
          #      filename = "NoCs_data/Mat2NoC"
          #      create_NoC_data(adj_mat, filename)
          #      cpt_nbc[int(nbc - 8)] += 1
                
          #      print("#### 2. configure ####")
          #      # 2. configure
          #      ## a) modify config.ini
          #      print("  ## a) modify config.ini")
          #      config_writer(filename)
          #      ## b) run configuration
          #      print("  ## b) run configuration")
          #      configure_AdjMat.main()
          #  
          #      # 3. run sim
          #      print("#### 3. run sim ####")
          #      os.system("python3 Create_RoutingTable.py")
          #      #os.system("cp RT.txt urand/.")
          #      os.system("python3 run_urand.py")

          #      # 4. save results --> perf dataset
          #      #output = read_results()
          #      #print(output)
          #      #report_data[i] = output

          #      # 5. copy and rename raw results
          #      #new_name = name+"-nbc"+str(int(nbc))+"i"+str(cpt_nbc[int(nbc - 8)])+".pkl"
          #      new_name = name+"-compare-"+str(int(i+5))+".pkl"
                
          #      os.system("cp /home/mmirka/my_ratatoskr/bin/urand/rawResults.pkl /home/mmirka/my_ratatoskr/bin/urand/results_NoC-compare/set-rapido/scores/"+new_name)


if __name__ == "__main__":
    main()
