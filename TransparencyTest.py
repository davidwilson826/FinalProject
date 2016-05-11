from ggame import App

class Transparency(App):
    
    def __init__(self):
        super().__init__()
        self.direction = 0
        self.transparency = 1
        
    def step(self):
        if self.transparency == 1:
            self.direction = -0.1
        elif self.transparency == 0:
            self.direction = 0.1
        self.transparency += self.direction
        print(self.transparency)