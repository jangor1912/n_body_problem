#!/usr/bin/env python
import csv
import sys
from time import time

from mpi4py import MPI

from src.body.body import Body
from src.properties.position import Position
from src.properties.velocity import Velocity
from src.worker.worker import Worker


def create_bodies(input_csv):
    bodies = list()
    with open(input_csv, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            if int(row["step"]) == 0:
                id = int(row["id"])
                x = float(row["x"])
                y = float(row["y"])
                z = float(row["z"])
                vx = float(row["vx"])
                vy = float(row["vy"])
                vz = float(row["vz"])
                mass = float(row["mass"])
                position = Position(x, y, z)
                velocity = Velocity(vx, vy, vz)
                body = Body(position, velocity, mass)
                body.id = id
                bodies.append(body)
        # print('Processed {line_count} lines'.format(line_count=line_count))
    return bodies


def write_time_to_csv(csv_file, iterations, stars_csv, processors, delta, time):
    stars_no = int(stars_csv.split("/").pop().split(".").pop(0))
    with open(csv_file, 'a') as fd:
        fd.write("{iterations},{stars},{processors},{delta},{time}\n".format(iterations=iterations,
                                                                             stars=stars_no,
                                                                             processors=processors,
                                                                             delta=delta,
                                                                             time=time))


def sequential():
    input_csv_file_name = sys.argv[1]
    output_csv_file_name = sys.argv[2]
    time_stats_file_name = sys.argv[3]
    iterations = int(sys.argv[4])
    delta = float(sys.argv[5])

    bodies = create_bodies(input_csv_file_name)
    start = time()
    for i in xrange(iterations):
        bodies_acc = list()
        for body in bodies:
            bodies_acc.append(body.count_acceleration(bodies))

        for j, body in enumerate(bodies):
            body.step(delta, bodies_acc[j])
            # body.append_to_csv(output_csv_file_name, i)

    stop = time()
    write_time_to_csv(time_stats_file_name, iterations, input_csv_file_name, 1, delta, stop - start)


def parallel():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    processors = size
    parallel_data = (processors, rank, comm)

    input_csv_file_name = sys.argv[1]
    output_csv_file_name = sys.argv[2]
    time_stats_file_name = sys.argv[3]
    iterations = int(sys.argv[4])
    delta = float(sys.argv[5])

    bodies = create_bodies(input_csv_file_name)
    ids = Worker.get_proteges_ids(rank, processors, bodies)
    # the last processor gets most proteges with current metric
    buffer_size = len(Worker.get_proteges_ids(processors - 1, processors, bodies)) + Body.length_flat * 2
    worker = Worker(parallel_data, buffer_size, ids, bodies)

    comm.Barrier()
    start = MPI.Wtime()
    worker.run(delta, iterations)
    comm.Barrier()
    stop = MPI.Wtime()
    if rank == 0:
        write_time_to_csv(time_stats_file_name, iterations, input_csv_file_name, processors, delta, stop - start)


if __name__ == "__main__":
    try:
        xrange
    except NameError:
        xrange = range
    sequential()
