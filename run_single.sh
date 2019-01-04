#!/bin/bash

mpiexec -machinefile ./allnodes -np 4 python ~/AR/assignment2/n_body_problem/main.py ./input/stars.csv ./output/stars.csv ./output/time.csv 1000 0.1

