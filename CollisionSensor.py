from ggame import App, Sprite, Color, LineStyle, RectangleAsset, CircleAsset

black = Color(0x000000, 1.0)
blue = Color(0x0000ff, 1.0)

noline = LineStyle(black, 0.0)

class Ball(Sprite):
    
    r = 30
    asset = CircleAsset(r, noline, black)
    
    def __init__(self, position):
        super().__init__(Ball.asset, position)
        self.fxcenter = self.fycenter = 0.5
        
class Collisions(App):
    
    def __init__(self):
        super().__init__()
        Ball((0,0))
        
Collisions().run()