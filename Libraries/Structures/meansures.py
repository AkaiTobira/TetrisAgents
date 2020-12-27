import pygame

class TimerClock:
    clock = None
    delta = 0 

    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()

    def update(self):
        self.delta = self.clock.tick()/1000.0

class MeansuresClass:
    meansures = {}

    def __init__(self): pass

    def register_meansure(self, name):
        self.meansures[name] = 0.0

    def tick(self):
        for key in self.meansures.keys():
            self.meansures[key] += Time.delta

    def get_meansure(self, name):
        return self.meansures[name]

    def lap_meansure(self, name, _continue=True):
        value = self.meansures[name]
        if _continue: self.meansures[name] = 0
        else : del self.meansures[name]
        return value

Time = TimerClock()
Meansures = MeansuresClass()