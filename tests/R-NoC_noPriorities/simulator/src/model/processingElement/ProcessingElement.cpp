/*******************************************************************************
 * Copyright (C) 2018 joseph
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
#include "ProcessingElement.h"

ProcessingElement::ProcessingElement(sc_module_name mn, Node& node, TrafficPool* tp)
        :
        node(node),
        trafficPool(tp)
{
    this->id = node.id%(globalResources.nodes.size()/2);
    this->dbid = rep.registerElement("NetworkInterface", this->id);
    rep.reportAttribute(dbid, "pos_x", std::to_string(node.pos.x));
    rep.reportAttribute(dbid, "pos_y", std::to_string(node.pos.y));
    rep.reportAttribute(dbid, "pos_z", std::to_string(node.pos.z));
    rep.reportAttribute(dbid, "clock", std::to_string(node.type->clockDelay));
    rep.reportAttribute(dbid, "type", node.type->model);
}
