from random import uniform, randint
from math   import sqrt
from copy   import deepcopy

class Vector:
    v = []

    def __init__(self,  size, unit=False, rangee=(-10,10)):
        self.v = [] 
        for _ in range(size): self.v.append( uniform( rangee[0], rangee[1] ) )
        if unit: self.unit()

    def __str__(self):
        return str(self.v)

    def __repr__(self):
        return self.__str__()

    def len(self):
        s = 0.0
        for val in self.v: s += val**2
        return sqrt(s)

    def clean(self):
        size = len(self.v)
        self.v = [] 
        for _ in range(size): self.v.append( 0 )        

    def one(self):
        size = len(self.v)
        self.v = [] 
        for _ in range(size): self.v.append( 1 )
        return self

    def unit(self):
        l = self.len()
        for i in range(len(self.v)): self.v[i] = self.v[i]/l        

    def norm(self):
        new_v = Vector(len(self.v))
        l = self.len()
        if l == 0 : return new_v
        for i in range(len(self.v)): new_v.v[i] = self.v[i]/l
        return new_v

    def __sub__(self, v):
        new_v = Vector(len(self.v))
        for i in range(len(self.v)): new_v.v[i] = self.v[i] - v.v[i]
        return new_v

    def __add__(self, v):
        new_v = Vector(len(self.v))
        for i in range(len(self.v)): new_v.v[i] = self.v[i] + v.v[i]
        return new_v

    def __truediv__(self, v):
        new_v = Vector(len(self.v))
        for i in range(len(self.v)): new_v.v[i] = self.v[i]/v
        return new_v

    def __mul__(self, v):
        new_v = Vector(len(self.v))
        for i in range(len(self.v)): new_v.v[i] = self.v[i]*v
        return new_v       

    def __rmul__(self, nmb):
        return self.__mul__(nmb)

    def mutate(self, rate, value=uniform(-0.2,0.2)):
        if uniform(0,1) > rate: return
        self.v[ randint(0, len(self.v)-1) ] += value

    def __getitem__(self, i):    return self.v[i]
    def __setitem__(self, i, c): self.v[i] = c

    def max_normalization(self):
        return (self - (max(self.v)*Vector(len(self.v)).one())) / (max(self.v) - min(self.v))

    def min_normalization(self):
        return (self - (min(self.v)*Vector(len(self.v)).one())) / (max(self.v) - min(self.v))

    def mean_normalization(self):
        return (self - ((sum(self.v)/len(self.v))*Vector(len(self.v)).one())) / (max(self.v) - min(self.v))