#!/bin/bash

mkdir build
cd build
cmake3 ..
make -j
cp sim ..
cd ..
rm -rf build
