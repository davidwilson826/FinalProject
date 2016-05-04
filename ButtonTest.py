from ggame import App, Sprite, RectangleAsset, Color, LineStyle

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

black = Color(0x000000, 1.0)

noLine = LineStyle(0.0, black)

class Button(Sprite):
    
    def __init__(self, asset, position):
        super().__init__(asset, position)
        self.fxcenter = self.fycenter = 0.5
        
class Test(App):
    
    def __init__(self):
        super().__init__()
        Button(RectangleAsset(SCREEN_WIDTH, 5, noLine, black), (SCREEN_WIDTH/2, SCREEN_HEIGHT))
        Button(RectangleAsset(5, SCREEN_HEIGHT, noLine, black), (SCREEN_WIDTH, SCREEN_HEIGHT/2))
        for x in range(9):
            Button(RectangleAsset(20, 20, noLine, black), (0,0))