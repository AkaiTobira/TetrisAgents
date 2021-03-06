
class FPSCounter:
    counter   = 0
    drop_time = 1.0
    delayed   = 0.0

    currentValue = 0

    avg = []

    def update(self,delta):
        self.counter += 1
        self.delayed += delta
        if( self.drop_time < self.delayed):
            
            self.currentValue = self.counter

            self.avg.append( self.counter )
            if len(self.avg) > 10: self.avg = self.avg[1:]

            self.counter = 0
            self.delayed -= self.drop_time

    def getFPS(self):
        return str( self.currentValue ) + " - AVG: " + str( sum(self.avg)/10.0 ) 

