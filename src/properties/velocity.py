class Velocity(object):
    dim_no = 3

    def __init__(self, vx=0.0, vy=0.0, vz=0.0):
        self.vx = vx
        self.vy = vy
        self.vz = vz

    def __repr__(self):
        return str(self.to_list())

    def add(self, vel):
        self.vx += vel.vx
        self.vy += vel.vy
        self.vz += vel.vz
        return self

    def multiply(self, const):
        self.vx *= const
        self.vy *= const
        self.vz *= const
        return self

    def step(self, dt, acc):
        dv = Velocity.from_list(acc.multiply(dt).to_list())
        self.add(dv)
        return self

    @classmethod
    def from_list(cls, cust_list):
        vel = Velocity()
        vel.vx = cust_list.pop(0)
        vel.vy = cust_list.pop(0)
        vel.vz = cust_list.pop(0)
        return vel

    def to_list(self):
        res = list()
        res.append(self.vx)
        res.append(self.vy)
        res.append(self.vz)
        return res
