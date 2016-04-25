from ggame import App, Sprite, CircleAsset, RectangleAsset, Color, LineStyle, TextAsset

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

black = Color(0x000000, 1.0)
white = Color(0x0000ff, 1.0)

noline = LineStyle(0.0, black)

def classDestroy(sclass):
    while len(Test.getSpritesbyClass(sclass)) > 0:
        for x in Test.getSpritesbyClass(sclass):
            x.destroy()

class Ball(Sprite):
    
    def __init__(self, asset, position):
        super().__init__(asset, position)
        self.fxcenter = self.fycenter = 0.5
        
    def step(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        
class Ball1(Ball):
    
    asset = CircleAsset(30, noline, black)
    
    def __init__(self, position):
        super().__init__(Ball1.asset, position)
        self.velocity = [5,0]
        self.mass = 5
        
class Ball2(Ball):
    
    asset = CircleAsset(30, noline, white)
    
    def __init__(self, position):
        super().__init__(Ball1.asset, position)
        self.velocity = [5,0]
        self.mass = 5
        
class Test(App):
    
    def __init__(self):
        super().__init__()
        Ball1((30,SCREEN_HEIGHT/2))
        Ball2((SCREEN_WIDTH-30,SCREEN_HEIGHT/2))
        
    def classStep(self, sclass):
        for x in self.getSpritesbyClass(sclass):
            x.step()
        
    def step(self):
#        self.classStep(Ball1)
#        self.classStep(Ball2)
        for x in [Ball1,Ball2]:
            for y in self.getSpritesbyClass(x):
                y.step()