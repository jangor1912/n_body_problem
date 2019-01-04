#!/bin/bash

for i in $(seq 1 8)
do
    for k in $(seq 0 10)
    do
        mpiexec -machinefile ./allnodes -np ${i} python ~/AR/assignment2/n_body_problem/main.py ./input/1024.csv ./output/stars.csv ./output/time.csv 100 0.1
    done
done