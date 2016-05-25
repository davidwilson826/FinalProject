from ggame import App, Sprite, RectangleAsset, Color, LineStyle

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

black = Color(0x000000, 1.0)

noLine = LineStyle(0.0, black)

class Border(Sprite):
    width = 5

class Button(Sprite):
    pass
        
class Test(App):
    
    def __init__(self):
        super().__init__()
        Border(RectangleAsset(SCREEN_WIDTH, Border.width, noLine, black), (0, SCREEN_HEIGHT-(Border.width/2)))
        Border(RectangleAsset(Border.width, SCREEN_HEIGHT, noLine, black), (SCREEN_WIDTH-(Border.width/2), 0))
        for x in range(9):
            width = 0.2*SCREEN_WIDTH
            height = 0.2*SCREEN_HEIGHT
            Button(RectangleAsset(width, height, noLine, black), 
            ((x//3+1)/4*SCREEN_WIDTH-width/2,(x%3+1)/4*SCREEN_HEIGHT-height/2))
        for x in self.getSpritesbyClass(Button)[2:]:
            print(x.x,x.y)
            
Test().run()