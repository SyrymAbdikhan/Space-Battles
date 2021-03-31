# helper class for countdowns
class Timer:
    def __init__(self, time):
        self.endtime = time
        self.counter = 0
        self.do = True
    
    def update(self):
        if not self.do:
            self.counter += 1
            if self.counter >= self.endtime:
                self.counter = 0
                self.do = True
