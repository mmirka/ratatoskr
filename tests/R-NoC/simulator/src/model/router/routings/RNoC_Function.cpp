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
#include "RNoC_Table.h"

int RNoC_Table::route_credit(int src_node_id, int dst_node_id, std::map<Channel, int> creditCounter)
{
    Node src_node = globalResources.nodes.at(src_node_id);
    Node dst_node = globalResources.nodes.at(dst_node_id);
    
    int column = -1;
    
    int num = globalResources.nodes.size()/2;
    int src = src_node_id%num;
    int dst = dst_node_id%num;
    
    int con_pos;
    
    std::string dir_dst;
    if (dst == 64) dir_dst = "South";
    else if (dst == 65) dir_dst = "East";
    else if (dst == 66) dir_dst = "North";
    else if (dst == 67) dir_dst = "West";
    else if (dst == 68) dir_dst = "Local";
    
    /*FOR XY ROUTING WITH MESH, COMMENT IF TEST RNOC ONLY
    // 1. get local IDs (src / dest)
    int src_roundabout_ID = src % globalResources.nbRouters_Roundabout; 
    int src_roundabout_ID_min = src - src_roundabout_ID; 
    int src_roundabout_ID_max = src + (globalResources.nbRouters_Roundabout-src_roundabout_ID-1);
    
    int local_src = src_roundabout_ID_min;
    
    int dst_roundabout_ID = dst_raw % globalResources.nbRouters_Roundabout; 
    int dst_roundabout_ID_min = dst_raw - dst_roundabout_ID; 
    int dst_roundabout_ID_max = dst_raw + (globalResources.nbRouters_Roundabout-dst_roundabout_ID-1);
    
    int local_dst = dst_roundabout_ID_min;
    
    Node local_src_node = globalResources.nodes.at(local_src);
    Node local_dst_node = globalResources.nodes.at(local_dst);
    Vec3D<float> src_pos = local_src_node.pos;
    Vec3D<float> dst_pos = local_dst_node.pos;
     
    //2. check if it is the same roundabout, if yes, destination = local, else XY routing
    if (local_src == local_dst) { // destination = local
        column = 0; // column index in RT
    }
    else{ // XY 
        if (dst_pos.x<src_pos.x) {
            //std::cout << "dst_pos.x = " << dst_pos.x << " , src_pos.x = " << src_pos.x << " \n";
            column = 4;
        }
        else if (dst_pos.x>src_pos.x) {
            //std::cout << "dst_pos.x = " << dst_pos.x << " , src_pos.x = " << src_pos.x << " \n";
            column = 2;
        }
        else if (dst_pos.y<src_pos.y) {
            //std::cout << "dst_pos.x = " << dst_pos.x << " , src_pos.x = " << src_pos.x << " \n";
            column = 1;
        }
        else if (dst_pos.y>src_pos.y) {
            //std::cout << "dst_pos.x = " << dst_pos.x << " , src_pos.x = " << src_pos.x << " \n";
            column = 3;
        }
    }
    */
    
    if (src == dst)
        con_pos = src_node.getConPosOfDir(DIR::Local);
    else{
        if (src_node.RNoC_moduleType == "Buffer" || (src_node.RNoC_moduleType == "Mux" || src_node.RNoC_moduleType == "InputController")){
            con_pos = src_node.getConPosOfDir(DIR::Keep);
        }
        else {
            if (std::count(src_node.Outputs.begin(), src_node.Outputs.end(), dir_dst))
                con_pos = src_node.getConPosOfDir(DIR::Out);
            else con_pos = src_node.getConPosOfDir(DIR::Keep);
        }
        
    }
    
    
    std::cout<<"Src type: "<<src_node.RNoC_moduleType<<std::endl;
    std::cout<<"Src: "<<src<<", Dst: "<<dst<<", Connection: "<<con_pos<<std::endl;

    

    return con_pos;
}

bool RNoC_Table::is_used(int dst_node_id)
{
    //std::cout<<"check "<<dst_node_id<<std::endl;
    int nbNode = globalResources.nodes.size()/2;
    //std::cout<<"nbNode "<<nbNode<<std::endl;
    bool check = false;
    Node node = globalResources.nodes.at(dst_node_id); // node of interest
    //std::cout<<"dicho 0 "<<std::endl;
    for(auto& n_id:node.connectedNodes){ // for all nodes connected to node
        //std::cout<<"connected node "<<n_id<<std::endl;
        if(n_id%nbNode == dst_node_id){
            //std::cout<<"___ PE   -->  PASS"<<std::endl;
        }
        else{
	    Node connectedRouter = globalResources.nodes.at(n_id); // get connectedRouter info
	    Connection* conn = &globalResources.connections.at(connectedRouter.getConnWithNode(node)); // get connection from connectedRouter to node
	    int conPos = connectedRouter.getConnPosition(conn->id); // get corresponding conPos
	    Channel ch{conPos, 0};  // channel to check
	    //std::cout<<"dicho 1 "<<std::endl;
	    // check creditCounter at ch
	    std::map<Channel, int>* ptr_cC;
	    std::map<Channel, int> cC;
	    ptr_cC = globalReport.ptr_creditCounters[n_id];
	    cC = *ptr_cC;
	    //std::cout<<"Src "<<n_id<<", Dst "<<dst_node_id<<", Cc "<<cC.at(ch)<<std::endl;
	    if (cC.count(ch) && cC.at(ch)<4){
	        //std::cout<<"Src "<<n_id<<", Dst "<<dst_node_id<<", Cc "<<cC.at(ch)<<std::endl;
	        //std::cout<<"Set check to true --> is_used"<<std::endl;
	        check = true;
	        //break;
	    }
	    //std::cout<<"dicho 2 "<<std::endl;
        }
    }
    return check;
}

/*
int RNoC_Table::route(int src_node_id, int dst_node_id, std::map<Channel, int> creditCounter)
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
*/
