import math
from uuid import uuid4

from src.properties.acceleration import Acceleration
from src.properties.position import Position
from src.properties.velocity import Velocity


class Body:
    length_flat = 2 + Position.dim_no + Velocity.dim_no
    grav_const = 6.67408e-11

    def __init__(self, position, velocity, mass):
        self.id = uuid4().int & (1 << 64) - 1
        self.position = position
        self.velocity = velocity
        self.mass = mass

    def __repr__(self):
        return "id={id}\nposition={position}\nvelocity={velocity}\nmass={mass}".format(id=self.id,
                                                                                       position=str(self.position),
                                                                                       velocity=str(self.velocity),
                                                                                       mass=str(self.mass))

    def count_acceleration(self, bodies):
        sum_x = 0.0
        sum_y = 0.0
        sum_z = 0.0
        for body in bodies:
            if self.id != body.id:
                tmp = (body.mass / math.pow(body.position.distance(self.position), 3))
                sum_x += tmp * (body.position.x - self.position.x)
                sum_y += tmp * (body.position.y - self.position.y)
                sum_z += tmp * (body.position.z - self.position.z)

        ax = self.grav_const * sum_x
        ay = self.grav_const * sum_y
        az = self.grav_const * sum_z
        acc = Acceleration(ax, ay, az)
        return acc

    def step(self, dt, acc):
        self.velocity.step(dt, acc)
        self.position.step(dt, self.velocity)
        return self

    def to_list(self):
        res = list()
        res.append(self.id)
        res.append(self.position.to_list())
        res.append(self.velocity.to_list())
        res.append(self.mass)
        return res

    @classmethod
    def from_list(cls, cust_list):
        id = cust_list.pop(0)
        position = Position.from_list(cust_list.pop(0))
        velocity = Velocity.from_list(cust_list.pop(0))
        mass = cust_list.pop(0)
        body = Body(position, velocity, mass)
        body.id = id
        return body

    def to_flat_list(self):
        res = list()
        res.append(self.id)
        for arg in self.position.to_list():
            res.append(arg)
        for arg in self.velocity.to_list():
            res.append(arg)
        res.append(self.mass)
        return res

    @classmethod
    def many_to_flat_list(cls, bodies):
        res = list()
        res.append(len(bodies))
        for body in bodies:
            res += body.to_flat_list()
        return res

    @classmethod
    def from_flat_list(cls, cust_list, many=False):
        bodies = list()
        if many is not True:
            cust_list = [1, cust_list]
        bodies_no = int(cust_list.pop(0))
        while bodies_no > 0:
            single_list = cust_list[:cls.length_flat]
            cust_list = cust_list[cls.length_flat:]
            id = single_list.pop(0)

            pos_list = single_list[:Position.dim_no]
            single_list = single_list[Position.dim_no:]
            position = Position.from_list(pos_list)

            vel_list = single_list[:Velocity.dim_no]
            single_list = single_list[Velocity.dim_no:]
            velocity = Velocity.from_list(vel_list)

            mass = single_list.pop(0)

            body = Body(position, velocity, mass)
            body.id = id
            bodies.append(body)
            bodies_no -= 1

        if many is not True:
            return bodies[0]
        return bodies

    def append_to_csv(self, csv_file, step):
        with open(csv_file, 'a') as fd:
            fd.write("{step},{id},{x},{y},{z},{vx},{vy},{vz},{mass}\n".format(step=step,
                                                                              id=self.id,
                                                                              x=self.position.x,
                                                                              y=self.position.y,
                                                                              z=self.position.z,
                                                                              vx=self.velocity.vx,
                                                                              vy=self.velocity.vy,
                                                                              vz=self.velocity.vz,
                                                                              mass=self.mass))
