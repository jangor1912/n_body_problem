import math


class Position(object):
    dim_no = 3

    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return str(self.to_list())

    def add(self, pos):
        self.x += pos.x
        self.y += pos.y
        self.z += pos.z
        return self

    def step(self, dt, vel):
        ds = Position.from_list(vel.multiply(dt).to_list())
        self.add(ds)
        return self

    def distance(self, pos):
        d_x = self.x - pos.x
        d_y = self.y - pos.y
        d_z = self.z - pos.z
        dist = math.sqrt(math.pow(d_x, 2) + math.pow(d_y, 2) + math.pow(d_z, 2))
        return dist

    @classmethod
    def from_list(cls, cust_list):
        pos = Position()
        pos.x = cust_list.pop(0)
        pos.y = cust_list.pop(0)
        pos.z = cust_list.pop(0)
        return pos

    def to_list(self):
        res = list()
        res.append(self.x)
        res.append(self.y)
        res.append(self.z)
        return res
