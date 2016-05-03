from ggame import App
from time import time

class Timer(App):
    
    def __init__(self):
        super().__init__()
        self.frameTime = [time(),time()]
        self.deltaTime = 0
        
    def step(self):
        self.frameTime[0] = self.frameTime[1]
        self.frameTime[1] = time()
        self.deltaTime = self.frameTime[1]-self.frameTime[0]
        print(round(self.deltaTime,10))
        
Timer().run()
