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

def config_writer(base_file, NoC_file):
  
    pattern = "data_file = "
    subst = "data_file = /home/mirka/ratatoskr/bin/urand/collectes/c1/" + NoC_file
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
    #for j in range(1):
    for j in range(24,29,1):
    #for j in range(8,19,1):
    #for j in range(8,9,1):
        filename = '/home/mirka/Workspace/gan_explo/Data/Datasets_nxn_nbC_matrices/Datasets_nxn_nbC/Dataset_mat16x16_nbR:16_nbC:'+str(j)+'_*'
        #filename = '/home/mmirka/Documents/Projects/RataGAN/ratagan/GAN/Workspace/Data/Datasets_nxn_nbC/Datasets_nxn_nbC/Dataset_mat16x16_nbR:16_nbC:'+str(j)+'_*'
        #folder = '/home/mmirka/Documents/Projects/RataGAN/ratagan/GAN/Workspace/Data/sorted/matrices/'
        folder = '/home/mirka/Workspace/gan_explo/Data/Datasets_nxn_nbC_matrices/Datasets_nxn_nbC/'
        name = filename.replace(folder, '')
        ##print('Filename = ', name)
        for file in glob.glob('/home/mirka/Workspace/gan_explo/Data/Datasets_nxn_nbC_matrices/Datasets_nxn_nbC/Dataset_mat16x16_nbR:16_nbC:'+str(j)+'_*'):
            #print(file)
            #print(22222)
            filename = file
        with open(filename, 'rb') as f:
            load_data = pickle.load(f)
        f.close()
       
        '''
        plt.figure(figsize=(10, 10))
    
        for i, image in enumerate(load_data):
            c=i
            if c >= 100:
                break
            plt.subplot(10, 10, i+1)
            plt.imshow(image.reshape((20, 20)), cmap='gray')
            plt.axis('off')
    
        plt.tight_layout()
        plt.show()

    
        for i in range(10):
            adj_mat = load_data[i]
            ret = 0
            while ret != 1:
                NoC = Archi(adj_mat)
                ret = NoC.place_nodes()
                if ret == 1:
                    break
                else:
                    link_length_max += 1
            NoC.plot()
        '''
        if len(load_data) > 2000:
            report_data=np.zeros((2000,3))
        else:
            report_data=np.zeros((len(load_data),3)) #[flit_latency, packet_latency]
 
        for i in range(len(load_data)): #len(load_data)
        #for i in range(1):
            if i >= 2000:
                break
            print("###################")
            print("#######     ", i)
            print("###################")
            # 1. Create NoC
            print("#### 1. Create NoC ####")
            adj_mat = load_data[i]
            adj_mat = np.array(adj_mat)
          
            print(adj_mat.shape)
            print(adj_mat)
            #adj_mat = mattest
        
            filename = "NoCs_data/Mat2NoC" + str(i)
            create_NoC_data(adj_mat, filename)

            print("#### 2. configure ####")
            # 2. configure
            ## a) modify config.ini
            print("  ## a) modify config.ini")
            base_file = "config_template_30%.ini"
            config_writer(base_file, filename)
            ## b) run configuration
            print("  ## b) run configuration")
            configure_AdjMat.main()
            
            # 3. run sim
            print("#### 3. run sim ####")
            os.system("python3 Create_RoutingTable.py")
            #os.system("cp RT.txt urand/.")
            os.system("python3 run_urand.py")

            # 4. save results --> perf dataset
            output = read_results()
            print(output)
            report_data[i] = output

            if i%100==0:
                filename = "/home/mirka/ratatoskr/bin/urand/collectes/scores/uni30/"+name
                with open(filename, 'wb') as f:
                    pickle.dump(report_data, f) 
             
                f.close()
        filename = "/home/mirka/ratatoskr/bin/urand/collectes/scores/uni30/"+name
        with open(filename, 'wb') as f:
            pickle.dump(report_data, f) 
        f.close()


if __name__ == "__main__":
    main()
