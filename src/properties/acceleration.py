class Acceleration(object):
    dim_no = 3

    def __init__(self, ax=0.0, ay=0.0, az=0.0):
        self.ax = ax
        self.ay = ay
        self.az = az

    def __repr__(self):
        return str(self.to_list())

    def multiply(self, const):
        self.ax *= const
        self.ay *= const
        self.az *= const
        return self

    def add(self, acc):
        self.ax += acc.ax
        self.ay += acc.ay
        self.az += acc.az
        return self

    def to_list(self):
        res = list()
        res.append(self.ax)
        res.append(self.ay)
        res.append(self.az)
        return res
