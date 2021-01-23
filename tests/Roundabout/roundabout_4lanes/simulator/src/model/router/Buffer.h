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
#pragma once

#include <list>
#include "utils/Structures.h"
#include "utils/Report.h"
#include "model/traffic/Flit.h"

extern int buffer_idcnt;

template<class T>
class Buffer {
protected:
    std::list<T>* list;

public:
    int depth; //max elements of type T
    Report& rep = Report::getInstance();
    int id;
    int dbid;

    explicit Buffer(int depth)
            :
            depth(depth)
    {
        list = new std::list<T>;
        id = ++buffer_idcnt;
        dbid = rep.registerElement("Buffer", id);
    }

    ~Buffer()
    {
        delete list;
    }

    virtual bool enqueue(T) = 0;

    virtual T dequeue() = 0;

    virtual T front() = 0;

    virtual T back() = 0;

    bool empty()
    {
        return list->empty();
    }

    unsigned long free()
    {
        return depth-list->size();
    }

    unsigned long occupied()
    {
        return list->size();
    }

    void flush()
    {
        list->clear();
    }

};

template<typename T>
class BufferFIFO : public Buffer<T> {
public:
    explicit BufferFIFO(int depth)
            :
            Buffer<T>(depth)
    {
    }

    ~BufferFIFO() = default;

    bool enqueue(T a)
    {
        if (Buffer<T>::free()>0) {
            Buffer<T>::list->push_back(a);
            return true;
        }
        return false;
    }

    T dequeue()
    {
        if (!Buffer<T>::empty()) {
            T a = Buffer<T>::list->front();
            Buffer<T>::list->pop_front();
            return a;
        }
        return 0;
    }

    T front()
    {
        if (!Buffer<T>::empty()) {
            return Buffer<T>::list->front();
        }
        return 0;
    }

    T back()
    {
        if (!Buffer<T>::empty()) {
            return Buffer<T>::list->back();
        }
        return 0;
    }
};

template<typename T>
class BufferLIFO : public Buffer<T> {
public:
    explicit BufferLIFO(int depth)
            :
            Buffer<T>(depth)
    {
    }

    ~BufferLIFO() = default;

    bool enqueue(T a)
    {
        if (Buffer<T>::free()>0) {
            Buffer<T>::list->push_back(a);
            return true;
        }
        return false;
    }

    T dequeue()
    {
        if (!Buffer<T>::empty()) {
            T a = Buffer<T>::list->back();
            Buffer<T>::list->pop_back();
            return a;
        }
        return 0;
    }

    T front()
    {
        if (!Buffer<T>::empty()) {
            return Buffer<T>::list->back();
        }
        return 0;
    }

    T back()
    {
        if (!Buffer<T>::empty()) {
            return Buffer<T>::list->front();
        }
        return 0;
    }
};
