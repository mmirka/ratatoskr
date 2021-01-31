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
    int dst_raw = dst_node_id%num;
    
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
    
    //std::cout << "RNoC \n";
    
    int direction;
    std::cout << "src = " << src << " , dst = " << dst_raw << " , column = " << column << " \n";
    
    //std::cout << "read all dir \n";
    
    std::vector<int> destinations_l = globalResources.RoutingTable_RNoC[src_roundabout_ID][column];
    //std::cout << destinations_l.size() << "\n";
    //for (auto c : destinations_l){
    //    std::cout<<c<<" , ";
    //}
    //std::cout << "read dest \n";
    for(int i = 0; i<3; i++){
         if(destinations_l[i] != -1){
              //std::cout << "Select dir : "<< destinations_l[i] <<"\n";
              direction = destinations_l[i];
              break;
         }
    }
    //std::cout << "dir = " << direction << " \n";
    int con_pos;
    /*
    if (direction==0) {
        con_pos = src_node.getConPosOfDir(DIR::Local);
    }
    else if (direction==2) {
        con_pos = src_node.getConPosOfDir(DIR::West);
    }
    else if (direction==1) {
        con_pos = src_node.getConPosOfDir(DIR::East);
    }
    else if (direction==4) {
        con_pos = src_node.getConPosOfDir(DIR::South);
    }
    else if (direction==3) {
        con_pos = src_node.getConPosOfDir(DIR::North);
    }

    //std::cout<<"Src: "<<src<<", Dst: "<<dst_raw<<", Next: "<<direction<<", Connection: "<<con_pos<<std::endl;
    Channel out{con_pos, 0};
    //std::cout << "ROUTING \n channel out = " << out << " , creditCounter value = " << creditCounter.at(out) << " \n end routing \n";
    */
    std::vector<int> directions = destinations_l;
    int Out = directions[0]; 
    int Switch = directions[1]; 
    int Keep = directions[2];
    
    DIR::TYPE dOut; 
    DIR::TYPE dSwitch; 
    DIR::TYPE dKeep;
    
    int dstID_out, dstID_sw, dstID_keep;
    
    // assign directions and save dest_node_ID
    
    if (Out != -1){
        if(Out == 0){
            dOut = DIR::Local;
        }
        else if (Out == 1){
            dOut = DIR::East;
        }
        dstID_out = src_node.getDestIdOfDir(dOut);
    }
    if (Switch != -1) {
        dSwitch = DIR::West;
        dstID_sw = src_node.getDestIdOfDir(dSwitch);
    }
    if (Keep != -1) {
        dKeep = DIR::North;
        dstID_keep = src_node.getDestIdOfDir(dKeep);
    }
    
    // Prioritised routing
    
    if (Out != -1){
        if (Switch == -1 && Keep == -1) {
            con_pos = src_node.getConPosOfDir(dOut); 
            //std::cout << "OUT only choice"<<" _ Src: "<<src<<", Dst: "<<dst_raw<<std::endl;
        }
        else if (Switch != -1 && Keep != -1){ 
            Channel out{src_node.getConPosOfDir(dOut), 0};
            Channel sw{src_node.getConPosOfDir(dSwitch), 0};
            Channel keep{src_node.getConPosOfDir(dKeep), 0};
            std::cout << "dstID_out: "<<dstID_out<<", dstID_sw: "<<dstID_sw<<std::endl;
            if (!is_used(dstID_out)){ 
                con_pos = src_node.getConPosOfDir(dOut);
              //  std::cout << "OUT first choice"<<" _ Src: "<<src<<", Dst: "<<dst_raw<<std::endl;
            }
            else if (!is_used(dstID_sw)){
                con_pos = src_node.getConPosOfDir(dSwitch);
                std::cout << "SWITCH second choice"<<" _ Src: "<<src<<", Dst: "<<dst_raw<<std::endl;
            }
            else{
                con_pos = src_node.getConPosOfDir(dKeep);
                std::cout << "KEEP last choice"<<" _ Src: "<<src<<", Dst: "<<dst_raw<<std::endl;
            }
        }
        else {
            std::cout << "dstID_out: "<<dstID_out<<", dstID_sw: "<<dstID_sw<<std::endl;
            if (Switch != -1){
                Channel out{src_node.getConPosOfDir(dOut), 0};
                Channel sw{src_node.getConPosOfDir(dSwitch), 0};
                
                if (!is_used(dstID_out)){ // 4 = buffer depth
                    con_pos = src_node.getConPosOfDir(dOut);
              //      std::cout << "OUT first choice"<<" _ Src: "<<src<<", Dst: "<<dst_raw<<std::endl;
                }
                else{
                    con_pos = src_node.getConPosOfDir(dSwitch);
                    std::cout << "SWITCH last choice"<<" _ Src: "<<src<<", Dst: "<<dst_raw<<std::endl;
                }
            }
            else{
                Channel out{src_node.getConPosOfDir(dOut), 0};
                Channel keep{src_node.getConPosOfDir(dKeep), 0};
                
                if (!is_used(dstID_out)){ 
                    con_pos = src_node.getConPosOfDir(dOut);
                  //  std::cout << "OUT first choice"<<" _ Src: "<<src<<", Dst: "<<dst_raw<<std::endl;
                }
                else{
                    con_pos = src_node.getConPosOfDir(dKeep);
                    std::cout << "KEEP last choice"<<" _ Src: "<<src<<", Dst: "<<dst_raw<<std::endl;
                }
            }
        }
    }
    else if (Switch != -1){
        std::cout << "dstID_out: "<<dstID_out<<", dstID_sw: "<<dstID_sw<<std::endl;
        if (Keep == -1){
            con_pos = src_node.getConPosOfDir(dSwitch); // Direction Switch
          //  std::cout << "SWITCH only choice"<<" _ Src: "<<src<<", Dst: "<<dst_raw<<std::endl;
        }
        else{ 
            Channel sw{src_node.getConPosOfDir(dSwitch), 0};
            if (!is_used(dstID_sw)){ // --> Switch
                con_pos = src_node.getConPosOfDir(dSwitch);
            //    std::cout << "SWITCH first choice"<<" _ Src: "<<src<<", Dst: "<<dst_raw<<std::endl;
            }
            else{// --> Keep by default
                con_pos = src_node.getConPosOfDir(dKeep);
                std::cout << "KEEP last choice"<<" _ Src: "<<src<<", Dst: "<<dst_raw<<std::endl;
            }
        }
    }
    else if (Keep != -1){
        con_pos = src_node.getConPosOfDir(dKeep); // Direction Keep
       // std::cout << "KEEP only choice"<<" _ Src: "<<src<<", Dst: "<<dst_raw<<std::endl;
    }
    else{
        std::cout<<"Error, no routing for "<<" _ Src: "<<src<<", Dst: "<<dst_raw<<std::endl;
        con_pos = -1;
    }

    //std::cout<<"Src: "<<src<<", Dst: "<<dst<<", Next: "<<direction<<", Connection: "<<con_pos<<std::endl;

    
/*    
    
    if (Out != -1){
        if (Switch == -1 && Keep == -1) {
            con_pos = src_node.getConPosOfDir(dOut); 
            //std::cout << "OUT only choice"<<" _ Src: "<<src<<", Dst: "<<dst_raw<<std::endl;
        }
        else if (Switch != -1 && Keep != -1){ // test credit in order, and assign the first to be free or the last one (keep = lower priority)
            Channel out{src_node.getConPosOfDir(dOut), 0};
            Channel sw{src_node.getConPosOfDir(dSwitch), 0};
            Channel keep{src_node.getConPosOfDir(dKeep), 0};
            
            if (creditCounter.count(out) && creditCounter.at(out)>=4){ // 4 = buffer depth
                con_pos = src_node.getConPosOfDir(dOut);
              //  std::cout << "OUT first choice"<<" _ Src: "<<src<<", Dst: "<<dst_raw<<std::endl;
            }
            else if (creditCounter.count(sw) && creditCounter.at(sw)>=4){
                con_pos = src_node.getConPosOfDir(dSwitch);
                std::cout << "SWITCH second choice"<<" _ Src: "<<src<<", Dst: "<<dst_raw<<std::endl;
            }
            else{
                con_pos = src_node.getConPosOfDir(dKeep);
                std::cout << "KEEP last choice"<<" _ Src: "<<src<<", Dst: "<<dst_raw<<std::endl;
            }
        }
        else {
            if (Switch != -1){
                Channel out{src_node.getConPosOfDir(dOut), 0};
                Channel sw{src_node.getConPosOfDir(dSwitch), 0};
                // if creditcounter(out) is full : con_pos = src_node.getConPosOfDir(1); // --> Switch
                if (creditCounter.count(out) && creditCounter.at(out)>=4){ // 4 = buffer depth
                    con_pos = src_node.getConPosOfDir(dOut);
              //      std::cout << "OUT first choice"<<" _ Src: "<<src<<", Dst: "<<dst_raw<<std::endl;
                }
                else{
                    con_pos = src_node.getConPosOfDir(dSwitch);
                    std::cout << "SWITCH last choice"<<" _ Src: "<<src<<", Dst: "<<dst_raw<<std::endl;
                }
            }
            else{
                Channel out{src_node.getConPosOfDir(dOut), 0};
                Channel keep{src_node.getConPosOfDir(dKeep), 0};
                // if creditcounter(out) is full : con_pos = src_node.getConPosOfDir(2); // --> Keep
                if (creditCounter.count(out) && creditCounter.at(out)>=4){ // 4 = buffer depth
                    con_pos = src_node.getConPosOfDir(dOut);
                  //  std::cout << "OUT first choice"<<" _ Src: "<<src<<", Dst: "<<dst_raw<<std::endl;
                }
                else{
                    con_pos = src_node.getConPosOfDir(dKeep);
                    std::cout << "KEEP last choice"<<" _ Src: "<<src<<", Dst: "<<dst_raw<<std::endl;
                }
            }
        }
    }
    else if (Switch != -1){
        if (Keep == -1){
            con_pos = src_node.getConPosOfDir(dSwitch); // Direction Switch
          //  std::cout << "SWITCH only choice"<<" _ Src: "<<src<<", Dst: "<<dst_raw<<std::endl;
        }
        else{ // test credit in order
            //if creditcounter(switch) is available: src_node.getConPosOfDir(1); // --> Switch
            // else src_node.getConPosOfDir(2); // --> Keep by default
            Channel sw{src_node.getConPosOfDir(dSwitch), 0};
            if (creditCounter.count(sw) && creditCounter.at(sw)>=4){ // 4 = buffer depth
                con_pos = src_node.getConPosOfDir(dSwitch);
            //    std::cout << "SWITCH first choice"<<" _ Src: "<<src<<", Dst: "<<dst_raw<<std::endl;
            }
            else{
                con_pos = src_node.getConPosOfDir(dKeep);
                std::cout << "KEEP last choice"<<" _ Src: "<<src<<", Dst: "<<dst_raw<<std::endl;
            }
        }
    }
    else if (Keep != -1){
        con_pos = src_node.getConPosOfDir(dKeep); // Direction Keep
       // std::cout << "KEEP only choice"<<" _ Src: "<<src<<", Dst: "<<dst_raw<<std::endl;
    }
    else{
        std::cout<<"Error, no routing for "<<" _ Src: "<<src<<", Dst: "<<dst_raw<<std::endl;
        con_pos = -1;
    }

    //std::cout<<"Src: "<<src<<", Dst: "<<dst<<", Next: "<<direction<<", Connection: "<<con_pos<<std::endl;

 */ 
    return con_pos;
}

bool RNoC_Table::is_used(int dst_node_id)
{
    std::cout<<"check "<<dst_node_id<<std::endl;
    int nbNode = globalResources.nodes.size()/2;
    std::cout<<"nbNode "<<nbNode<<std::endl;
    bool check = false;
    Node node = globalResources.nodes.at(dst_node_id); // node of interest
    std::cout<<"dicho 0 "<<std::endl;
    for(auto& n_id:node.connectedNodes){ // for all nodes connected to node
        std::cout<<"connected node "<<n_id<<std::endl;
        if(n_id%nbNode == dst_node_id){
            std::cout<<"___ PE   -->  PASS"<<std::endl;
        }
        else{
	    Node connectedRouter = globalResources.nodes.at(n_id); // get connectedRouter info
	    Connection* conn = &globalResources.connections.at(connectedRouter.getConnWithNode(node)); // get connection from connectedRouter to node
	    int conPos = connectedRouter.getConnPosition(conn->id); // get corresponding conPos
	    Channel ch{conPos, 0};  // channel to check
	    std::cout<<"dicho 1 "<<std::endl;
	    // check creditCounter at ch
	    std::map<Channel, int>* ptr_cC;
	    std::map<Channel, int> cC;
	    ptr_cC = globalReport.ptr_creditCounters[n_id];
	    cC = *ptr_cC;
	    std::cout<<"Src "<<n_id<<", Dst "<<dst_node_id<<", Cc "<<cC.at(ch)<<std::endl;
	    if (cC.count(ch) && cC.at(ch)<4){
	        //std::cout<<"Src "<<n_id<<", Dst "<<dst_node_id<<", Cc "<<cC.at(ch)<<std::endl;
	        std::cout<<"Set check to true --> is_used"<<std::endl;
	        check = true;
	        //break;
	    }
	    std::cout<<"dicho 2 "<<std::endl;
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
