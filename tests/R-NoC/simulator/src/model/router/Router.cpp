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
//#include <model/router/routings/XYZRouting.h>
//#include <model/router/routings/HeteroXYZRouting.h>
//#include <model/router/routings/RandomXYZRouting.h>
//#include <model/router/routings/RandomHeteroXYZRouting.h>
//#include <model/router/routings/ZXYZRouting.h>
//#include <model/router/routings/TableRouting.h>
#include <model/router/routings/RNoC_Table.h>
#include "Router.h"

Router::Router(sc_module_name nm, Node& node)
        :
        node(node)
{
    int numOfRouters = static_cast<int>(globalResources.nodes.size() / 2);
    this->id = node.id%(numOfRouters);
    this->dbid = rep.registerElement("Router", this->id);

    rep.reportAttribute(dbid, "pos_x", std::to_string(node.pos.x));
    rep.reportAttribute(dbid, "pos_y", std::to_string(node.pos.y));
    rep.reportAttribute(dbid, "pos_z", std::to_string(node.pos.z));
    rep.reportAttribute(dbid, "clock", std::to_string(node.type->clockDelay));
    rep.reportAttribute(dbid, "type", node.type->model);

    /*if(node.type->routing=="XYZ")
        routingAlg = std::make_unique<XYZRouting>();
    else if(node.type->routing=="HeteroXYZ")
        routingAlg = std::make_unique<HeteroXYZRouting>();
    else if(node.type->routing=="RandomXYZ")
        routingAlg = std::make_unique<RandomXYZRouting>();
    else if(node.type->routing=="RandomHeteroXYZ")
        routingAlg = std::make_unique<RandomHeteroXYZRouting>();
    else if(node.type->routing=="ZXYZ")
        routingAlg = std::make_unique<ZXYZRouting>();
    else if(node.type->routing=="Table")
        routingAlg = std::make_unique<TableRouting>();
    else*/ 
    if(node.type->routing=="RNoC"){
        routingAlg = std::make_unique<RNoC_Table>();
    }    
}

Router::~Router()
{
    for (auto& dir_buf:buffers) {
        for (auto& vc_buf:*dir_buf)
            vc_buf->flush();
        dir_buf->clear();
    }
    buffers.clear();
}
