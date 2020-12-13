#!/bin/bash
printf "Set governor \n"
echo polytech | sudo -S cpupower frequency-set -g performance

#c0:
cd c0/
./run.sh &
cd ..

#c1:
cd c1/
./run.sh &
cd ..

#c2:
cd c2/
./run.sh &
cd ..

#c3:
cd c3/
./run.sh &
cd ..

#c4:
cd c4/
./run.sh &
cd ..

#c5:
cd c5/
./run.sh &
cd ..

#c6:
cd c6/
./run.sh &
cd ..

#c7:
cd c7/
./run.sh &
cd ..

#c8:
cd c8/
./run.sh &
cd ..

#c9:
cd c9/
./run.sh &
cd ..



