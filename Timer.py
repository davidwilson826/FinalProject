from ggame import App
from time import time

class Timer(App):
    
    def __init__(self):
        super().__init__()
        self.frameTime = [time(),time()]
        self.deltaTime = 0
        
    def step(self):
        self.deltaTime = self.frameTime[1]-self.frameTime[0]
        print(self.deltaTime)
        
Timer().run()
