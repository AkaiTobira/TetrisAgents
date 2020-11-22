
class FPSCounter:
    counter   = 0
    drop_time = 1.0
    delayed   = 0.0

    currentValue = 0

    def update(self,delta):
        self.counter += 1
        self.delayed += delta
        if( self.drop_time < self.delayed):
            self.currentValue = self.counter
            self.counter = 0
            self.delayed -= self.drop_time

    def getFPS(self):
        return str(self.currentValue)

