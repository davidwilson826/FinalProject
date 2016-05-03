from ggame import App, Sprite, TextAsset
from time import time

class TimeText(Sprite):
    
    def __init__(self, asset, position):
        super().__init__(asset, position)
        
class Test(App):
    
    def __init__(self):
        super().__init__()
        self.start = time()
        self.elapsed = 0
        self.dispTime()
        
    def dispTime(self):
        self.elapsed = time()-self.start
        TimeText(TextAsset(str(self.elapsed//60)+':'+str(int(self.elapsed%60))))
        
    def step(self):
        self.getSpritesbyClass(TimeText)[0].destroy()
        self.dispTime()
        
Test().run()