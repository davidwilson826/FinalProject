from ggame import App, Sprite, CircleAsset, Color, LineStyle

black = Color(0x000000, 1.0)

noline = LineStyle(0.0, black)

class Thing(Sprite):
    
    def __init__(self, asset, position):
        super().__init__(asset, position)
        self.fxcenter = self.fycenter = 0.5
        
class CenterTest(App):
    
    def __init__(self):
        super().__init__()
        Thing(CircleAsset(50, noline, black), (0,0))
        
CenterTest().run()