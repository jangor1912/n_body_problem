#!/bin/bash

for j in $(seq 32 32 128)
do
	for i in $(seq 1 8)
	do
		for k in $(seq 0 10)
		do
			mpiexec -machinefile ./allnodes -np ${i} python ~/AR/assignment2/n_body_problem/main.py ./input/${j}.csv ./output/stars.csv ./output/time.csv 100 0.1
		done
	done
done
