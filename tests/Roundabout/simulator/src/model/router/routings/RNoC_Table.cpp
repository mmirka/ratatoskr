/*******************************************************************************
 * Copyright (C) 2018 Jan Moritz Joseph
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 ******************************************************************************/
#include "TableRouting.h"

int TableRouting::route(int src_node_id, int dst_node_id, std::map<Channel, int> creditCounter)
{
    Node src_node = globalResources.nodes.at(src_node_id);
    
    int con_pos;
    std::vector<int> directions;
    int Out, Switch, Keep;
    int num = globalResources.nodes.size()/2;
    int src = src_node_id%num;
    int dst = dst_node_id%num;
    
    directions = globalResources.RoutingTable_RNoC[dst][src];
    Out = directions[0]; Switch = directions[1]; Keep = directions[2];
    
    if (Out != -1){
        if (Switch == -1 && Keep == -1) {
            con_pos = src_node.getConPosOfDir(0); // Direction OUT
        }
        else if (Switch != -1 && Keep != -1){ // test credit in order, and assign the first to be free or the last one (keep = lower priority)
            Channel out{conPos, vc};
            if (creditCounter.count(out) && creditCounter.at(out)>0)
            // if creditcounter(out) is available: src_node.getConPosOfDir(0); // --> Out
            // else if creditcounter(switch) is available: src_node.getConPosOfDir(1); // --> Switch
            // else src_node.getConPosOfDir(2); // --> Keep by default
        }
        else {
            if (Swith != -1){
                // if creditcounter(out) is full : con_pos = src_node.getConPosOfDir(1); // --> Switch
                // else con_pos = src_node.getConPosOfDir(0); // --> Out
            }
            else{
                // if creditcounter(out) is full : con_pos = src_node.getConPosOfDir(2); // --> Keep
                // else con_pos = src_node.getConPosOfDir(0); // --> Out
            }
        }
    }
    else if (Switch != -1){
        if (Keep == -1){
            con_pos = src_node.getConPosOfDir(1); // Direction Switch
        }
        else{ // test credit in order
            //if creditcounter(switch) is available: src_node.getConPosOfDir(1); // --> Switch
            // else src_node.getConPosOfDir(2); // --> Keep by default
        }
    }
    else if (Keep != -1){
        con_pos = src_node.getConPosOfDir(2); // Direction Keep
    }
    else{
        std::cout<<"Error, no routing for: Src = "<<src<<", Dst = "<<dst<<std::endl;
        con_pos = -1
    }

    //std::cout<<"Src: "<<src<<", Dst: "<<dst<<", Next: "<<direction<<", Connection: "<<con_pos<<std::endl;

    return con_pos;
}
