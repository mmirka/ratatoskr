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
###############################################################################
import numpy as np
import pickle
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
plt.rcParams.update({'figure.max_open_warning': 0})
from PyPDF2 import PdfFileMerger
import glob as glob
import os
from matplotlib.lines import Line2D
###############################################################################

def my_plot_latencies2(results0, results1):

    latenciesFlit0 = results0['latenciesFlit']
    latenciesNetwork0 = results0['latenciesNetwork']
    latenciesPacket0 = results0['latenciesPacket']
    #injectionRates = results['injectionRates']
    injectionRates0 = [1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95]

    meanLatenciesFlit0 = np.mean(latenciesFlit0, axis=1)
    meanLatenciesPacket0 = np.mean(latenciesPacket0, axis=1)
    meanLatenciesNetwork0 = np.mean(latenciesNetwork0, axis=1)
    stdLatenciesFlit0 = np.std(latenciesFlit0, axis=1)
    stdLatenciesPacket0 = np.std(latenciesPacket0, axis=1)
    stdLatenciesNetwork0 = np.std(latenciesNetwork0, axis=1)

    fig = plt.figure(figsize=[16,8])
    plt.ylabel('Latencies in ns', fontsize=50)
    plt.xlabel('Injection Rate (%)', fontsize=50)
    plt.ylim([20, 100])
    plt.xlim([0, 60])
    linestyle = {'linestyle': '--', 'linewidth': 5, 'markeredgewidth': 10,
                 'elinewidth': 1, 'capsize': 10}
    #plt.errorbar(injectionRates0, meanLatenciesFlit0, yerr=stdLatenciesFlit0,
    #             color='r', **linestyle, marker='*')
    plt.errorbar(injectionRates0, meanLatenciesNetwork0, #yerr=stdLatenciesNetwork, 
                 color='k', **linestyle,marker='^')
    #plt.errorbar(injectionRates0, meanLatenciesPacket0, yerr=stdLatenciesPacket0,
    #             color='g', **linestyle, marker='^')
                 
                 
    latenciesFlit1 = results1['latenciesFlit']
    latenciesNetwork1 = results1['latenciesNetwork']
    latenciesPacket1 = results1['latenciesPacket']
    #injectionRates = results['injectionRates']
    injectionRates1 = [1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95]

    meanLatenciesFlit1 = np.mean(latenciesFlit1, axis=1)
    meanLatenciesPacket1 = np.mean(latenciesPacket1, axis=1)
    meanLatenciesNetwork1 = np.mean(latenciesNetwork1, axis=1)
    stdLatenciesFlit1 = np.std(latenciesFlit1, axis=1)
    stdLatenciesPacket1 = np.std(latenciesPacket1, axis=1)
    stdLatenciesNetwork1 = np.std(latenciesNetwork1, axis=1)

    #fig = plt.figure()
    #plt.ylabel('Latencies in ns', fontsize=11)
    #plt.xlabel('Injection Rate', fontsize=11)
    #plt.ylim([0, 150])
    #plt.xlim([0, 100])
    #linestyle = {'linestyle': '--', 'linewidth': 1, 'markeredgewidth': 1,
    #             'elinewidth': 1, 'capsize': 10}
    #plt.errorbar(injectionRates1, meanLatenciesFlit1, yerr=stdLatenciesFlit1,
    #             color='r', **linestyle, marker='*')
    plt.errorbar(injectionRates1, meanLatenciesNetwork1, #yerr=stdLatenciesNetwork, 
                 color='k', **linestyle,marker='s')
    #plt.errorbar(injectionRates1, meanLatenciesPacket1, yerr=stdLatenciesPacket1,
    #             color='g', **linestyle, marker='^')
    
    plt.legend(['WGAN', 'RWGAN'], fontsize=40)
    #fig.suptitle('Latencies', fontsize=16)
    plt.tick_params(axis='both', which='major', pad=0)
    plt.xticks(fontsize=45)
    plt.yticks(fontsize=45)
    plt.tight_layout()
    #plt.show()
    plt.grid()
    fig.savefig('latencies.pdf')
    

def my_plot_latencies(results0, results1, results2, results3, results4, results5):

    latenciesFlit0 = results0['latenciesFlit']
    latenciesNetwork0 = results0['latenciesNetwork']
    latenciesPacket0 = results0['latenciesPacket']
    #injectionRates = results['injectionRates']
    injectionRates0 = [1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95]

    meanLatenciesFlit0 = np.mean(latenciesFlit0, axis=1)
    meanLatenciesPacket0 = np.mean(latenciesPacket0, axis=1)
    meanLatenciesNetwork0 = np.mean(latenciesNetwork0, axis=1)
    stdLatenciesFlit0 = np.std(latenciesFlit0, axis=1)
    stdLatenciesPacket0 = np.std(latenciesPacket0, axis=1)
    stdLatenciesNetwork0 = np.std(latenciesNetwork0, axis=1)

    fig = plt.figure()
    plt.ylabel('Latencies in ns', fontsize=11)
    plt.xlabel('Injection Rate (%)', fontsize=11)
    plt.ylim([0, 100])
    plt.xlim([0, 60])
    linestyle = {'linestyle': '--', 'linewidth': 1, 'markeredgewidth': 1,
                 'elinewidth': 1, 'capsize': 10}
    #plt.errorbar(injectionRates0, meanLatenciesFlit0, yerr=stdLatenciesFlit0,
    #             color='r', **linestyle, marker='*')
    plt.errorbar(injectionRates0, meanLatenciesNetwork0, #yerr=stdLatenciesNetwork, 
                 color='b', **linestyle,marker='s')
    #plt.errorbar(injectionRates0, meanLatenciesPacket0, yerr=stdLatenciesPacket0,
    #             color='g', **linestyle, marker='^')
                 
                 
    latenciesFlit1 = results1['latenciesFlit']
    latenciesNetwork1 = results1['latenciesNetwork']
    latenciesPacket1 = results1['latenciesPacket']
    #injectionRates = results['injectionRates']
    injectionRates1 = [1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95]

    meanLatenciesFlit1 = np.mean(latenciesFlit1, axis=1)
    meanLatenciesPacket1 = np.mean(latenciesPacket1, axis=1)
    meanLatenciesNetwork1 = np.mean(latenciesNetwork1, axis=1)
    stdLatenciesFlit1 = np.std(latenciesFlit1, axis=1)
    stdLatenciesPacket1 = np.std(latenciesPacket1, axis=1)
    stdLatenciesNetwork1 = np.std(latenciesNetwork1, axis=1)

    #fig = plt.figure()
    #plt.ylabel('Latencies in ns', fontsize=11)
    #plt.xlabel('Injection Rate', fontsize=11)
    #plt.ylim([0, 150])
    #plt.xlim([0, 100])
    #linestyle = {'linestyle': '--', 'linewidth': 1, 'markeredgewidth': 1,
    #             'elinewidth': 1, 'capsize': 10}
    #plt.errorbar(injectionRates1, meanLatenciesFlit1, yerr=stdLatenciesFlit1,
    #             color='r', **linestyle, marker='*')
    plt.errorbar(injectionRates1, meanLatenciesNetwork1, #yerr=stdLatenciesNetwork, 
                 color='k', **linestyle,marker='s')
    #plt.errorbar(injectionRates1, meanLatenciesPacket1, yerr=stdLatenciesPacket1,
    #             color='g', **linestyle, marker='^')
    
    
    latenciesNetwork2 = results2['latenciesNetwork']
    injectionRates2 = [1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95]

    meanLatenciesNetwork2 = np.mean(latenciesNetwork2, axis=1)
    stdLatenciesNetwork2 = np.std(latenciesNetwork2, axis=1)

    #fig = plt.figure()
    #plt.ylabel('Latencies in ns', fontsize=11)
    #plt.xlabel('Injection Rate', fontsize=11)
    #plt.ylim([0, 150])
    #plt.xlim([0, 100])
    #linestyle = {'linestyle': '--', 'linewidth': 1, 'markeredgewidth': 1,
    #             'elinewidth': 1, 'capsize': 10}
    #plt.errorbar(injectionRates0, meanLatenciesFlit0, yerr=stdLatenciesFlit0,
    #             color='r', **linestyle, marker='*')
    plt.errorbar(injectionRates2, meanLatenciesNetwork2, #yerr=stdLatenciesNetwork, 
                 color='b', **linestyle,marker='*')
    #plt.errorbar(injectionRates0, meanLatenciesPacket0, yerr=stdLatenciesPacket0,
    #             color='g', **linestyle, marker='^')
    
    latenciesNetwork3 = results3['latenciesNetwork']
    injectionRates3 = [1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95]

    meanLatenciesNetwork3 = np.mean(latenciesNetwork3, axis=1)
    stdLatenciesNetwork3 = np.std(latenciesNetwork3, axis=1)

    #fig = plt.figure()
    #plt.ylabel('Latencies in ns', fontsize=11)
    #plt.xlabel('Injection Rate', fontsize=11)
    #plt.ylim([0, 150])
    #plt.xlim([0, 100])
    #linestyle = {'linestyle': '--', 'linewidth': 1, 'markeredgewidth': 1,
    #             'elinewidth': 1, 'capsize': 10}
    #plt.errorbar(injectionRates0, meanLatenciesFlit0, yerr=stdLatenciesFlit0,
    #             color='r', **linestyle, marker='*')
    plt.errorbar(injectionRates3, meanLatenciesNetwork3, #yerr=stdLatenciesNetwork, 
                 color='k', **linestyle,marker='*')
    #plt.errorbar(injectionRates0, meanLatenciesPacket0, yerr=stdLatenciesPacket0,
    #             color='g', **linestyle, marker='^')
    
    latenciesNetwork4 = results4['latenciesNetwork']
    injectionRates4 = [1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95]

    meanLatenciesNetwork4 = np.mean(latenciesNetwork4, axis=1)
    stdLatenciesNetwork4 = np.std(latenciesNetwork4, axis=1)

    #fig = plt.figure()
    #plt.ylabel('Latencies in ns', fontsize=11)
    #plt.xlabel('Injection Rate', fontsize=11)
    #plt.ylim([0, 150])
    #plt.xlim([0, 100])
    #linestyle = {'linestyle': '--', 'linewidth': 1, 'markeredgewidth': 1,
    #             'elinewidth': 1, 'capsize': 10}
    #plt.errorbar(injectionRates0, meanLatenciesFlit0, yerr=stdLatenciesFlit0,
    #             color='r', **linestyle, marker='*')
    plt.errorbar(injectionRates4, meanLatenciesNetwork4, #yerr=stdLatenciesNetwork, 
                 color='b', **linestyle,marker='^')
    #plt.errorbar(injectionRates0, meanLatenciesPacket0, yerr=stdLatenciesPacket0,
    #             color='g', **linestyle, marker='^')
                              
    latenciesNetwork5 = results5['latenciesNetwork']
    injectionRates5 = [1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95]

    meanLatenciesNetwork5 = np.mean(latenciesNetwork5, axis=1)
    stdLatenciesNetwork5 = np.std(latenciesNetwork5, axis=1)

    #fig = plt.figure()
    #plt.ylabel('Latencies in ns', fontsize=11)
    #plt.xlabel('Injection Rate', fontsize=11)
    #plt.ylim([0, 150])
    #plt.xlim([0, 100])
    #linestyle = {'linestyle': '--', 'linewidth': 1, 'markeredgewidth': 1,
    #             'elinewidth': 1, 'capsize': 10}
    #plt.errorbar(injectionRates0, meanLatenciesFlit0, yerr=stdLatenciesFlit0,
    #             color='r', **linestyle, marker='*')
    plt.errorbar(injectionRates5, meanLatenciesNetwork5, #yerr=stdLatenciesNetwork, 
                 color='k', **linestyle,marker='^')
    #plt.errorbar(injectionRates0, meanLatenciesPacket0, yerr=stdLatenciesPacket0,
    #             color='g', **linestyle, marker='^')
                 
    plt.grid()
    #plt.legend(['Flit', 'Network', 'Packet'])
    fig.suptitle('Latencies', fontsize=16)
    # plt.show()
    fig.savefig('latencies.pdf')

def my_plot_latencies_rapido(results):
    latencies = []
    meanLatencies = []
    stdLatencies = []
    injectionRates = results[0][0]['injectionRates'] 
    for i in range(len(injectionRates)):
        injectionRates[i] = injectionRates[i]*3200
    print(injectionRates)
    for i in range(len(results)):
        lat_nbc = []
        meanLat_nbc = []
        stdLat_nbc = []
        for j in range(len(results[i])):
            lat_nbc.append(results[i][j]['latenciesNetwork'])
            #print(lat_nbc[0])
            meanLat_nbc.append(np.mean(lat_nbc[j], axis=1))
            #print(meanLat_nbc[0])
            stdLat_nbc.append(np.std(lat_nbc[j], axis=1))
        latencies.append(lat_nbc)
        meanLatencies.append(meanLat_nbc)
        stdLatencies.append(stdLat_nbc)
    print(meanLatencies)
    #injectionRates = [1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]
    fig, ax = plt.subplots()
    plt.ylabel('Latencies (ns)', fontsize=18)
    plt.xlabel('Injection Rate (%)', fontsize=18)
    plt.ylim([30, 100])
    plt.xlim([10, 50])
    linestyle1 = {'linestyle': '--', 'linewidth': 1, 'markeredgewidth': 1,
                 'elinewidth': 1, 'capsize': 20, 'markersize':8}
    linestyle2 = {'linestyle': '-', 'linewidth': 1, 'markeredgewidth': 1,
                 'elinewidth': 1, 'capsize': 20, 'markersize':8}
    colors = ['k','b','r']#,'g','c']#,'y', 'm']
    marker = ['*', 'x', '+', 'o', '^', 's', '^','*', 'x', 'o']
    linesSet = ['-','-','-','-','-']
    
    for i in range(len(results)):
        for j in range(len(results[i])):
            if i == 0:
                plt.errorbar(injectionRates, meanLatencies[i][j], #yerr=stdLatenciesNetwork, 
                    color=colors[i], **linestyle2, marker = marker[i])
            else:
                plt.errorbar(injectionRates, meanLatencies[i][j], #yerr=stdLatenciesNetwork, 
                    color=colors[i], **linestyle2, marker = marker[i])

    plt.grid()
    lines1 = [Line2D([0], [0], color=colors[i], linewidth=1, linestyle=linesSet[i], marker=marker[i], markersize=8) for i in range(3)]#, marker=marker[i]) for i in range(2)]
    lines2 = [Line2D([0], [0], color='r', linewidth=1, linestyle=linesSet[i], marker=marker[i],markersize=8) for i in range(5)]
    #labels = ['11 connections', '15 connections', '16 connections']
    labels = ['WGAN', 'RWGAN']
    plt.ylim([30, 100])
    plt.xlim([10, 50])
    ax.axis()
    ax.set_xlim(10, 50)
    # specify the lines and labels of the first legend
    leg1 = ax.legend(lines1, ['11 links', '15 links', '16 links'], loc='upper left', frameon=True, title="Class", fontsize=14, )
    title1 = leg1.get_title()
    title1.set_fontsize(16)
    # Create the second legend and add the artist manually.
    #from matplotlib.legend import Legend
    #leg = Legend(ax, lines2, ['15 links', '16 links', '14 links', '15 links', '14 links'], loc='upper right', frameon=True, title="RWGAN", fontsize=14)
    #title2 = leg.get_title()
    #title2.set_fontsize(16)
    #ax.add_artist(leg)
    ax.set_xlim(10, 50)
    
    plt.ylim([30, 100])
    plt.xlim([10, 50])
    ax.set_xlim(10, 50)
    
    #plt.legend(lines, labels, fontsize=14)
    #frame1 = leg1.get_frame()
    #frame2 = leg.get_frame()
    #frame1.set_facecolor('green')
    #frame2.set_facecolor('green')
    #plt.tick_params(axis='both', which='major', pad=0)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.tight_layout()
    plt.ylim([30, 100])
    plt.xlim([10, 50])
    #plt.legend(['Flit', 'Network', 'Packet'])
    #fig.suptitle('Latencies', fontsize=16)
    plt.setp(ax, xlim=[10, 50], ylim=[30, 100])
    plt.show()
    fig.savefig('latencies-3classes.pdf')


def plot_latencies(results):
    """
    Read the raw results from a dictionary of objects, then plot the latencies.

    Parameters:
        - results: a dictionary of raw data from the pickle file.

    Return:
        - None.
    """
    latenciesFlit = results['latenciesFlit']
    latenciesNetwork = results['latenciesNetwork']
    latenciesPacket = results['latenciesPacket']
    #injectionRates = results['injectionRates']
    injectionRates = [1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95]

    meanLatenciesFlit = np.mean(latenciesFlit, axis=1)
    meanLatenciesPacket = np.mean(latenciesPacket, axis=1)
    meanLatenciesNetwork = np.mean(latenciesNetwork, axis=1)
    stdLatenciesFlit = np.std(latenciesFlit, axis=1)
    stdLatenciesPacket = np.std(latenciesPacket, axis=1)
    stdLatenciesNetwork = np.std(latenciesNetwork, axis=1)

    fig = plt.figure()
    plt.ylabel('Latencies in ns', fontsize=11)
    plt.xlabel('Injection Rate', fontsize=11)
    plt.ylim([0, 150])
    plt.xlim([0, 100])
    linestyle = {'linestyle': '--', 'linewidth': 1, 'markeredgewidth': 1,
                 'elinewidth': 1, 'capsize': 10}
    plt.errorbar(injectionRates, meanLatenciesFlit, yerr=stdLatenciesFlit,
                 color='r', **linestyle, marker='*')
    plt.errorbar(injectionRates, meanLatenciesNetwork, #yerr=stdLatenciesNetwork, 
                 color='b', **linestyle,marker='s')
    plt.errorbar(injectionRates, meanLatenciesPacket, yerr=stdLatenciesPacket,
                 color='g', **linestyle, marker='^')

    plt.legend(['Flit', 'Network', 'Packet'])
    #fig.suptitle('Latencies', fontsize=16)
    # plt.show()
    fig.savefig('latencies.pdf')
###############################################################################


def plot_VCUsage_stats(inj_dfs, inj_rates):
    """
    Plot the VC usage statistics.

    Parameteres:
        - inj_dfs: the data frames of an injection rate.
        - inj_rates: the number of injection rates.

    Return:
        - None.
    """
    for inj_df, inj_rate in zip(inj_dfs, inj_rates):
        for layer_id, df in enumerate(inj_df):
            fig = plt.figure()  # plot a figure for each inj_rate and layer
            plt.title('Layer ' + str(layer_id) +
                      ', Injection Rate = ' + str(inj_rate))
            plt.ylabel('Count', fontsize=11)
            plt.xlabel('VC Usage', fontsize=11)
            for col in df.columns.levels[0].values:
                plt.errorbar(df.index.values, df[col, 'mean'].values,
                             yerr=df[col, 'std'].values)
            plt.legend(df.columns.levels[0].values)
            # plt.show()
            fig.savefig('VC_' + str(layer_id) + '_' + str(inj_rate) + '.pdf')
###############################################################################


def plot_BuffUsage_stats(inj_dicts, inj_rates):
    """
    Plot the buffer usage statistics.

    Parameters:
        - inj_dicts: the data dictionaries of an injection rate.
        - inj_rates: the number of injection rates.

    Return:
        - None.
    """
    for inj_dict, inj_rate in zip(inj_dicts, inj_rates):
        for layer_id, layer_name in enumerate(inj_dict):
            layer_dict = inj_dict[layer_name]
            fig = plt.figure()
            for it, d in enumerate(layer_dict):
                df = layer_dict[d]
                if not df.empty:
                    ax = fig.add_subplot(3, 2, it+1, projection='3d')
                    lx = df.shape[0]
                    ly = df.shape[1]
                    xpos = np.arange(0, lx, 1)
                    ypos = np.arange(0, ly, 1)
                    xpos, ypos = np.meshgrid(xpos, ypos, indexing='ij')

                    xpos = xpos.flatten()
                    ypos = ypos.flatten()
                    zpos = np.zeros(lx*ly)

                    dx = 1 * np.ones_like(zpos)
                    dy = dx.copy()
                    dz = df.values.flatten()

                    ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color='b')

                    ax.set_yticks(ypos)
                    ax.set_xlabel('Buffer Size')
                    ax.set_ylabel('VC Index')
                    ax.set_zlabel('Count')
                    ax.set_title('Direction:'+str(d))

            fig.suptitle('Layer: '+str(layer_name)+', Injection Rate = '
                         + str(inj_rate), fontsize=16)
            # plt.show()
            fig.savefig('Buff_' + str(layer_id) + '_' + str(inj_rate) + '.pdf')
###############################################################################


def read_raw_results(results_file):
    """
    Read the raw results from the pickle file.

    Parameters:
        - results_file: the path to the pickle file.

    Return:
        - results: a dictionary of objects.
    """
    results = None
    with open(results_file, 'rb') as f:
        results = pickle.load(f)
    return results
###############################################################################


def merge_pdfs(output_path):
    """Merge the generated reports in one pdf."""
    try:
        os.remove(output_path)
    except FileNotFoundError:
        pass

    input_paths = glob.glob('*.pdf')
    input_paths.sort()
    pdf_merger = PdfFileMerger()

    for path in input_paths:
        pdf_merger.append(path)

    with open(output_path, 'wb') as fileobj:
        pdf_merger.write(fileobj)

    for path in input_paths:
        os.remove(path)
###############################################################################


def main():
    """Main Point of Execution."""
    #results = read_raw_results('rawResults.pkl')
    #results0 = read_raw_results('results_NoC-compare/rawResults1-0.pkl')
    #results1 = read_raw_results('results_NoC-compare/rawResults1-1.pkl')
    #results2 = read_raw_results('results_NoC-compare/rawResults2-0.pkl')
    #results3 = read_raw_results('results_NoC-compare/rawResults2-1.pkl')
    #results4 = read_raw_results('results_NoC-compare/rawResults3-0.pkl')
    #results5 = read_raw_results('results_NoC-compare/rawResults3-1.pkl')
    
    results=[]
    for j in range(11,17,1):
        r_nbc = []
        if j == 11 or j == 15 or j == 16:
            for i in range(5):
                name = 'results_NoC-compare/set-rapido/scores/test_set_RW-nbc'+str(int(j))+'i' + str(int(i+1)) + '.pkl' 
                r = read_raw_results(name)
                r_nbc.append(r)
            results.append(r_nbc)
    #    plot_latencies(results)
    #for i in range(2):
    #    r_type = []
    #    if i == 0:
    #        name = 'results_NoC-compare/set-rapido/scores/test_set_cW-compare-'
    #    else:
    #        name = 'results_NoC-compare/set-rapido/scores/test_set_cRW-compare-'
    #    for i in range(5):
    #        filename = name +str(i)+ '.pkl'
    #        r = read_raw_results(filename)
    #        r_type.append(r)
    #    results.append(r_type)
        
    my_plot_latencies_rapido(results)
    
    #my_plot_latencies2(results4, results5)
    
    #my_plot_latencies(results0, results1, results2, results3, results4, results5)

    #plot_VCUsage_stats(results['VCUsage'], results['injectionRates'])

    #plot_BuffUsage_stats(results['BuffUsage'], results['injectionRates'])

    #merge_pdfs('performance_buffer_VCUsage_report.pdf')
###############################################################################


if __name__ == '__main__':
    main()
