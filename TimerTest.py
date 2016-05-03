from ggame import App, Sprite, TextAsset
from time import time

class TimeText(Sprite):
    
    def __init__(self, asset, position):
        super().__init__(asset, position)
        
class Timer(App):
    
    def __init__(self):
        super().__init__()
        self.start = time()
        self.dispTime()
        
    def dispTime(self):
        elapsed = time()-self.start
        seconds = elapsed%60
        if seconds < 10:
            placeholder = ':0'
        else:
            placeholder = ':'
        TimeText(TextAsset(str(int(elapsed//60))+placeholder+str(int(seconds))), (200,200))
        
    def step(self):
        self.getSpritesbyClass(TimeText)[0].destroy()
        self.dispTime()
        
Timer().run()