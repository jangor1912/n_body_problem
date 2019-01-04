import numpy as np
from mpi4py import MPI

from src.body.body import Body
from src.properties.acceleration import Acceleration


class Worker(object):

    def __init__(self, parallel_data, buffer_size, proteges_ids, all_bodies):
        self.processors, self.rank, self.comm = parallel_data
        self.proteges_ids = proteges_ids
        self.proteges = list()
        for body in all_bodies:
            if body.id in proteges_ids:
                self.proteges.append(body)

        self.buffer_size = buffer_size
        self.accumulator = dict()
        self.senders = list()
        self.receivers = list()
        self.package_length = dict()
        self.init_senders_and_receivers()

    def init_senders_and_receivers(self):
        if self.rank != 0:
            self.senders.append(self.rank-1)
        else:
            self.senders.append(self.processors-1)

        if self.rank != self.processors - 1:
            self.receivers.append(self.rank + 1)
        else:
            self.receivers.append(0)

    @classmethod
    def get_proteges_ids(cls, rank, processors, bodies):
        res = list()
        step = int(np.floor(len(bodies) / processors))
        start = rank * step
        stop = (rank + 1) * step
        cur_bodies = bodies[start:stop]
        if rank == processors - 1:
            cur_bodies = bodies[start:]
        for body in cur_bodies:
            res.append(body.id)
        return res

    def receive(self):
        bodies_flat_list = np.empty(Body.length_flat * self.buffer_size, dtype=np.float64)
        for sender in self.senders:
            self.comm.Recv([bodies_flat_list, MPI.DOUBLE], source=sender, tag=77)
        bodies_flat_list = list(bodies_flat_list)
        return bodies_flat_list

    def send(self, list_to_send):
        list_to_send = np.array(list_to_send, dtype=np.float64)
        for receiver in self.receivers:
            self.comm.Isend([list_to_send, MPI.DOUBLE], dest=receiver, tag=77)

    def run(self, delta=0.1, iterations=1000, csv_file=None):
        try:
            xrange
        except NameError:
            xrange = range

        for i in xrange(iterations):
            for j in xrange(self.processors + 1):
                bodies_to_send = self.proteges
                if j != 0:
                    bodies_flat_list = self.receive()
                    received_bodies = Body.from_flat_list(bodies_flat_list, many=True)
                    for body in self.proteges:
                        acc = body.count_acceleration(received_bodies)
                        prev_acc = self.accumulator.get(body.id, Acceleration(0, 0, 0))
                        self.accumulator[body.id] = prev_acc.add(acc)
                    bodies_to_send = received_bodies

                if j != self.processors:
                    bodies_flat_list = Body.many_to_flat_list(bodies_to_send)
                    self.send(bodies_flat_list)

            for body in self.proteges:
                acc = self.accumulator[body.id]
                body.step(delta, acc)
                if csv_file is not None:
                        body.append_to_csv(csv_file, i)

            self.accumulator = dict()
